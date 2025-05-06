'''
Table Name: user
Attributes:
user_id: Integer, Primary Key
name: String
email: String

Table Name: pet
Attributes:
pet_id: Integer, Primary Key
name: String 
type: String 
breed: String
age: Integer
status: String, indicating whether the pet is "available" or "adopted"

Table Name: adoption
Attributes:
adoption_id: Integer, Primary Key
user_id: Integer, Foreign Key referencing user.user_id
pet_id: Integer, Foreign Key referencing pet.pet_id
adoption_date: String

'''
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String)

class Pet(db.Model):
    pet_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    type = db.Column(db.String)
    breed = db.Column(db.String)
    age = db.Column(db.Integer)
    status = db.Column(db.String)

class Adoption(db.Model):
    adoption_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    pet_id = db.Column(db.Integer, db.ForeignKey('pet.pet_id'))
    adoption_date = db.Column(db.String)
