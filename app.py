from flask import Flask, request
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import create_access_token, JWTManager, get_jwt_identity, jwt_required
app=Flask(__name__)


app.config['SECRET_KEY']='dlgnsg'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///database.db'
db=SQLAlchemy(app)
api=Api(app)
jwt=JWTManager(app)

class User(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(100), unique=True, nullable=False)
    password=db.Column(db.String(100), nullable=False)
    
with app.app_context():
    db.create_all()

class UserRegistration(Resource):
    def post(self):
        data=request.get_json()
        username=data['username']
        password=data['password']
        
        if not username or not password:
            return {'message': 'Missing username or password'}, 400
            
        if User.query.filter_by(username=username).first():
            return {'message': "username already taken!!"}, 400

        new_user=User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        return {'message': 'User created successfully!!'}, 200
    
class UserLogin(Resource):
    def post(self):
        data=request.get_json()
        username=data['username']
        password=data['password']
        user=User.query.filter_by(username=username).first()
        if user and user.password==password:
            access_token=create_access_token(identity=user.id)
            return {'access_token': access_token }, 200
        return {'message': 'Invalid credentials!!'}, 401
    
class ProtectedResource(Resource):
    @jwt_required()
    def get(self):
        current_user_id = get_jwt_identity()
        return {'message': f"hello user {current_user_id}, you accessed the protected resource"}, 200

api.add_resource(UserRegistration, '/register')
api.add_resource(UserLogin, '/login')
api.add_resource(ProtectedResource,'/secure')
    
    
###################### Exclusive REST-API Example ###############################    
    
data= [
    {"id": 1, 'name': "user1", 'age': 49},
    {"id": 2, 'name': "user2", 'age': 69}
]



class PeopleResource(Resource):
    def get(self):
        return data
    def put(self):
        person={
            'id':len(data)+1,
            'name':'User3',
            'age': 4
        }
        data.append(person)
        return person, 201


def find_person(person_id):
    for person in data: 
        if person['id']==person_id:
            return person
    
    return None

class PersonResource(Resource):
    def get(self, person_id):
        person= find_person(person_id)
        if person:
            return person
        return {'message': 'person not found!!'}, 404
    def put(self, person_id):
        person= find_person(person_id)
        if person:
            person['name']=request.json['name']
            person['age']=request.json['age']
            return person
        return {'message': 'person not found!!'}, 404
    
    def delete(self, person_id):
        global data
        data=[person for person in data if person['id'] != person_id]
        
        return {'message': 'person deleted succesfully!!'}, 200

api.add_resource(PeopleResource, '/people')
api.add_resource(PersonResource,'/people/<int:person_id>')



if __name__=='__main__':
    app.run()