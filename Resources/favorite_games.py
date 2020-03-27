from flask_restful import Resource, reqparse, request
from Models.user import UserModel
from Models.favorite_games import FavoriteGamesModel


class FavoriteGame(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("game_name",
                        required=True,
                        type=str,
                        help="Please provide valid name")
    parser.add_argument("game_url_id",
                        required=True,
                        type=int,
                        help="Please provide valid id")

    def post(self, user_id):
        data = self.parser.parse_args()
        if UserModel.find_by_id(user_id):
            favorite_games = FavoriteGamesModel.find_favorite_games_by_user_id(user_id)
            for favorite_game in favorite_games:
                if favorite_game.game_url_id == data['game_url_id']:
                    return {"message": "This game ID is already in your list of favorites"}
            new_favorite_game = FavoriteGamesModel(user_id, **data)
            new_favorite_game.save_favorite_game_id()
            return {"message": f"Favorite game was save to user_id: {user_id}"}
        return{"message": "User do not exist"}

    def delete(self, user_id):
        game_url_id = request.args.get('game_url_id')
        if not game_url_id:
            return {"message": "Please provide a (game_url_id = ? ) as query parameter to remove it from the list"}
        if UserModel.find_by_id(user_id):
            favorite_games = FavoriteGamesModel.find_favorite_games_by_user_id(user_id)
            for favorite_game in favorite_games:
                if favorite_game.game_url_id == int(game_url_id):
                    favorite_game.remove_favorite_game()
                    return {"message":"Game was removed from the list of favorites"},202
            return {"message":"Game is not in the list of favorites"}
        return{"message": "User do not exist"}
    
