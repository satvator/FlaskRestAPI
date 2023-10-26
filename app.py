from flask import Flask, request
from flask_restful import Api, Resource

app=Flask(__name__)
api=Api(app)

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