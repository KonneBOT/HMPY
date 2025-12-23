from routes import app, db
from flask import render_template, send_from_directory, request, redirect, url_for, session, flash
import os
from sqlalchemy import text
from util import getAllInfo
import time
import secrets

def generate_captcha():
    a = secrets.randbelow(8) + 1
    b = secrets.randbelow(8) + 1
    session['captcha_answer'] = str(a + b)
    return f"{a} + {b} = ?"

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                          'favicon.ico',mimetype='image/vnd.microsoft.icon')

@app.route('/')
def index():
    sessionName = session.get('name')
    if not sessionName:
        return redirect(url_for('login_page'))
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login_page():

    if request.method == 'POST':
        username = request.form.get('Username')
        password = request.form.get('Password')
        user_captcha = request.form.get('captcha', '').strip()

        if 'login_attempts' in session and session['login_attempts'] >= app.config['MAX_LOGIN_ATTEMPTS']:
            return "Account locked. Please try again later."

        if username is None or isinstance(username,str) is False or len(username) < 1:
            print("Something with username is wrong 1")
            return render_template('login.html')

        if password is None or isinstance(password,str) is False or len(password) < 1:
            print("Something with password is wrong 2")
            return render_template('login.html')

        if 'login_attempts' in session:
            session['login_attempts'] += 1
        else:
            session['login_attempts'] = 1

        # Captcha
        correct_answer = session.get('captcha_answer')
        if not correct_answer or user_captcha != correct_answer:
            flash("Captcha wrong - try again.", "error")
            return render_template('login.html')

        qstmt = text("SELECT * FROM bugusers WHERE username = :username AND password = :password") # Query Statement
        print(f"qstmt: {qstmt}")
        result = db.session.execute(qstmt, {"username": username, "password": password})
        user = result.fetchall()

        if not user:
            print("Something wrong 3")
            return render_template('login.html')


        print(f"Login: OK, Forwarding...", user)
        resp = redirect('/home')
        session['name'] = username
        return resp
    else:
        captcha_question = generate_captcha()
        session.pop('name', None)   # Reset User Session
        return render_template('login.html', captcha=captcha_question)

@app.route('/logout')
def logout():
    resp = redirect('/')
    session.pop('name', None)   # Reset User Session
    return resp

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    if request.method == 'GET':
        return render_template('register.html')

    if request.method == 'POST':
        username = request.form.get('username')
        email_address = request.form.get('email_address')
        password = request.form.get('password')

        if username is None or isinstance(username, str) is False or len(username) < 1:
            print("Register: Something with username is wrong 1")
            return render_template('register.html')

        if password is None or isinstance(password, str) is False or len(password) < 1:
            print("Register: Something with password is wrong 2")
            return render_template('register.html')

        qstmt = text(f"INSERT INTO bugusers (username, email_address, password) VALUES (:username, :email_address, :password);")  # Query Statement
        print(f"qstmt: {qstmt}")
        result = db.session.execute(qstmt, {"username": username, "email_address": email_address, "password": password})
        print(
            f"Register: User {username} registered successfully."
        )

        qstmt = text("SELECT * FROM bugusers WHERE username = ':username';")
        user = db.session.execute(qstmt, {"username": username,}).fetchall()
        print(f"Register Result: {user}")
        if user:
            db.session.commit()
            print("Register: OK, Forwarding...")
            resp = redirect('/home')
            session['name'] = username
            return resp
        else:
            print("Register: Something went wrong 4")
            resp = redirect('/register')
            return resp


@app.route('/home')
def home_page():    
    sessionName = session.get('name')
    if not sessionName:
        return redirect(url_for('login_page'))

    trains, stations, rides = getAllInfo()

    return render_template('home.html', trains=trains, stations=stations, rides=rides)

@app.route('/trains')
def trains_page():
    sessionName = session.get('name')
    if not sessionName:
        return redirect(url_for('login_page'))
    
    trains, stations, rides = getAllInfo()
    return render_template('trains.html', trains=trains, stations=stations, rides=rides)


