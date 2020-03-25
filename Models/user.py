from db import db
import uuid


class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.String(), primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    
    # table relationship
    details = db.relationship('UserDetailsModel')
    favorite_games = db.relationship('FavoriteGamesModel', lazy= 'dynamic')

    def __init__(self, username, password):
        self.id = str(uuid.uuid4())
        self.username = username
        self.password = password

    def json(self):
        return {
            "username": self.username,
            "password": self.password,
            "id": self.id,
            "user_details": [detail.json() for detail in self.details],
            "favorite_games": [game.json() for game in self.favorite_games.all()]
        }

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
