import os

from dotenv import load_dotenv
from flask_migrate import Migrate
from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy
import json

load_dotenv()
database_name = os.getenv('DATABASE_NAME')
database_username = os.getenv('DATABASE_USERNAME')
database_password = os.getenv('DATABASE_PASSWORD')
database_url = os.getenv('DATABASE_URL')
database_path = ('postgresql://{}:{}@{}/{}'.format(
    database_username,
    database_password,
    database_url,
    database_name))

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    migrate = Migrate(app, db)

'''
Movie
a persistent movie entity, extends the base SQLAlchemy Model
'''


class Movie(db.Model):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    release_date = Column(db.DateTime)

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date,
        }

    def rollback(self):
        db.session.rollback()

    def clean_all_data(self):
        db.session.query(Movie).delete()
        db.session.commit()

    def __repr__(self):
        return json.dumps(self.short())


class Actor(db.Model):
    __tablename__ = 'actors'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    gender = Column(String)

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender
        }

    def rollback(self):
        db.session.rollback()

    def clean_all_data(self):
        db.session.query(Actor).delete()
        db.session.commit()

    def __repr__(self):
        return json.dumps(self.short())
