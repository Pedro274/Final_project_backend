# Third party lib
from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager

# Local file
from db import db
from Resources.user import User, Users, Sign_up, Login
from Resources.user_details import UserDetails


app = Flask(__name__)
api = Api(app)
app.config['JWT_SECRET_KEY'] = 'kfj3etfht'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
jwt = JWTManager(app)


@app.before_first_request
def create_table():
    db.create_all()


api.add_resource(Login, '/login')
api.add_resource(Users, '/users')
api.add_resource(Sign_up, '/sign_up')
api.add_resource(User, '/user/<string:username>')
api.add_resource(UserDetails, '/user_details/<string:user_id>')


if __name__ == "__main__":
    app.run(port=3000, debug=True)
