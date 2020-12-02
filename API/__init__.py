from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)

engine = create_engine('mysql+pymysql://root@127.0.0.1:3306/lab5')

Session = sessionmaker(bind=engine)
