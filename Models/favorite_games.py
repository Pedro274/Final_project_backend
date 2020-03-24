from db import db
import uuid


class FavoriteGamesModel(db.Model):
    __tablename__ = "favorite_games"

    id = db.Column(db.String(80), primary_key=True)
    game_id = db.Column(db.Integer(), required=True, nullable=False)

    # user relationship
    user_id = db.Column(db.String(80), db.ForeingKey('users.id'))
    user = db.Relationship('UserModel')

    def __init__(self, game_id, user_id):
        self.id = str(uuid.uuid4())
        self.game_id = game_id
        self.user_id = user_id

    def json(self):
        return {"favorite_game_id": self.game_id}

    def add_favorite_game_id(self):
        db.session.add(self)
        db.session.commit()

    def remove_favorite_game_id(self):
        db.session.add(self)
        db.session.commit()
