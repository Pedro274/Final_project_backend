from flask_restful import Resource, reqparse
from Models.user_details import UserDetailsModel
from Models.user import UserModel


class UserDetails(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("name",
                        type=str,
                        help="Please provide valid name")
    parser.add_argument("last_name",
                        type=str,
                        help="Please provide valid Last name")
    parser.add_argument("address",
                        type=str,
                        help="Please provide valid address")
    parser.add_argument("phone",
                        type=int,
                        help="Please provide valid phone number")

    def post(self, user_id):
        data = self.parser.parse_args()
        if UserModel.find_by_id(user_id):
            user_details = UserDetailsModel.find_by_user_id(user_id)
            if user_details:
                return {"message": "These user details already exist if you want to update please create a put request"}
            new_user_details = UserDetailsModel(user_id, **data)
            new_user_details.save_user_details_to_db()
            return {"message": "User details was created"}
        return{"message": "User do not exist"}

    def put(self, user_id):
        data = self.parser.parse_args()
        user_details = UserDetailsModel.find_by_user_id(user_id)
        if user_details:
            user_details.name = data['name'] if data['name'] else user_details.name
            user_details.last_name = data['last_name'] if data['last_name'] else user_details.last_name
            user_details.address = data['address'] if data['address'] else user_details.address
            user_details.phone = data['phone'] if data['phone'] else user_details.phone
            user_details.save_user_details_to_db()
            return {"message": "User details were updated"}
        return {"message": "User details do not exists"}

    def delete(self, user_id):
        user_details = UserDetailsModel.find_by_user_id(user_id)
        if user_details:
            user_details.delete_user_details_from_db()
            return {"message": "User details were deleted"}
        return {"message": "User details do not exists"}
