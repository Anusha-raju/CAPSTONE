from flask import Blueprint, render_template, request, flash, jsonify, redirect ,url_for
from flask_wtf import FlaskForm
from wtforms import Form,StringField, validators
from flask_login import login_required, current_user,login_user
from .models import User
from . import db
import json
import os


setup = Blueprint('setup', __name__)

class First_name(Form):
	first_name = StringField('First Name', [validators.Length(min=3, max=50)])

class Last_name(Form):
	last_name = StringField('Last Name', [validators.Length(min=3, max=50)])



@setup.route('/name/<email>', methods=['GET', 'POST'])
def name(email):
	email = email
	user = User.query.filter_by(email=email).first()
	if user.new_user == 'no':
		return '<h1>This page is not accesible by you</h1>'
	else:
		form = First_name(request.form)
		if request.method == 'POST' and form.validate() :
			first_name = form.first_name.data
			user = User.query.filter_by(email=email).first()

			user.first_name = first_name
			db.session.commit()

			flash('first name added successfully!!!' , category = 'success')
			return redirect(url_for('setup.lastname',email = email))


	return render_template('first_name.html', form = form)

@setup.route('/lastname/<email>', methods=['GET', 'POST'])
def lastname(email):
	email = email
	user = User.query.filter_by(email=email).first()
	if user.new_user == 'no':
		return '<h1>This page is not accesible by you</h1>'
	else:
		form = Last_name(request.form)
		if request.method == 'POST' and form.validate() :
			last_name = form.last_name.data
			user = User.query.filter_by(email=email).first()

			user.last_name = last_name
			db.session.commit()

			flash('last name added successfully!!!' , category = 'success')
			return redirect(url_for('setup.activity',email = email))

	return render_template('last_name.html', form = form)


@setup.route('/activity/<email>', methods=['GET', 'POST'])
def activity(email):
	email = email
	user = User.query.filter_by(email=email).first()
	if user.new_user == 'no':
		return '<h1>This page is not accesible by you</h1>'
	else:
		if request.method == 'POST':
			activity = request.form.get('activity')
			user = User.query.filter_by(email=email).first()

			user.activity = activity
			user.new_user = 'no'
			db.session.commit()



			login_user(user, remember=True)

			flash('Account created!', category='success')

			return redirect(url_for('views.home',user = current_user))

			


	return render_template('activity.html', email=email)