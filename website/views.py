from flask import Blueprint, render_template, request, flash, jsonify,redirect,url_for,current_app,Response,make_response
from flask_login import login_required, current_user
from .models import User,Forms,Data,Client,Answers,Unanswered
from . import db
import json
import os

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from werkzeug.utils import secure_filename
from wtforms import widgets,Form,DateField,FileField, SelectMultipleField,SelectField,StringField, TextAreaField, PasswordField, validators, DateTimeField, BooleanField, IntegerField,RadioField,SubmitField
from wtforms.validators import ValidationError,InputRequired
from wtforms.fields.html5 import TelField,URLField,EmailField
import phonenumbers
from werkzeug.exceptions import BadRequestKeyError


views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        forms = request.form['action']
        if request.form['action'] == "add":
            return redirect(url_for('views.add_form'))
        else:
            return redirect(url_for('views.view_final',formsname=forms))

    return render_template("home_page.html",user = current_user)



@views.route('/add_form', methods=['GET','POST'])
@login_required
def add_form():
    if request.method == 'POST':
        name = request.form.get('name')
        type_ = request.form.get('type')
        new_form = Forms(name=name,type_ = type_,user_id = current_user.id)

        db.session.add(new_form)
        db.session.commit()
        flash('Form created!', category='success')
        return redirect(url_for('views.add_question',formname = name))


    return render_template("add_new_form.html" , user=current_user)


@views.route('/add_question/<formname>', methods=['GET','POST'])
@login_required
def add_question(formname):
    if request.method == 'POST':
        if request.form['action'] == "add":
            data_type = request.form.get('question_type')
            
            name = formname
            return redirect(url_for('views.add_question_type',formname = name,data_type = data_type))

        elif request.form['action'] == "submit":
            return redirect(url_for('views.home',user = current_user))

        else:
            dataId = request.form['action']
            return redirect(url_for('views.edit',dataId = dataId,formsname=formname))

    return render_template("add_new_question.html",user = current_user,formsname=formname)


