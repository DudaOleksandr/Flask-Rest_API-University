from flask import Flask
from flask_bcrypt import Bcrypt
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

_version__ = '0.1.0'
app = Flask(__name__)
bcrypt = Bcrypt(app)

engine = create_engine('mysql+pymysql://root@127.0.0.1:3306/lab5')
SessionFactory = sessionmaker(bind=engine)
Session = scoped_session(SessionFactory)
session = Session()

from . import urls
from . import models
