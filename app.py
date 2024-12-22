from flask import Flask, url_for, redirect, render_template
import os
from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL 
from db import db
from db.models import user_data
from flask_login import LoginManager
from config import Config
from lab1 import lab1
from lab2 import lab2
from lab3 import lab3
from lab4 import lab4
from lab6 import lab6
from lab7 import lab7
from lab8 import lab8

app = Flask(__name__)

mysql = MySQL(app)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'секретный-секрет')
app.config['DB_TYPE'] = os.getenv('DB_TYPE', 'sqlite')

app.config['MYSQL_HOST'] = '31.31.196.16'
app.config['MYSQL_USER'] = 'u2939432_egor'
app.config['MYSQL_PASSWORD'] = '2004egor'
app.config['MYSQL_DB'] = 'u2939432_default'
app.config['MYSQL_PORT'] = 3306

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://u2939432_egor:2004egor@31.31.196.16/u2939432_default'

db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'lab8.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return user_data.query.get(int(user_id))

app.register_blueprint(lab1)
app.register_blueprint(lab2)
app.register_blueprint(lab3)
app.register_blueprint(lab4)
app.register_blueprint(lab6)
app.register_blueprint(lab7)
app.register_blueprint(lab8)

@app.errorhandler(404)
def not_found(err):
    path = url_for("static", filename = "404.png")
    style = url_for("static", filename = "lab1.css")
    return '''
<!doctype html>
<html>
<head>
    <link rel = "stylesheet" href="''' + style +'''"
</head>
    <body>
        <img src="''' + path + '''" class="full-screen-image">
    </body>
</html>
''', 404

@app.route('/')
@app.route('/index')
def index():
    style = url_for("static", filename="main.css")
    return '''<!doctype html>
        <html>
        <head>
            <link rel = "stylesheet" href="''' + style +'''"
            <title>НГТУ, ФБ, Лабораторные работы</title>
        </head>
           <header>
                НГТУ, ФБ, WEB-программирование, часть 2. Список лабораторных
           </header>
           <body>
                <li><a href='/lab1'>Первая лабораторная</a></li>
                <li><a href='/lab2/'>Вторая лабораторная</a></li>
                <li><a href='/lab3/'>Третья лабораторная</a></li>
                <li><a href='/lab4/'>Четвертая лабораторная</a></li>
                <li><a href='/lab5/'>Пятая лабораторная</a></li>
                <li><a href="/lab6">Шестая лабораторная</a></li>
                <li><a href="/lab7">Седьмая лабораторная</a></li>
                <li><a href="/lab8">Восьмая Лабораторная</a></li>
           </body>
           <footer>Иванов Егор Владиславович, ФБИ-22, 3 курс, 2024</footer>
        </html>''', 200

@app.errorhandler(500)
def internal_error(error):
    return '''
<!doctype html>
<html>
    <head>
        <title>Ошибка сервера</title>
    </head>
    <body>
        <h1>Произошла ошибка на сервере</h1>
        <p>Пожалуйста, попробуйте позже.</p>
    </body>
</html>
''', 500