@views.route('/add_question_type/<formname>,<data_type>', methods=['GET','POST'])
@login_required
def add_question_type(formname,data_type):
    if request.method == 'POST':
        name = formname
        form1 = Forms.query.filter_by(name=name).first()
        if data_type in ['Picture Multiple Choice','Picture Multiple Answers']:
            if request.files:
                file = request.files["image"]
            if file.filename == '':
                flash('No image selected for uploading')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                question = request.form.get('question')
                option_1 = request.form.get('option_1')
                option_2 = request.form.get('option_2')
                option_3 = request.form.get('option_3')
                option_4 = request.form.get('option_4')
                answer = request.form.get('answer')
                layout = request.form.get('layout')
                compulsory = request.form.get('compulsory')
                score = request.form.get('score')
                neg_score = request.form.get('neg_score')
                timer = request.form.get('timer')
                new_data = Data(question=question,score = score,timer = timer,layout = layout,compulsory=compulsory,neg_score = neg_score,option_1 = option_1,option_2 = option_2,option_3 = option_3,option_4 = option_4,answer=answer,data_id=form1.id,data_type = data_type,picture = file.read(),mimetype = file.mimetype)
            
                #filename = secure_filename(file.filename)
                #file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                    #print('upload_image filename: ' + filename)
            else:
                flash('Allowed image types are - png, jpg, jpeg, gif')
                return redirect(request.url)

           
        elif data_type in ['Multiple Choice','Multiple Answers']:
            question = request.form.get('question')
            option_1 = request.form.get('option_1')
            option_2 = request.form.get('option_2')
            option_3 = request.form.get('option_3')
            option_4 = request.form.get('option_4')
            compulsory = request.form.get('compulsory')
            answer = request.form.get('answer')
            score = request.form.get('score')
            neg_score = request.form.get('neg_score')
            timer = request.form.get('timer')
            new_data = Data(question=question,score = score,timer = timer,compulsory=compulsory,neg_score = neg_score,option_1 = option_1,option_2 = option_2,option_3 = option_3,option_4 = option_4,answer=answer,data_id=form1.id,data_type = data_type)
        
        elif data_type in ['Likert']:
            question = request.form.get('question')
            compulsory = request.form.get('compulsory')
            timer = request.form.get('timer')
            new_data = Data(question = question,timer = timer,compulsory=compulsory, data_type = data_type,data_id=form1.id)
            db.session.add(new_data)
            db.session.commit()
            dataid = new_data.id
            return redirect(url_for('views.likert',user = current_user,dataid = dataid,formname = formname))

        elif data_type in ['Short Text (min 10, max 144 characters)']:
            question = request.form.get('question')
            compulsory = request.form.get('compulsory')
            timer = request.form.get('timer')
            new_data = Data(question=question,data_id=form1.id,timer = timer,compulsory=compulsory,data_type = data_type)

        elif data_type in ['Yes or No','Fill in A Blank','Fill in the Blanks']:
            question = request.form.get('question')
            compulsory = request.form.get('compulsory')
            answer = request.form.get('answer')
            score = request.form.get('score')
            neg_score = request.form.get('neg_score')
            timer = request.form.get('timer')
            new_data = Data(question=question,data_id=form1.id,timer = timer,compulsory=compulsory,data_type = data_type,score = score,neg_score = neg_score,answer=answer)

        elif data_type in ['Dropdown']:
            question = request.form.get('question')
            compulsory = request.form.get('compulsory')
            option_1 = request.form.get('option_1')
            answer = request.form.get('answer')
            score = request.form.get('score')
            neg_score = request.form.get('neg_score')
            timer = request.form.get('timer')
            new_data = Data(question=question,option_1 = option_1,timer = timer,compulsory=compulsory,data_id=form1.id,data_type = data_type,score = score,neg_score = neg_score,answer=answer)

        else:
            question = request.form.get('question')
            compulsory = request.form.get('compulsory')
            score = request.form.get('score')
            neg_score = request.form.get('neg_score')
            timer = request.form.get('timer')
            new_data = Data(question=question,data_id=form1.id,timer = timer,compulsory=compulsory,data_type = data_type,score = score,neg_score = neg_score)


        db.session.add(new_data)
        db.session.commit()
        
        return redirect(url_for('views.add_question',user = current_user,formname = formname))

    return render_template("add_question.html",user = current_user,data_type = data_type)


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


aLLOWED_EXTENSIONS = set(['pdf', 'md', 'txt'])
def Allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in aLLOWED_EXTENSIONS
 
@views.route('/display_image/<dataaid>')
def display_image(dataaid):
    #print('display_image filename: ' + filename)
    data = Data.query.get(dataaid)
    return Response(data.picture, mimetype=data.mimetype)

@views.route('/display_file/<dataaid>')
def display_file(dataaid):
    #print('display_image filename: ' + filename)
    data = Answers.query.get(dataaid)
    return Response(data.answers_info, mimetype=data.mimetype)

@views.route('/likert/<dataid>,<formname>', methods=['GET','POST'])
@login_required
def likert(dataid,formname):
    data = Data.query.get(dataid)
    if request.method == 'POST':
        if request.form['action'] == 'add_column':
            column = request.form.get('column')
            if data.columns:
                new_column = data.columns+','+column
            else: 
                new_column = column
        
            data.columns = new_column
            db.session.commit()
        if request.form['action'] == 'add_row':
            row = request.form.get('row')
            if data.rows:
                new_row = data.rows+','+row
            else: 
                new_row = row

            data.rows = new_row
            db.session.commit()
        if request.form['action'] == 'submit':
            return redirect(url_for('views.add_question',user = current_user,formname = formname))
    return render_template("likert.html",user = current_user,question = data.question,columns = data.columns,rows = data.rows)

 

