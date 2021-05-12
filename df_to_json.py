##########################################모듈##########################################
# 기본모듈
import os
import json

# 데이터베이스
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

###########################################db 모델###########################################
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///symbol_data.db'
app.config['SQLALCHEMY_BINDS'] = {
        'json_db': 'sqlite:///symbol_data_json.db'
        }
db = SQLAlchemy(app)

# 기존 df db
class SymbolData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(80), unique=True, nullable=False)
    data = db.Column(db.PickleType)

    def __repr__(self):
        return '<SymbolData %r>' % self.symbol

# 새로운 dict db
class SymbolDataJSON(db.Model):
    __bind_key__ = 'json_db'
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(80), unique=True, nullable=False)
    json_data = db.Column(db.PickleType)

    def __repr__(self):
        return '<SymbolDataJSON %r>' % self.symbol

db.create_all()
db.create_all(bind="json_db")

###########################################함수###########################################
#df db 개별 query row에서 df 불러오기
def call_df(db_row) :
    df = db_row.data
    symbol = db_row.symbol
    return df

# 불러온 df -> json 변환
def df_to_json(symbol_df):
    df = symbol_df
    df = df.reset_index()#여기서부터 'timestamp str으로 변환'
    df["Date"] = df["Date"].apply(str)
    df = df.set_index("Date")#여기까지 'timestamp str으로 변환'
    new_json = {}
    df_columns = list(df.columns) #데이터프레임 열(시고저종 볼륨 변동률)
    for _index in list(df.index) :
        _1_date_data_dict = {} #시종고저볼변 값 모두 삽입
        for _column in df_columns : #시고저종볼변 각각 해당
            _value = df.loc[_index,_column] #해당 인덱스의 해당 콜럼의 값
            _value = float(_value) #해당 값 모두 float값으로 변환(cython사용 예정))
            _1_date_data_dict[_column] = _value #해당일자 해당 시고저종볼변 값 삽입
        new_json[_index] = _1_date_data_dict #json 해당일자 모든 시고저종볼변 값 삽입
    new_json = json.dumps(new_json)
    return new_json

######################################메인작업######################################
symbol_data_query_list = SymbolData.query.order_by(SymbolData.symbol).all() #df db 모든 데이터 쿼리 리스트
count_n = 0
for symbol_data_query in symbol_data_query_list :
    symbol = symbol_data_query.symbol #심볼이름
    is_symbol_in_json_db = SymbolDataJSON.query.filter_by(symbol=symbol).first() #여기서부터 해당 심볼이 이미 json db에 있는지 찾기
    if is_symbol_in_json_db is not None:
        count_n += 1
        continue #여기까지 해당 심볼이 이미 json db에 있는지 찾기
    symbol_df = call_df(symbol_data_query) #{"symbol":symbol,"df":df} # 심볼 df
    symbol_json = df_to_json(symbol_df) #심볼 json
    new_json_db_row = SymbolDataJSON(symbol=symbol, json_data=symbol_json) #json db에 삽입할 row 제작
    db.session.add(new_json_db_row)
    db.session.commit()
    count_n += 1
    print("\r",count_n,end="")