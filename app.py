import os
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Table, Column, Integer, String, ForeignKey
# from sqlalchemy.ext.declarative import sqlalchemy.orm.declarative_base()
from sqlalchemy.orm import relationship, declarative_base
# from sqlalchemy import create_engine

username = os.environ.get('DB_USERNAME')
password = os.environ.get('DB_PASSWORD')
host = os.environ.get('DB_HOST', 'localhost')
port = int(os.environ.get('DB_PORT', '3306'))
db_name = os.environ.get('DB_NAME', 'db_ref')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{username}:{password}@{host}/{db_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Hospital(db.Model):
    __tablename__ = 'hospital'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    # Define a relationship with the services table using an association table
    services = db.relationship('Service', secondary='hospital_service', lazy='subquery',
        backref=db.backref('hospital', lazy=True))

    def __repr__(self):
        return f'<Hospital {self.name}>'

# Define a model for the services table
class Service(db.Model):
    __tablename__ = 'service'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Service {self.name}>'

# Define an association table for the many-to-many relationship between hospitals and services
hospital_service = db.Table('hospital_service',
    db.Column('hospital_id', db.Integer, db.ForeignKey('hospital.id'), primary_key=True),
    db.Column('service_id', db.Integer, db.ForeignKey('service.id'), primary_key=True)
)


@app.route('/')
def homepage():
    return render_template('home.html')

@app.route('/Search', methods=['GET'])
def Search():
    return render_template('index.html')

@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')

@app.route('/setup', methods=['GET'])
def setup():
    return render_template('setup.html')

@app.route('/hospitals', methods=['GET'])
def search_hospitals():
    
    query = request.args.get('query', '')
    hospitals = Hospital.query.filter(Hospital.name.ilike(f'%{query}%')).all()
    results = [{'id': hospital.id, 'name': hospital.name} for hospital in hospitals]
    return jsonify(results)
# @app.route('/search', methods=['POST'])
# def search():
#     keyword = request.form.get('keyword')
#     hospitals = Hospital.query.filter(Hospital.name.ilike(f'%{keyword}%')).all()
#     services = Service.query.filter(Service.name.ilike(f'%{keyword}%')).all()

#     hospitals_list = [hospital.to_dict() for hospital in hospitals]
#     services_list = [service.to_dict() for service in services]

#     return jsonify({'hospitals': hospitals_list, 'services': services_list})


if __name__ == "__main__":
    app.run(debug=True)
    # app.run(host='0.0.0.0', port=5000, debug=True)