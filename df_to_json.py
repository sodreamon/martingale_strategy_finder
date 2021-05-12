##########################################모듈##########################################
# 기본모듈
import os

# 데이터베이스
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

###########################################db 모델###########################################
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///symbol_data_json.db'
SQLALCHEMY_BINDS = {
        'df_db': 'sqlite:///symbol_data.db'
        }
db = SQLAlchemy(app)

# 기존 df db
class SymbolData(db.Model):
    __bind_key__ = 'df_db'
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(80), unique=True, nullable=False)
    data = db.Column(db.PickleType)

    def __repr__(self):
        return '<SymbolData %r>' % self.symbol

# 새로운 dict db
class SymbolDataJSON(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(80), unique=True, nullable=False)
    json_data = db.Column(db.PickleType)

    def __repr__(self):
        return '<SymbolDataJSON %r>' % self.symbol

db.create_all()

###########################################함수###########################################

