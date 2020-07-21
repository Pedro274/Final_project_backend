from db import db
import uuid


class UserDetailsModel(db.Model):
    __tablename__ = "user_details"

    id = db.Column(db.String(), primary_key=True)
    name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    address = db.Column(db.String(80))
    phone = db.Column(db.BigInteger())
    email = db.Column(db.String(80))
    user_id = db.Column(db.String(80), db.ForeignKey('users.id'))

    #user relationship
    user = db.relationship('UserModel')

    def __init__(self, user_id, name, last_name, address, phone, email):
        self.id = str(uuid.uuid4())
        self.user_id = user_id
        self.name = name
        self.last_name = last_name
        self.address = address
        self.phone = phone
        self.email = email

    def json(self):
        return {
            "name": self.name,
            "last_name": self.last_name,
            "address": self.address,
            "phone": self.phone,
            "email": self.email
        }

    @classmethod
    def find_by_user_id(cls, user_id):
        return cls.query.filter_by(user_id=user_id).first()

    def save_user_details_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_user_details_from_db(self):
        db.session.delete(self)
        db.session.commit()