@app.route('/rides', methods=['GET', 'POST'])
def rides_page():
    sessionName = session.get('name')
    if not sessionName:
        return redirect(url_for('login_page'))
    
    if request.method == "GET":
        trains, stations, rides = getAllInfo()
        return render_template('rides.html', trains=trains, stations=stations, rides=rides)
    if request.method == "POST":
        pass

@app.route('/new')
def new_page():
    sessionName = session.get('name')
    if not sessionName:
        return redirect(url_for('login_page'))

    return render_template('new.html')

@app.route('/new_train', methods=['GET', 'POST'])
def new_train_page():
    sessionName = session.get('name')
    if not sessionName:
        return redirect(url_for('login_page'))

    # Neuen Zug anlegen
    if request.method == "GET":
        return render_template('new_train.html')
    if request.method == "POST":
        name = request.form.get('name')
        typ = request.form.get('typ')
        comment = request.form.get('comment')
        if name and typ and comment:
            qstmt = f"INSERT INTO zug (name, typ, comment) VALUES ('{name}', '{typ}', '{comment}')"
            db.session.execute(text(qstmt))
            db.session.commit()
            return redirect('/trains')
        else:
            return redirect('/new_train')

@app.route('/new_ride', methods=['GET', 'POST'])
def new_ride_page():
    sessionName = session.get('name')
    if not sessionName:
        return redirect(url_for('login_page'))

    # Neue Zugfahrt anlegen
    if request.method == "GET":

        trains_result = db.session.execute(text("SELECT * FROM zug")).fetchall()
        stations_result = db.session.execute(text("SELECT * FROM bahnhof")).fetchall()

        # Umwandeln in Listen aus Dictionaries
        trains = [{"id": t.id, "name": t.name, "typ": t.typ, "comment": t.comment} for t in trains_result]
        stations = [{"id": s.id, "name": s.name, "ort": s.ort} for s in stations_result]

        return render_template('new_ride.html', trains=trains, stations=stations)

    if request.method == "POST":
        start_station_id = request.form.get('start_station_id')
        end_station_id = request.form.get('end_station_id')
        start_time = request.form.get('start_time')
        end_time = request.form.get('end_time')
        train_id = request.form.get('train_id')
        delay = request.form.get('delay')
        comment = request.form.get('comment')
        if start_station_id and end_station_id and start_time and end_time and train_id and delay and comment:
            print("New Ride hat POST bekommen: ", start_station_id, end_station_id, start_time, end_time, train_id, delay, comment)
            qstmt = f"INSERT INTO zugfahrt (start_station_id, end_station_id, start_time, end_time, train_id, comment, delay) VALUES ({start_station_id}, {end_station_id}, '{start_time}', '{end_time}', {train_id}, '{comment}', {delay})"
            db.session.execute(text(qstmt))
            db.session.commit()
            return redirect('/rides')
        else:
            return redirect('/new_ride')



@app.route('/new_station', methods=['GET', 'POST'])
def new_station_page():
    sessionName = session.get('name')
    if not sessionName:
        return redirect(url_for('login_page'))

    if request.method == "GET":
        return render_template("new_station.html")

    if request.method == "POST":
        name = request.form.get('name')
        ort = request.form.get('ort')
        if name and ort:
            qstmt = text("INSERT INTO bahnhof (name, ort) VALUES (':name', ':ort')")
            db.session.execute(qstmt, {'name': name, 'ort': ort})
            db.session.commit()
            return redirect('/home')
        else:
            return redirect('/new_station')

@app.route('/train')
def train_page():
    sessionName = session.get('name')
    if not sessionName:
        return redirect(url_for('login_page'))
    
    train_id = request.args.get('id')
    qstmt = text("SELECT * FROM zug WHERE id = :trainId")
    result = db.session.execute(qstmt, {'trainId': train_id}).fetchall()
    print("Results Trains: ", result)
    print("Länge Liste: ", len(result))
    return render_template('train.html', result=result)