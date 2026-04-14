from flask import Flask
from modules.user.user_routes import user_bp
from blueprints.user_blueprint import user_bp


app = Flask(__name__)

#register blueprints
app.register_blueprint(user_bp)

if __name__ == '__main__':
    app.run(debug=True)


