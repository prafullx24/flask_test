from flask import Flask
from config import Config
from models import db
from routes import user_routes

app = Flask(__name__)
app.config.from_object(Config)

# Initialize the database
db.init_app(app)

# Register routes
app.register_blueprint(user_routes)

if __name__ == '__main__':
    app.run(debug=True)
