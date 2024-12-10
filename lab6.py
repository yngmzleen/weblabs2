from flask import Blueprint, render_template, request, redirect, session, g
import sqlite3

lab6 = Blueprint('lab6', __name__)

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect('database.db')
        g.db.row_factory = sqlite3.Row
    return g.db

@lab6.teardown_app_request
def close_db(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()

@lab6.route('/lab6/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')

        if not login or not password:
            return render_template('lab6/login.html', error="Заполните все поля")

        db = get_db()
        cursor = db.cursor()

        cursor.execute('SELECT * FROM users WHERE login = ? AND password = ?', (login, password))
        user = cursor.fetchone()

        if user:
            session['user_id'] = user['id']
            session['login'] = user['login']
            return redirect('/lab6/')
        else:
            return render_template('lab6/login.html', error="Неверный логин или пароль")

    return render_template('lab6/login.html')

@lab6.route('/lab6/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')

        if not login or not password:
            return render_template('lab6/register.html', error="Заполните все поля")

        db = get_db()
        cursor = db.cursor()

        try:
            cursor.execute('INSERT INTO users (login, password) VALUES (?, ?)', (login, password))
            db.commit()
            return redirect('/lab6/login')
        except sqlite3.IntegrityError:
            return render_template('lab6/register.html', error="Пользователь с таким логином уже существует")

    return render_template('lab6/register.html')

@lab6.route('/lab6/logout')
def logout():
    session.pop('user_id', None)
    session.pop('login', None)
    return redirect('/lab6/login')

offices = []
for i in range(1, 11):
    offices.append({'number': i, 'tenant': '', 'price': 2000})

@lab6.route('/lab6/')
def lab():
    return render_template('lab6/lab6.html')

@lab6.route('/lab6/json-rpc-api/', methods=['POST'])
def api():
    data = request.json
    id = data['id']
    result = {
        'jsonrpc': '2.0',
        'id': id
    }

    db = get_db()
    cursor = db.cursor()

    if data['method'] == 'info':
        cursor.execute('SELECT * FROM offices')
        offices = cursor.fetchall()
        result['result'] = [{'number': office['number'], 'tenant': office['tenant'], 'price': office['price']} for office in offices]
        return result

    login = session.get('login')
    if not login:
        result['error'] = {
            'code': 1,
            'message': 'Unauthorized'
        }
        return result

    if data['method'] == 'booking':
        office_number = data['params']
        cursor.execute('SELECT * FROM offices WHERE number = ?', (office_number,))
        office = cursor.fetchone()

        if not office:
            result['error'] = {
                'code': -32601,
                'message': 'Office not found'
            }
            return result

        if office['tenant']:
            result['error'] = {
                'code': 2,
                'message': 'Already booked'
            }
            return result

        cursor.execute('UPDATE offices SET tenant = ? WHERE number = ?', (login, office_number))
        db.commit()
        result['result'] = 'success'
        return result

    if data['method'] == 'cancel':
        office_number = data['params']
        cursor.execute('SELECT * FROM offices WHERE number = ?', (office_number,))
        office = cursor.fetchone()

        if not office:
            result['error'] = {
                'code': -32601,
                'message': 'Office not found'
            }
            return result

        if not office['tenant']:
            result['error'] = {
                'code': 3,
                'message': 'Office not booked'
            }
            return result

        if office['tenant'] != login:
            result['error'] = {
                'code': 4,
                'message': "You didn't book this office"
            }
            return result

        cursor.execute('UPDATE offices SET tenant = NULL WHERE number = ?', (office_number,))
        db.commit()
        result['result'] = 'success'
        return result

    result['error'] = {
        'code': -32601,
        'message': 'Method not found'
    }
    return result