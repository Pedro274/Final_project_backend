import os
from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp
from Models.user import UserModel
from blacklist import BLACKLIST
from Tools.twilio import sms_contact
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    jwt_refresh_token_required,
    fresh_jwt_required,
    get_raw_jwt,
    get_jwt_claims
)

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
        username = data['username']
        user = UserModel.find_by_username(data['username'])
        if user:
            return {"message": f"Username '{data['username']}' already exists"}
        else:
            user = UserModel(**data)
            user.save_to_db()
            count_of_users = len(UserModel.query.all())
            sms_contact(os.getenv(
                'ADMIN_PHONE'), f"A new user just created an account (username: {username}) that makes {count_of_users} users")
        return {"message": "Acccount was created successfully"}, 201


class User(Resource):
    @jwt_required
    def get(self):
        user_id = get_jwt_identity()
        user = UserModel.find_by_id(user_id)
        return user.json()

    @fresh_jwt_required
    def delete(self):
        user_id = get_jwt_identity()
        user = UserModel.find_by_id(user_id)
        user.delete_from_db()
        return {"message": "User was deleted"}

    @fresh_jwt_required
    def put(self):
        data = _parser.parse_args()
        user_id = get_jwt_identity()
        user = UserModel.find_by_id(user_id)
        if safe_str_cmp(user.password, data['password']):
            return {"message": "You are using the same password please change it"}
        user.username = data['username']
        user.password = data['password']
        user.save_to_db()
        return {"message": "User name and password have been changed"}


class Users(Resource):
    @jwt_required
    def get(self):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {"message": "Sorry you need to have admin privilege in order to see all users"}
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
        return {"message": "Invalid credentials"}, 401


class Logout(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        BLACKLIST.append(jti)
        return {"message": "User successfully logged out"}


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {"new_access_token": new_token}
