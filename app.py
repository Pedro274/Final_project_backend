# Third party lib
from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager

#python
import os
import datetime

# Local file
from db import db
from blacklist import BLACKLIST
from Resources.user import User, Users, Sign_up, Login, Logout, TokenRefresh
from Resources.user_details import UserDetails
from Resources.favorite_games import FavoriteGame


app = Flask(__name__)
api = Api(app)
app.config['JWT_SECRET_KEY'] = 'kfj3etfht'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(seconds=3600)
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
db.init_app(app)
jwt = JWTManager(app)


@jwt.expired_token_loader
def expire_token_callback():
    return jsonify({"message": "Please log back in to have access to your account", "error": "token_expire"}), 401


@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({"message": "Signature verification fail", "error": "invalid_token_loader"}), 401


@jwt.revoked_token_loader
def revoked_token_callback():
    return jsonify({"message": "User logged out of the account", "error": "revoked_token"})


@jwt.user_claims_loader
def claim_callback(identity):
    if identity in os.getenv('ADMIN_ID'):
        return {'is_admin': True}
    return {'is_admin': False}


@jwt.token_in_blacklist_loader
def jwt_blacklist_callback(decrypted_token):
    return decrypted_token['jti'] in BLACKLIST


@app.before_first_request
def create_table():
    db.create_all()


api.add_resource(User, '/user')
api.add_resource(Login, '/login')
api.add_resource(Users, '/users')
api.add_resource(Sign_up, '/sign_up')
api.add_resource(Logout, '/logout')
api.add_resource(UserDetails, '/user_details/<string:user_id>')
api.add_resource(FavoriteGame, '/favorite/<string:user_id>')
api.add_resource(TokenRefresh, '/refresh')


if __name__ == "__main__":
    app.run(port=3000, debug=True)
