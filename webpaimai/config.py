import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@localhost/campus_auction'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.urandom(24)
