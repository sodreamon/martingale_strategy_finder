##########################################모듈##########################################
# 기본모듈
import os

# 데이터베이스
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

###########################################db 모델###########################################
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///symbol_data.db'
db = SQLAlchemy(app)

class SymbolData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(80), unique=True, nullable=False)
    data = db.Column(db.PickleType)

    def __repr__(self):
        return '<SymbolData %r>' % self.symbol

if not os.path.isfile("symbol_data.db") :
    db.create_all()



###########################################함수###########################################