@views.route('/delete_forms', methods=['POST'])
def delete_forms():
    form = json.loads(request.data)
    formId = form['formId']
    note = Forms.query.get(formId)
    if note:
        db.session.delete(note)
        db.session.commit()

    return jsonify({})

@views.route('/delete_question', methods=['POST'])
def delete_question():
    form = json.loads(request.data)
    dataaId = form['dataaId']
    data = Data.query.get(dataaId)
    if data:
        db.session.delete(data)
        db.session.commit()

    return jsonify({})

@views.route('/next_question1',methods = ['POST'])
def next_question1():
    form = json.loads(request.data)
    questionid = form['questionid']
    client_id = form['client_id']
    data_id = form['data_id']
    question = Unanswered.query.get(questionid)
    curr_question = question.questions
    client = Client.query.get(client_id)
    cu_ques = remove_str(curr_question,len(data_id))
    cu_ques = cu_ques.replace(' ','')
    question.questions = cu_ques
    db.session.commit()
        
    return jsonify({})

@views.route('/delete/<id>/<name>')
def delete(id,name):
    data = Data.query.get(id)
    if data:
        db.session.delete(data)
        db.session.commit()
    return redirect(url_for('views.view', formsname = name ))


@login_required
@views.route('/view/<formsname>', methods=['GET','POST'])
def view(formsname):
    if request.method == 'POST':
        if request.form['action']:
            dataId = request.form['action']
            return redirect(url_for('views.edit_forms', formsname = formsname, dataId = dataId))
    return render_template("view.html",user = current_user,formsname = formsname)


@login_required
@views.route('/create_new_form/<formid>',methods = ['GET','POST'])
def create_new_form(formid):
    form = Forms.query.get(formid)
    if request.method == 'POST':
        name = request.form.get('name')
        type_ = request.form.get('type')


        new_form = Forms(name=name,type_ = type_,user_id = current_user.id)
        db.session.add(new_form)
        db.session.commit()

        for data in form.data:
            question = data.question
            compulsory = data.compulsory
            data_type = data.data_type
            option_1 = data.option_1
            option_2 = data.option_2
            option_3 = data.option_3
            option_4 = data.option_4
            picture = data.picture
            mimetype = data.mimetype
            answer = data.answer
            score = data.score
            neg_score = data.neg_score
            columns = data.columns
            rows = data.rows
            layout = data.layout
            timer = data.timer
            new_data = Data(columns = columns,rows = rows,question=question,score = score,timer = timer,layout = layout,compulsory=compulsory,neg_score = neg_score,option_1 = option_1,option_2 = option_2,option_3 = option_3,option_4 = option_4,answer=answer,data_id=new_form.id,data_type = data_type,picture = picture,mimetype = mimetype)
            db.session.add(new_data)
            db.session.commit()

        return redirect(url_for('views.view',formsname = name))

    return render_template("create_new_form.html",user=current_user)


@login_required
@views.route('/view_final/<formsname>', methods=['GET','POST'])
def view_final(formsname):
    if request.method == 'POST':
        if request.form['action']:
            formid = request.form['action']
            return redirect(url_for('views.create_new_form', formid = formid))
    return render_template("view_final.html",user = current_user,formsname = formsname)


