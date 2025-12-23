import os
from flask import Flask, request, session, redirect, url_for
from config import Config
from models import db
from admin_panel import init_admin
#from flask_babel import Babel

from routes_api import api_bp
from routes_view import view_bp as main_bp
from routes_order import view_bp as order_bp
from api_order import order_api_bp

app = Flask(__name__)
app.config.from_object(Config)

#babel = Babel(app)

db.init_app(app)

app.register_blueprint(main_bp)
app.register_blueprint(api_bp)
app.register_blueprint(order_bp)
app.register_blueprint(order_api_bp)

init_admin(app, db)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)