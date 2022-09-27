from flask import Flask, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_alembic import Alembic

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///accountant.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


def initials():
    db = SQLAlchemy(app)
    alembic = Alembic()
    alembic.init_app(app)
    return db
