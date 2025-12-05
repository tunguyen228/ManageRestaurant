from flask import Flask
from config import Config
from models import db
from routes_view import view_bp
from routes_api import api_bp
from admin_panel import init_admin

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

# Đăng ký Blueprint
app.register_blueprint(view_bp)
app.register_blueprint(api_bp)

# Init Admin
init_admin(app, db)

if __name__ == '__main__':
    app.run(debug=True)