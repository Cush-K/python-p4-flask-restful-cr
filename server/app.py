#!/usr/bin/env python3

from flask import Flask, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Newsletter

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///newsletters.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Home(Resource):
    def get(self):
        
        response_dict_list = [n.to_dict() for n in Newsletter.query.all()]
        
        return make_response(response_dict_list, 200)
    
    def post(self):
        new_record = Newsletter(
            title = request.form['title'],
            body = request.form['body']
        )
        
        db.session.add(new_record)
        db.session.commit()
        
        return make_response(new_record.to_dict(), 200)
        
api.add_resource(Home,'/newsletters')

class NewsletterById(Resource):
    
    def get(self, id):
        newsletter = Newsletter.query.filter(Newsletter.id==id).first()
        newsletter_dict = newsletter.to_dict()
        
        return make_response(newsletter_dict, 200)
    
    def patch(self, id):
        newsletter = Newsletter.query.filter(Newsletter.id==id).first()
        
        for attr in request.form:
            setattr(newsletter, attr, request.form.get(attr))

            db.session.add(newsletter)
            db.session.commit()
            
            return make_response(newsletter.to_dict(), 200)
        
    def delete(self, id):
        newsletter = Newsletter.query.filter(Newsletter.id==id).first()
        
        db.session.delete(newsletter)
        db.session.commit()
    
api.add_resource(NewsletterById, '/newsletters/<int:id>')

    
if __name__ == '__main__':
    app.run(port=5555, debug=True)
