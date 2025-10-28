from flask import Flask
from flask_migrate import Migrate
from dotenv import load_dotenv
from app.config import Config
from app.db import db

# --- Import NoSQL Initializers ---
# NOTE: Update the import path if necessary
from app.services.your_db_init import init_mongodb, init_cassandra 


load_dotenv()

def create_app():
    app = Flask(__name__)

    # 1. Load config (from config.py)
    app.config.from_object(Config)
    app.config['UPLOAD_FOLDER'] = 'uploads' # Ensure this is here for file handling

    # 2. Initialize SQL DB and migrations
    db.init_app(app)
    migrate = Migrate(app, db)

    # 3. Initialize NoSQL Connections (NEW LOCATION)
    # Call the initializers within the app context to ensure connections are available
    with app.app_context():
        print("Attempting NoSQL Database Connections...")
        init_mongodb()
        init_cassandra()
        # The global mongo_collection and session variables are now set

    # 4. Import models so they get registered with SQLAlchemy
    from app import models  

    # 5. Register Blueprints (routes)
    from app.routes.auth_routes import auth_bp
    from app.routes.admin_routes import admin_bp
    
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(admin_bp, url_prefix="/admin")
    
    # 6. Basic health check route
    @app.route("/")
    def home():
        return {"message": "University Management API is running "}

    return app