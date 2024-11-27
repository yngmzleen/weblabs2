from flask import Blueprint, render_template, request, redirect, session, current_app
import psycopg2
from os import path, close
import sqlite3
from psycopg2.extras import RealDictCursor
from werkzeug.security import check_password_hash, generate_password_hash

lab6 = Blueprint('lab6', __name__)

@lab6.route('/lab6/')
def lab():
    return render_template('lab6/lab6.html')

offices = []
for i in range(1, 11):
    offices.append({'number': i, 'tenant': ''})

def db_connect():

    
    if current_app.config['DB_TYPE'] == 'postgres':
        conn = psycopg2.connect(
            host = '127.0.0.1',
            database = 'egor_ivanov_knowledge_base',
            user = 'egor_ivanov_knowledge_base',
            password = '2004'
        )
        cur = conn.cursor(cursor_factory=RealDictCursor)
    else:
        dir_path = path.dirname(path.realpath(__file__))
        db_path = path.join(dir_path, 'database.db')
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
    return conn, cur
def db_close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()

@lab6.route('/lab6/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab6/lab6_register.html')

    login = request.form.get('login')
    password = request.form.get('password')
    if not (login and password):
        return render_template('lab6/lab6_register.html', error='Заполните все поля')
    
    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT login FROM users WHERE login=%s;", (login, ))
    else:
        cur.execute("SELECT login FROM users WHERE login=?;", (login, ))
    if cur.fetchone():
        db_close(conn, cur)
        return render_template('lab6/lab6_register.html', error='Данное имя уже занято')
    
    password_hash = generate_password_hash(password)
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("INSERT INTO users (login, password) VALUES (%s, %s);", (login, password_hash))
    else:
        cur.execute("INSERT INTO users (login, password) VALUES (?, ?);", (login, password_hash))

    db_close(conn, cur)
    return render_template('lab6/lab6_success.html', login=login)

@lab6.route('/lab6/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab6/lab6_login.html')
    
    login = request.form.get('login')
    password = request.form.get('password')
    if not (login and password):
        return render_template('lab6/lab6_login.html', error='Заполните все поля')
    
    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM users WHERE login=%s;", (login, ))
    else:
        cur.execute("SELECT * FROM users WHERE login=?;", (login, ))
    user = cur.fetchone()
    if not user:
        db_close(conn, cur)
        return render_template('lab6/lab6_login.html', error="Пользователь и/или пароль введены неверно!")
    
    if not check_password_hash(user['password'], password):
        db_close(conn, cur)
        return render_template('lab6/lab6_login.html', error="Пользователь и/или пароль введены неверно!")
    
    session['login'] = login
    db_close(conn, cur)
    return render_template('lab6/lab6_success.html', login=login)

@lab6.route('/lab6/json-rpc-api/', methods=['POST'])
def api():
    data = request.json
    id = data['id']
    if data['method'] == 'info':
        return {
            'jsonrpc': '2.0',
            'result': offices,
            'id': id
        }
    
    login = session.get('login')
    if not login:
        return {
            'jsonrpc': '2.0',
            'error': {
                'code': 1,
                'message': 'Unauthorized'
            },
            'id': id
        }
    
    if data['method'] == 'booking':
        office_number = data['params']
        for office in offices:
            if office['number'] == office_number:
                if office['tenant'] != '':
                    return {
                        'jsonrpc': '2.0',
                        'error': {
                            'code': 2,
                            'message': 'Already booked'
                        },
                        'id': id
                    }
                
                office['tenant'] = login
                return {
                    'jsonrpc': '2.0',
                    'result': 'success',
                    'id': id
                }
    
    if data['method'] == 'cancellation':
        office_number = data['params']
        
        # Проверка, что офис арендован
        office_found = False
        for office in offices:
            if office['number'] == office_number:
                office_found = True
                if office['tenant'] == '':
                    return {
                        'jsonrpc': '2.0',
                        'error': {
                            'code': 3,
                            'message': 'Office is not booked'
                        },
                        'id': id
                    }
                
                # Проверка, что арендатор — текущий пользователь
                if office['tenant'] != login:
                    return {
                        'jsonrpc': '2.0',
                        'error': {
                            'code': 4,
                            'message': 'You are not the tenant of this office'
                        },
                        'id': id
                    }
                
                # Снятие аренды
                office['tenant'] = ''
                return {
                    'jsonrpc': '2.0',
                    'result': 'success',
                    'id': id
                }
        
        if not office_found:
            return {
                'jsonrpc': '2.0',
                'error': {
                    'code': 5,
                    'message': 'Office not found'
                },
                'id': id
            }
    
    return {
        'jsonrpc': '2.0',
        'error': {
            'code': -32601,
            'message': 'Method not found'
        },
        'id': id
    }

@lab6.route('/lab6/logout')
def logout():
    session.pop('login_id', None)
    session.pop('login', None)
    return redirect('/lab6/lab6_login')