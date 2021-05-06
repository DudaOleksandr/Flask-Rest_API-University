from flask import Flask
from flask_bcrypt import Bcrypt
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from flask_cors import CORS


_version__ = '0.1.0'
app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.config['TESTING'] = True
bcrypt = Bcrypt(app)
engine = create_engine('mysql+pymysql://root@127.0.0.1:3306/lab5')
SessionFactory = sessionmaker(bind=engine)
Session = scoped_session(SessionFactory)
session = Session()

# from . import urls
from API import models
from API import urls
