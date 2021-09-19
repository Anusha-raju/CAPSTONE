from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func




class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    name = db.Column(db.String(150))
    username = db.Column(db.String(150))
    data_stored = db.relationship('Forms')
    first_name = db.Column(db.String(150),default = None)
    last_name = db.Column(db.String(150),default = None)
    new_user = db.Column(db.String(4),default = 'yes')
    activity = db.Column(db.String(150),default = None)


class Forms(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    type_ = db.Column(db.String(150))
    data = db.relationship('Data')
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    clients = db.relationship('Client')

class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(300))
    compulsory = db.Column(db.String(150))
    data_type = db.Column(db.String(150))
    option_1 = db.Column(db.String(150))
    option_2 = db.Column(db.String(150))
    option_3 = db.Column(db.String(150))
    option_4 = db.Column(db.String(150))
    picture = db.Column(db.Text)
    mimetype = db.Column(db.Text)
    answer = db.Column(db.String(150))
    score = db.Column(db.Integer)
    neg_score = db.Column(db.Integer)
    data_id = db.Column(db.Integer, db.ForeignKey('forms.id'))
    columns = db.Column(db.String(1000))
    rows = db.Column(db.String(1000))
    layout = db.Column(db.String(150),default='top')
    timer = db.Column(db.Integer)


class Client(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(150))
    email = db.Column(db.String(150))
    form_id = db.Column(db.Integer, db.ForeignKey('forms.id'))
    total_score = db.Column(db.Integer)
    answers = db.relationship('Answers')

class Answers(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    question_id = db.Column(db.String(150))
    question = db.Column(db.String(300))
    data_type = db.Column(db.String(150))
    score = db.Column(db.Integer)
    neg_score = db.Column(db.Integer)
    correct_answer = db.Column(db.String(150))
    answer = db.Column(db.String(1500))
    result = db.Column(db.Integer)
    answers_info = db.Column(db.Text)
    mimetype = db.Column(db.Text)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))
    

class Unanswered(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    question_user_id = db.Column(db.String(150))
    questions = db.Column(db.String(1000))