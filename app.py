from flask import Flask
from extensions import db
from blueprints.user_blueprint import user_bp
from modules.user.user_model import User
from modules.user import user_routes 
from waitress import serve


app = Flask(__name__)

# MySQL connection string
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/flask_crud_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize DB
db.init_app(app)

# Register blueprint
app.register_blueprint(user_bp)


if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=5000, threads=8)

