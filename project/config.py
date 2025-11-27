import os

class Config:
    # Thay mật khẩu MySQL của bạn vào đây
    SECRET_KEY = 'ptt_team_super_secret'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:200905@localhost/quan_ly_nha_hang'
    SQLALCHEMY_TRACK_MODIFICATIONS = False