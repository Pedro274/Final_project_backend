from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp
from Models.user import UserModel
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required

_parser = reqparse.RequestParser()
_parser.add_argument("username",
                            type=str,
                            required=True,
                            help="Username required to create a new account")
_parser.add_argument("password",
                            type=str,
                            required=True,
                            help="Password required to create a new account")

class Sign_up(Resource):
    def post(self):
        data = _parser.parse_args()
        user = UserModel.find_by_username(data['username'])
        if user:
            return {"message": f"Username '{data['username']}' already exists"}
        else:
            user = UserModel(**data)
            user.save_to_db()
        return {"message": "Acccount was created successfully"}, 201


class User(Resource):
    @jwt_required
    def get(self, username):
        user = UserModel.find_by_username(username)
        if(user):
            return user.json()
        return{"message": "Sorry username does not exist"}, 404

    @jwt_required
    def delete(self, username):
        user = UserModel.find_by_username(username)
        print(user)
        if(user):
            user.delete_from_db()
            return {"message": "User was deleted"}
        return{"message": "Sorry username does not exist"}, 404


class Users(Resource):
    def get(self):
        return {"Users": list(map(lambda user: user.json(), UserModel.query.all()))}


class Login(Resource):
    def post(self):
        data = _parser.parse_args()
        user = UserModel.find_by_username(data['username'])
        if user and safe_str_cmp(user.password, data['password']):
            token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(identity=user.id)
            return {
                "token": token,
                "refresh_token": refresh_token
            }, 200
        return {"message": "Invalid credentials"}