@login_required
@views.route('/edit/<dataId>,<formsname>', methods=['GET','POST'])
def edit(dataId,formsname):
    dataId = dataId
    data = Data.query.get(dataId)
    if request.method == 'POST':
        data.question = request.form.get('question')
        data.compulsory = request.form.get('compulsory')
        data.score = request.form.get('score')
        data.neg_score = request.form.get('neg_score')
        if data.data_type in ['Multiple Choice','Multiple Answers','Picture Multiple Choice','Picture Multiple Answers']:
            data.option_1 = request.form.get('option_1')
            data.option_2 = request.form.get('option_2')
            data.option_3 = request.form.get('option_3')
            data.option_4 = request.form.get('option_4')
            data.answer = request.form.get('answer')
        if data.data_type in ['Picture Multiple Choice','Picture Multiple Answers']:
            if request.files:
                file = request.files["image"]
            if file.filename == '':
                flash('No image selected for uploading')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                data.picture = file.read()
                data.mimetype = file.mimetype

            else:
                flash('Allowed image types are - png, jpg, jpeg, gif')
                return redirect(request.url)

        if data.data_type in ['Yes or No','Fill in A Blank','Fill in the Blanks']:
            data.answer = request.form.get('answer')

        if data.data_type in ['Dropdown']:
            data.answer = request.form.get('answer')
            data.option_1 = request.form.get('option_1')


        db.session.commit()

        return redirect(url_for('views.add_question',formname = formsname))

    
    return render_template("edit.html",user = current_user,formsname = formsname,data=data)


@login_required
@views.route('/edit_forms/<formsname>,<dataId>', methods=['GET','POST'])
def edit_forms(formsname,dataId):
    form = Forms.query.filter_by(name = formsname)
    data = Data.query.get(dataId)
    if request.method == 'POST':
        data.question = request.form.get('question')
        data.compulsory = request.form.get('compulsory')
        data.score = request.form.get('score')
        data.neg_score = request.form.get('neg_score')
        if data.data_type in ['Multiple Choice','Multiple Answers','Picture Multiple Choice','Picture Multiple Answers']:
            data.option_1 = request.form.get('option_1')
            data.option_2 = request.form.get('option_2')
            data.option_3 = request.form.get('option_3')
            data.option_4 = request.form.get('option_4')
            data.answer = request.form.get('answer')
        if data.data_type in ['Picture Multiple Choice','Picture Multiple Answers']:
            if request.files:
                file = request.files["image"]
            if file.filename == '':
                flash('No image selected for uploading')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                data.picture = file.read()
                data.mimetype = file.mimetype

            else:
                flash('Allowed image types are - png, jpg, jpeg, gif')
                return redirect(request.url)


        if data.data_type in ['Yes or No','Fill in A Blank','Fill in the Blanks']:
            data.answer = request.form.get('answer')

        if data.data_type in ['Dropdown']:
            data.answer = request.form.get('answer')
            data.option_1 = request.form.get('option_1')

        db.session.commit()
        return redirect(url_for('views.view',formsname = formsname))

    
    return render_template("edit.html",user = current_user,formsname = formsname,data = data)

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class short_text(Form):
    short_text = StringField('short_text', [validators.Length(min=10, max=144)])
class phone(Form):
    phone = StringField('Phone')

    def validate_phone(self, phone):
        try:
            p = phonenumbers.parse(phone.data)
            if not phonenumbers.is_valid_number(p):
                raise ValueError()
        except (phonenumbers.phonenumberutil.NumberParseException, ValueError):
            raise ValidationError('Invalid phone number')

class long_text(Form):
    long_text = StringField('long_text', [validators.Length(min=50, max=500)])
class radio(Form):
    radio = RadioField('radio',choices = [])
class select(Form):
    select = MultiCheckboxField('select',choices = [])
class submit(Form):
    submit = SubmitField('Save')
class email(Form):
    email = EmailField('Email')
class drop(Form):
    drop = SelectField('Dropdown',choices = [])
class date(Form):
    date = DateField('Date',format='%Y-%m-%d')
class number(Form):
    number = IntegerField('number')
class blank(Form):
    blank = StringField('blank')
class file(Form):
    file = FileField('File_upload')
class link(Form):
    link = URLField('LINK')
class rate(Form):
    rate = SelectField('rate',choices = [])



class client_info(Form):
    name = StringField('Name', [validators.Length(min=3, max=50)])
    email = StringField('Email', [validators.Email()])


