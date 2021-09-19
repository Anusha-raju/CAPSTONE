from flask import Blueprint, render_template, request, flash, redirect, url_for,session, logging, send_file
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from functools import wraps
from email_validator import validate_email, EmailNotValidError
#import Client
import os
import smtplib
from email.message import EmailMessage
from wtforms import Form, StringField, TextAreaField, PasswordField, validators, DateTimeField, BooleanField, IntegerField
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from passlib.hash import sha256_crypt
from werkzeug.utils import secure_filename
#from docx import Document
#from coolname import generate_slug
from datetime import timedelta, datetime
from flask_mail import Mail, Message
from threading import Thread
from flask import render_template_string
from itsdangerous import URLSafeTimedSerializer,SignatureExpired
from sqlalchemy.exc import IntegrityError
#from validate_email import validate_email
import random
import json
import csv
import operator
from wtforms_components import TimeField
from wtforms.fields.html5 import DateField
from wtforms.validators import ValidationError
import socket



auth = Blueprint('auth', __name__)


#os.environ.get('EMAIL_PASS')
EMAIL_ADDRESS = 'anushatest48@gmail.com'
EMAIL_PASSWORD = '48testanusha'





@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                flash('Logged in successfully!', category='success')
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)



@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully!', category='success')
    return redirect(url_for('auth.login'))



def asynch(f):
	@wraps(f)
	def wrapper(*args, **kwargs):
		thr = Thread(target=f, args=args, kwargs=kwargs)
		thr.start()
	return wrapper

@asynch
def send_async_email(msg):
	with smtplib.SMTP_SSL('smtp.gmail.com',465) as smtp:
		smtp.login(EMAIL_ADDRESS,EMAIL_PASSWORD)
		smtp.send_message(msg)



htmlbody='''
Your account on <b>Typesform</b> was successfully created.
Please click the link below to confirm your email address and
activate your account:
  
<a href="{{ confirm_url }}">Confirm Email</a>
 <p>
--
Questions? Comments? Email </p>
'''
def get_local_ip():	
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(('8.8.8.8', 1))
	local_ip_address = s.getsockname()[0]
	return local_ip_address

def send_email(recipients,html_body):

	try:
		msg = EmailMessage()
		msg['Subject'] = 'Confirm Your Email Address'
		msg['From'] = EMAIL_ADDRESS
		msg['To'] = recipients

		msg.add_alternative(html_body,subtype = 'html')
		send_async_email(msg)
		# return 'Mail sent!'
		return
	except Exception as e:
		# return(str(e))
		return

confirm_serializer = URLSafeTimedSerializer('hjshjhdjah kjshkjdhjs')
def send_confirmation_email(user_email):

	token = confirm_serializer.dumps(user_email, salt='email-confirm')
	link = url_for('auth.confirm_email', token=token, _external=True)
	html = render_template_string(htmlbody, confirm_url=link)
	send_email([user_email], html)
	return

@auth.route('/confirm_email/<token>')
def confirm_email(token):
    try:
        email = confirm_serializer.loads(token, salt='email-confirm', max_age=300)

    except SignatureExpired:
        return '<h1>The token is expired!</h1>'

    login_link = url_for('auth.login',_external=True)
    return '<h1>The token works!!</h1>'

class RegisterForm(Form):
	name = StringField('Name', [validators.Length(min=3, max=50)])
	username = StringField('Username', [validators.Length(min=4,max=25)])
	email = StringField('Email', [validators.Email()])
	password = PasswordField('Password', [
			validators.Regexp("^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$", message="Password should contain min 8 characters including 1 letter and 1 number."),
			validators.DataRequired(),
			validators.EqualTo('confirm', message="Password do not match")
		])
	confirm = PasswordField('Confirm Password')

#class First_name(Form):
	#first_name = StringField('First Name', [validators.Length(min=3, max=50)])


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
	form = RegisterForm(request.form)
	if request.method == 'POST' and form.validate() :
		name = form.name.data
		email = form.email.data
		#email verifier
		#data = client.get(email)

		try:
			valid = validate_email(email)
		except EmailNotValidError as e:
			flash('Invalid email, please provide a valid email address','danger')
			return render_template('sign_up.html', form=form)


		username = form.username.data
		password = generate_password_hash(form.password.data)

		try:
			new_user = User(email=email,password=password,name=name,username=username)
			db.session.add(new_user)
			db.session.commit()
			send_confirmation_email(email)
			flash('Thanks for registering!  Please check your email to confirm your email address.', category= 'success')
				
			return redirect(url_for('setup.name',email = email))

		except IntegrityError:
			flash('Email Exists','danger')
			return render_template('sign_up.html', form=form,user = current_user)

		



	return render_template('sign_up.html', form=form,user = current_user)

