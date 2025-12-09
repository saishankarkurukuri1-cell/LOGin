from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from database.config import Config
from database.models import db,bcrypt
from auth.routes import auth_bp

# Initialize extensions
jwt = JWTManager()


def create_app():
    app = Flask(__name__)
    # loads Configurations
    app.config.from_object(Config)

    # Initializing Extensions....Connects Flask app to these extensions
    CORS(app)
   
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # Register blueprints
    
    app.register_blueprint(auth_bp, url_prefix="/auth")

    # Creates Database Tables
    with app.app_context():
        db.create_all()
    return app

# Runs the Server
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)