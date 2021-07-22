from OnlineExamSystem import app , db , bcrypt
from flask import redirect , render_template , url_for , flash  , request , abort , Response
from OnlineExamSystem.models import User , Question , Subjects
from OnlineExamSystem.forms import LoginForm , RegistrationForm , UpdateAccountForm , QuestionForm , TestForm
from flask_login import login_user , current_user , logout_user , login_required
from datetime import datetime
from random import randint
import cv2
import os
from threading import Thread

@app.route('/')
@app.route('/homepage')
def home_page() : 
    global count
    count = 0
    return render_template('home.html' , title = 'Home')

@app.route('/register' , methods=['GET' , 'POST'])
def register_page() :
    if current_user.is_authenticated :
        return redirect(url_for('home_page'))
    form = RegistrationForm()
    if form.validate_on_submit() :
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(
            name = form.name.data ,
            username = form.username.data , 
            gender = form.gender.data ,
            password = hashed_password
        )
        db.session.add(user)
        db.session.commit()

        flash('Registered Successfully' , 'success')
        return redirect(url_for('home_page'))
    return render_template('register.html' , title = 'Register' , form = form)

@app.route('/login' , methods=['GET' , 'POST'])
def login_page() :
    if current_user.is_authenticated :
        return redirect(url_for('home_page'))
    form = LoginForm()
    if form.validate_on_submit() :
        user = User.query.filter_by(username =form.username.data).first()
        if user and bcrypt.check_password_hash(user.password , form.password.data) :
            login_user(user , remember = form.remember.data)
            next_page = request.args.get('next')
            flash(f'Logged in Successfully.' , 'success')
            return redirect(next_page) if next_page else redirect(url_for('home_page'))
        else :
            flash(f'Incorrect Username or Password.' , 'danger')
 
    return render_template('login.html' , title = 'Login' , form = form)

@app.route('/logout')
def logout() :
    logout_user()
    return redirect(url_for('home_page'))

@app.route('/feeds')
def feeds_page() :
    return render_template('feeds.html' , title = 'Feeds')

@app.route('/rules')
def rules_page() :
    return render_template('rules.html' , title = 'Rules')

@app.route('/account/<string:username>')
def account(username) :
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('account.html' , title = 'Account' , user = user)

@app.route('/account/update_account' , methods=['GET' , 'POST'])
@login_required
def update_account() : 

    form = UpdateAccountForm()
    if form.validate_on_submit() :
        current_user.username = form.username.data
        current_user.name = form.name.data
        current_user.gender = form.gender.data
        db.session.commit()
        flash(f'Account Updated.' , 'success')
        return redirect(url_for('home_page'))
    
    elif request.method == 'GET' :
        form.username.data = current_user.username
        form.name.data = current_user.name
        form.gender.data = current_user.gender

    return render_template('update_account.html' , title = 'Edit Account' , form = form)

name = ''
count = 0
capture = 0
@app.route('/pre_test' , methods = ['GET' , 'POST'])
@login_required
def pretest_page() :
    global count
    global capture
    global name
    global marks
    name = current_user.name
    count = 0
    marks = 0
    if current_user.image_file == 'default.jpg' :
        global switch,camera
        global p
        
        if request.form.get('click') == 'Capture':
            global capture
            print('Capture')
            capture=1
            now = datetime.now() 
            now = now.strftime("%d_%m_%Y") + f"_{name.replace(' ','')}"     
            p = f"shot_{str(now)}.jpg"
            current_user.image_file = p
            db.session.commit()
        if request.method=='POST':
            print('POST')
            return render_template('pretest_screen.html' , user = current_user , title = 'Ready?')
        return render_template('camera_page.html')
    return render_template('pretest_screen.html' , user = current_user , title = 'Ready?')
    
marks = 0
@app.route('/test' , methods = ['GET' , 'POST'])
@login_required
def test_page() :
    global count
    global idx , marks
    global questions
    form = TestForm()
    
    if count == 0 :
        questions = list(Question.query.all())
    if form.validate_on_submit() :
        response = form.options.data
        print(response)
        if questions[idx].correct == int(response) :
            marks = marks + 2
        count = count + 1
        questions = list(Question.query.all())
    
    idx = randint(0,len(questions)-1)
    if count < 20 :
        return render_template('test_page.html' , title = 'Test' , count = count + 1 ,  question = questions[idx] , form = form , user = current_user)
    else :
        #code will be added here
        return render_template('result.html' , user = current_user , marks = marks)

p = ''
camera = cv2.VideoCapture(0)

@login_required
def gen_frames():
    global out, capture,rec_frame
    global p
    while True:
        success, frame = camera.read() 
        if success:   
            if(capture):
                capture=0
                now = datetime.now()
                now = now.strftime("%d_%m_%Y") + f"_{name.replace(' ','')}"
                p = f"shot_{str(now)}.jpg"
                cv2.imwrite('OnlineExamSystem/static/uploads/{}'.format(p), frame)
        
            try:
                ret, buffer = cv2.imencode('.jpg', cv2.flip(frame,1))
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            except Exception as e:
                pass
@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')