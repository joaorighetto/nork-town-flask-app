import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv


load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')

db = SQLAlchemy(app)


@app.route('/')
def home():
    return "Hello, World!"


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)