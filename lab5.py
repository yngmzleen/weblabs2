from flask import Blueprint, render_template, request, redirect, session, current_app, url_for
import psycopg2
from os import path, close
import sqlite3
from psycopg2.extras import RealDictCursor
from werkzeug.security import check_password_hash, generate_password_hash

lab5 = Blueprint('lab5', __name__)

@lab5.route('/lab5/')
def lab():
    return render_template('lab5/lab5.html', login=session.get('login'))

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

@lab5.route('/lab5/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab5/register.html')

    login = request.form.get('login')
    password = request.form.get('password')
    if not (login and password):
        return render_template('lab5/register.html', error='Заполните все поля')
    
    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT login FROM users WHERE login=%s;", (login, ))
    else:
        cur.execute("SELECT login FROM users WHERE login=?;", (login, ))
    if cur.fetchone():
        db_close(conn, cur)
        return render_template('lab5/register.html', error='Данное имя уже занято')
    
    password_hash = generate_password_hash(password)
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("INSERT INTO users (login, password) VALUES (%s, %s);", (login, password_hash))
    else:
        cur.execute("INSERT INTO users (login, password) VALUES (?, ?);", (login, password_hash))

    db_close(conn, cur)
    return render_template('lab5/success.html', login=login)

@lab5.route('/lab5/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab5/login.html')
    
    login = request.form.get('login')
    password = request.form.get('password')
    if not (login and password):
        return render_template('lab5/login.html', error='Заполните все поля')
    
    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM users WHERE login=%s;", (login, ))
    else:
        cur.execute("SELECT * FROM users WHERE login=?;", (login, ))
    user = cur.fetchone()
    if not user:
        db_close(conn, cur)
        return render_template('lab5/login.html', error="Пользователь и/или пароль введены неверно!")
    
    if not check_password_hash(user['password'], password):
        db_close(conn, cur)
        return render_template('lab5/login.html', error="Пользователь и/или пароль введены неверно!")
    
    session['login'] = login
    db_close(conn, cur)
    return render_template('lab5/success_login.html', login=login)

@lab5.route('/lab5/create', methods=['GET', 'POST'])
def create():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    if request.method == 'GET':
        return render_template('/lab5/create_article.html')

    title = request.form.get('title')
    article_text = request.form.get('article_text')
    is_public = request.form.get('is_public') == '1'

    if not (title and article_text):
        return render_template('/lab5/create_article.html', error='Введите текст и название статьи!')

    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT * FROM users WHERE login=?;", (login,))

    login_id = cur.fetchone()['id']

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("INSERT INTO articles(user_id, title, article_text, is_public) VALUES (%s, %s, %s, %s);", (login_id, title, article_text, is_public))
    else:
        cur.execute("INSERT INTO articles(login_id, title, article_text, is_public) VALUES (?, ?, ?, ?);", (login_id, title, article_text, is_public))

    db_close(conn, cur)
    return redirect('/lab5')

@lab5.route('/lab5/list')
def list():
    login = session.get('login')

    conn, cur = db_connect()

    sqllite = False
    is_admin = False

    if login == 'admin':
        is_admin = True
    user_id = None
    if login:
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT id FROM users WHERE login = %s;", (login,))
        else:
            cur.execute("SELECT id FROM users WHERE login = ?;", (login,))
            sqllite = True

        user = cur.fetchone()
        user_id = user['id'] if user else None

    if current_app.config['DB_TYPE'] == 'postgres':
        query = """
            SELECT articles.id, articles.title, articles.article_text, articles.is_favorite, articles.is_public, articles.likes, users.login as creator_login 
            FROM articles 
            JOIN users ON articles.user_id = users.id
        """
    else:
        query = """
            SELECT articles.id, articles.title, articles.article_text, articles.is_favorite, articles.is_public, articles.likes, users.login as creator_login 
            FROM articles 
            JOIN users ON articles.user_id = users.id
        """
    conditions = []
    params = []

    if login:
        if current_app.config['DB_TYPE'] == 'postgres':
            conditions.append("(articles.is_public = TRUE OR articles.user_id = %s)")
        else:
            conditions.append("(articles.is_public = TRUE OR articles.user_id = ?)")
        params.append(user_id)
    else:
        conditions.append("articles.is_public = TRUE")

    if conditions:
        query += " WHERE " + " AND ".join(conditions)
    
    query += " ORDER BY articles.is_favorite DESC, articles.id DESC;"

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute(query, tuple(params) if params else ())
    else:
        cur.execute(query, tuple(params) if params else ())

    articles = cur.fetchall()

    db_close(conn, cur)

    return render_template('/lab5/articles.html', articles=articles, filter_type='all', sqllite=sqllite, is_admin=is_admin)
