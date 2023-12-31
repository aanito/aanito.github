import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')

db = SQLAlchemy(app)

class Base(db.Model):
    __abstract__ = True

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

def create_database(db_name):
    # get the credentials from environmental variables
    username = os.environ.get('DB_USERNAME')
    password = os.environ.get('DB_PASSWORD')
    host = os.environ.get('DB_HOST', 'localhost')
    port = int(os.environ.get('DB_PORT', '3306'))
    db_name = os.environ.get('DB_NAME', 'db_ref')

    engine = create_engine(f'mysql://{username}:{password}@{host}:{port}')
    with engine.connect() as conn:
        query = f"CREATE DATABASE IF NOT EXISTS {db_name}"
        conn.execute(text(query))

    # app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') + '/' + db_name
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{username}:{password}@{host}:{port}/{db_name}'
    db.init_app(app)
    db.create_all()

    return db.engine, Base


# import os
# import sqlalchemy
# from sqlalchemy import text
# from sqlalchemy import create_engine, column
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker

# def create_database(db_name):
#     # Get the credentials from environmental variables
#     username = os.environ.get('DB_USERNAME')
#     password = os.environ.get('DB_PASSWORD')
#     host = os.environ.get('DB_HOST', 'localhost')
#     port = int(os.environ.get('DB_PORT', '3306'))
#     db_name = os.environ.get('DB_NAME', 'db_ref')
    
#     engine = create_engine(f'mysql://{username}:{password}@{host}:{port}')
#     with engine.connect() as conn:
#         query = f"create database if not exists {db_name}"
#         conn.execute(text(query))

#     engine = create_engine(f'mysql://{username}:{password}@{host}:{port}/{db_name}')
#     base = declarative_base()

#     return engine, base