@views.route('/access_form/<formid>',methods=['GET','POST'])
def access_form(formid):
    form_data = Forms.query.get(formid)
    ids = []
    for data in form_data.data:
        ids.append(data.id)
    flash('Enter your details and fill the form!!!!!')
    client_information = client_info(request.form)
    if request.method == 'POST' and client_information.validate() :
        name = client_information.name.data
        email = client_information.email.data
        new_client = Client(email=email,name=name,form_id = form_data.id)
        db.session.add(new_client)
        db.session.commit()
        question_user_id = 'form_data.id'+','+'new_client.id'
        unanswered_questions = Unanswered(question_user_id = question_user_id,questions = str(ids))
        db.session.add(unanswered_questions)
        db.session.commit()
        questionid = unanswered_questions.id
        return redirect(url_for('views.display_question',questionid = questionid,client_id=new_client.id))
        
        
    return render_template("access_form.html",form = client_information)

def remove_str(s,length):
    l = list(s)
    for i in range(length+1):
        l.pop(1)
    return ''.join(l)

def next(s):
    l = list(s)
    a = []
    for i in l[1:]:
        if i == ',':
            break
        elif i == ']':
            break
        else:
            a.append(i)
    return ''.join(a)


@views.route('/display_question/<questionid>,<client_id>',methods = ['GET','POST'])
def display_question(questionid,client_id):
    question = Unanswered.query.get(questionid)
    curr_question = question.questions
    client = Client.query.get(client_id)
    try:
        new_id = next(curr_question)
        data = Data.query.get(new_id)


    except IndexError:
        return redirect(url_for('views.thank'))

    try:
        if data.data_type in ['Phone Number']:
            answerform = phone(request.form)
        elif data.data_type in ['Short Text']:
            answerform = short_text(request.form)
        elif data.data_type in ['Long Text']:
            answerform = long_text(request.form)
        elif data.data_type in ['Multiple Choice','Picture Multiple Choice']:
            answerform = radio(request.form)
            answerform.radio.choices = [(data.option_1,data.option_1),(data.option_2,data.option_2),(data.option_3,data.option_3),(data.option_4,data.option_4)]
        elif data.data_type in ['Multiple Answers','Picture Multiple Answers']:
            answerform = select(request.form)
            answerform.select.choices = [(data.option_1,data.option_1),(data.option_2,data.option_2),(data.option_3,data.option_3),(data.option_4,data.option_4)]
        elif data.data_type in ['Statement','Likert','File Upload']:
            answerform = submit(request.form)
        elif data.data_type in ['Yes or No']:
            answerform = radio(request.form)
            answerform.radio.choices = [('YES','YES'),('NO','NO')]

        elif data.data_type in ['Email (with validation)']:
            answerform = email(request.form)
        elif data.data_type in ['Date (with validation)']:
            answerform = date(request.form)
        elif data.data_type in ['Rating (out of 5)']:
            answerform = rate(request.form)
            answerform.rate.choices = [('1','1'),('2','2'),('3','3'),('4','4'),('5','5')]
        elif data.data_type in ['Dropdown']:
            answerform = drop(request.form)
            choose = [(choice,choice) for choice in data.option_1.split(',')]
            answerform.drop.choices = choose
        elif data.data_type in ['Number (with validation)']:
            answerform = number(request.form)
        elif data.data_type in ['Fill in A Blank','Fill in the Blanks']:
            answerform = blank(request.form)

        elif data.data_type in ['Website Link (with validation)']:
            answerform = link(request.form)

    except AttributeError:
        return redirect(url_for('views.thank'))

    try:
        if request.method == 'POST'and answerform.validate():
            print('hello')
            if data.data_type in ['Phone Number']:
                ans = answerform.phone.data
            elif data.data_type in ['Short Text']:
                ans = answerform.short_text.data
            elif data.data_type in ['Long Text']:
                ans = answerform.long_text.data
            elif data.data_type in ['Multiple Choice','Picture Multiple Choice']:
                ans = answerform.radio.data
            elif data.data_type in ['Multiple Answers','Picture Multiple Answers']:
                ans = answerform.select.data
                ans = ','.join(ans)
            elif data.data_type in ['Statement']:
                ans = answerform.submit.data
            elif data.data_type in ['Yes or No']:
                ans = answerform.radio.data
            elif data.data_type in ['Email (with validation)']:
                ans = answerform.email.data
            elif data.data_type in ['Date (with validation)']:
                ans = answerform.date.data
            elif data.data_type in ['Rating (out of 5)']:
                ans = answerform.rate.data
            elif data.data_type in ['Dropdown']:
                ans = answerform.drop.data
            elif data.data_type in ['Number (with validation)']:
                ans = answerform.number.data
            elif data.data_type in ['File Upload']:
                if request.files:
                    file = request.files['file']
                if file.filename == '':
                    flash('No File selected for uploading')
                    return redirect(request.url)
                if file and Allowed_file(file.filename):
                    ans = file.filename
                    answers_info = file.read()
                    mimetype = file.mimetype

                else:
                    flash('Allowed image types are - pdf,txt,md')
                    return redirect(request.url)




            elif data.data_type in ['Website Link (with validation)']:
                ans = answerform.link.data


            elif data.data_type in ['Likert']:
                temp_ans = []
                for row in data.rows.split(','):
                    answ = request.form[row]
                    temp_ans.append((row,answ))
                ans = str(temp_ans)



            elif data.data_type in ['Fill in A Blank','Fill in the Blanks']:
                ans = answerform.blank.data
                print(ans)

            if data.data_type in ['File Upload']:
                answered = Answers(question = data.question, question_id = data.id,data_type = data.data_type,answer = ans,client_id = client.id,answers_info=answers_info, mimetype = mimetype)
            elif data.data_type in ['Multiple Choice','Picture Multiple Choice','Multiple Answers','Picture Multiple Answers','Yes or No','Dropdown','Fill in A Blank','Fill in the Blanks']:
                answered = Answers(question = data.question, question_id = data.id,data_type = data.data_type,correct_answer = data.answer,score = data.score,neg_score = data.neg_score,answer = ans,client_id = client.id )
            else:
                answered = Answers(question = data.question, question_id = data.id,data_type = data.data_type,answer = ans,client_id = client.id )
            db.session.add(answered)
            db.session.commit()
            cu_ques = remove_str(curr_question,len(new_id))
            cu_ques = cu_ques.replace(' ','')
            question.questions = cu_ques
            db.session.commit()
            
            return redirect(url_for('views.display_question',questionid = question.id,client_id=client.id,length = len(new_id)))

    except BadRequestKeyError:
        return redirect(request.url) 
    return render_template("question.html",dataa = data,answerform = answerform,questionid = question.id,client_id=client.id)


