from enum import unique
from sqlalchemy import PrimaryKeyConstraint, delete
from . import db 
from flask_login import UserMixin
from sqlalchemy.sql import func

#Navigation links
class Navigation(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(20))

#User
class User(db.Model, UserMixin):
  id = db.Column(db.Integer, primary_key=True)
  #image = 
  full_name = db.Column(db.String(20))    
  email = db.Column(db.String(50), unique=True)
  password = db.Column(db.String(50))
  contact_num = db.Column(db.String(20))
  skype = db.Column(db.String(50))
  location = db.Column(db.Integer)
  github = db.Column(db.String(50))
  is_admin = db.Column(db.Boolean, default=False, nullable=False)
  cv = db.relationship('Cv')

#Work Experience
class Cv(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
  title = db.Column(db.String(20))
  company_name = db.Column(db.String(50))  
  start_date = db.Column(db.String(20))
  end_Date = db.Column(db.String(20))    
  country = db.relationship('Country', backref='cv', uselist=False)
  locaton = db.Column(db.String(20))
  cv_descs = db.relationship('Cv_Desc')
  portfolio_links = db.relationship('Portfolio_links')

class Country(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(20))
  cv_id = db.Column(db.Integer, db.ForeignKey('cv.id'))

class Cv_Desc(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  desc = db.Column(db.String(10000))
  cv_id = db.Column(db.Integer, db.ForeignKey('cv.id'))

class Portfolio_links(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  desc = db.Column(db.String(100))
  cv_id = db.Column(db.Integer, db.ForeignKey('cv.id'))

#Skills matrix
# class Skills(db.Model):
#   id = db.Column(db.Integer, primary_key=True)
#   title = db.Column(db.String(20))
#   length = db.Column(db.String(20))
#   level = db.relationship('Levels')

# class Levels(db.Model):
#   id = db.Column(db.Integer, primary_key=True)
#   title = db.Column(db.String(20))

#Accomplishments/Education
class Education(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(20))
  desc = db.Column(db.String(20))


    
