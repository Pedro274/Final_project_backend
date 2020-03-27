from db import db
import uuid


class FavoriteGamesModel(db.Model):
    __tablename__ = "favorite_games"

    id = db.Column(db.String(80), primary_key=True)
    game_name = db.Column(db.String(80))
    game_url_id = db.Column(db.BigInteger(), nullable=False)

    # user relationship
    user_id = db.Column(db.String(80), db.ForeignKey('users.id'))
    user = db.relationship('UserModel')

    def __init__(self, user_id, game_name, game_url_id):
        self.id = str(uuid.uuid4())
        self.user_id = user_id
        self.game_name = game_name
        self.game_url_id = game_url_id
        

    def json(self):
        return {
            "game_name": self.game_name,
            "game_url_id": self.game_url_id
        }

    @classmethod
    def find_favorite_games_by_user_id(cls, user_id):
        return cls.query.filter_by(user_id=user_id).all()

    def save_favorite_game_id(self):
        db.session.add(self)
        db.session.commit()

    def remove_favorite_game(self):
        db.session.delete(self)
        db.session.commit()