@views.route('/thank/',methods = ['GET'])
def thank():
    return render_template("thank.html")



@views.route('/results/<formid>',methods = ['GET','POST'])
@login_required
def results(formid):
    form = Forms.query.get(formid)
    if request.method == 'POST':
        return redirect(url_for('views.home',user = current_user))
    return render_template("results.html",form = form)

@views.route('/details/<clientid>',methods = ['GET','POST'])
@login_required
def details(clientid):
    client = Client.query.get(clientid)
    client.total_score = scoring(client.id)
    if request.method == 'POST':
        return redirect(url_for('views.home',user = current_user))
    return render_template("details.html",client = client)


def scoring(clientid):
    client = Client.query.get(clientid)
    total = 0
    for answer in client.answers:
        if answer.data_type in ['Multiple Choice','Picture Multiple Choice','Multiple Answers','Picture Multiple Answers','Dropdown','Fill in A Blank','Fill in the Blanks']:
            evaluate = answer.answer.split(',')
            print('evaluate')
            print(evaluate)
            evaluator = answer.correct_answer.split(',')
            print('evaluator')
            print(evaluator)
            for index in range(min(len(evaluate),len(evaluator))):
                if evaluator[index] == evaluate[index]:
                    print(evaluator[index] == evaluate[index])
                    print(answer.result == None)
                    if answer.result == None:
                        answer.result = answer.score
                        print(answer.result)
                    else:
                        answer.result = answer.result+answer.score
                else:
                    if answer.result == None:
                        answer.result = answer.neg_score
                    else:
                        answer.result = answer.result+answer.neg_score
        try:           
            total = total+answer.result
        except:
            total =total

    return total

