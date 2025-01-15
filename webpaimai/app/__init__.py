import os
from flask import Flask, send_from_directory, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from config import Config
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()
def create_app():
    app = Flask(__name__, template_folder='D:/ns/webpaimai/templates')
    print("Template folder:", app.template_folder)
    app.config.from_object(Config)
    db.init_app(app)
    CORS(app, origins=["http://localhost:8080"])

    @app.route('/')
    @app.route('/<path:path>')
    def serve(path='index.html'):
        try:
            if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
                return send_from_directory(app.static_folder, path)
            else:
                return render_template('index.html')
        except Exception as e:
            print(f"Error occurred: {type(e).__name__} - {e}")
            return f"An error occurred: {type(e).__name__} - {e}", 500

    from app.routes import main
    app.register_blueprint(main)

    return app