@views.route('/share/<formid>',methods = ['GET','POST'])
@login_required
def share(formid):
    link = url_for('views.access_form', formid=formid, _external=True)
    if request.method == 'POST':
        return redirect(url_for('views.home',user = current_user))
    return render_template("share.html",link = link)


@views.route('/skip/<questionid>,<client_id>,<data_id>',methods = ['GET','POST'])
def skip(questionid,client_id,data_id):
    if request.method == "POST":
        if request.form["action"] == 'yes':
            question = Unanswered.query.get(questionid)
            curr_question = question.questions
            client = Client.query.get(client_id)
            cu_ques = remove_str(curr_question,len(data_id))
            cu_ques = cu_ques.replace(' ','')
            question.questions = cu_ques
            db.session.commit()
            return redirect(url_for('views.display_question',questionid = question.id,client_id=client.id))
        else:
            return redirect(url_for('views.display_question',questionid = questionid,client_id=client_id))
    return render_template("skip.html")



@views.route('/next_question/<questionid>,<client_id>,<data_id>',methods = ['GET','POST'])
def next_question(questionid,client_id,data_id):

    if request.method == "POST":
        question = Unanswered.query.get(questionid)
        curr_question = question.questions
        client = Client.query.get(client_id)
        cu_ques = remove_str(curr_question,len(data_id))
        cu_ques = cu_ques.replace(' ','')
        question.questions = cu_ques
        db.session.commit()
        return redirect(url_for('views.display_question',questionid = question.id,client_id=client.id))
        
    return render_template("next.html")



@views.route('/plagarism/<formid>',methods = ['GET','POST'])
@login_required
def plagarism(formid):
    try:
        student_files=[]
        student_notes=[]
        form = Forms.query.get(formid)
        for clients in form.clients:
            for answer in clients.answers:
                if answer.answer.endswith('.txt'):
                    student_files.append(answer.answer)
                    student_notes.append(answer.answers_info)
        
        
        vectorize = lambda Text: TfidfVectorizer().fit_transform(Text).toarray()
        similarity = lambda doc1, doc2: cosine_similarity([doc1, doc2])

        vectors = vectorize(student_notes)
        s_vectors = list(zip(student_files, vectors))

        def check_plagiarism():
            plagiarism_results = set()
            nonlocal s_vectors
            for student_a, text_vector_a in s_vectors:
                new_vectors =s_vectors.copy()
                current_index = new_vectors.index((student_a, text_vector_a))
                del new_vectors[current_index]
                for student_b , text_vector_b in new_vectors:
                    sim_score = similarity(text_vector_a, text_vector_b)[0][1]
                    student_pair = sorted((student_a, student_b))
                    score = (student_pair[0], student_pair[1],sim_score)
                    plagiarism_results.add(score)
            return plagiarism_results
        
        data = check_plagiarism()
    except ValueError:
        data = ''
    if request.method == 'POST':
        return redirect(url_for('views.home',user = current_user))
    return render_template("plagarism.html",data = data)



@views.route('/pdf_template/<formsname>',methods = ['GET','POST'])
@login_required
def pdf_template(formsname):
    
    return render_template('download.html',formsname = formsname,user = current_user)

