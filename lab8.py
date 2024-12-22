from flask import Blueprint, url_for, redirect, abort, render_template, request, make_response, session, current_app, flash
from datetime import datetime
import sqlite3
from os import path
from db import db
from db.models import user_data, articles, favorites, offices
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, login_required, current_user, logout_user

lab8 = Blueprint('lab8', __name__)
@lab8.context_processor
def inject_current_lab():
    return {'current_lab': '/lab8/'}

@lab8.route('/lab8/')
def lab():
    return render_template('lab8/lab8.html', login=session.get('login'))

@lab8.route('/lab8/register/', methods = ['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab8/register.html')
    login_form = request.form.get('login')
    password_form = request.form.get('password')
    if not login_form:
        return render_template('lab8/register.html', error='Имя пользователя не должно быть пустым')
    if not password_form:
        return render_template('lab8/register.html', error='Пароль не должен быть пустым')
    login_exists = user_data.query.filter_by(login=login_form).first()
    if login_exists:
        return render_template('lab8/register.html', error='Такой пользователь уже существует')
    password_hash = generate_password_hash(password_form)
    new_user = user_data(login=login_form, password=password_hash)
    db.session.add(new_user)
    db.session.commit()

    login_user(new_user, remember=False)
    
    return redirect('/lab8/')

@lab8.route('/lab8/login/', methods = ['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab8/login.html')
    login_form = request.form.get('login')
    password_form = request.form.get('password')
    remember_me = request.form.get('remember_me')
    user = user_data.query.filter_by(login = login_form).first()
    if user:
        if check_password_hash(user.password, password_form):
            login_user(user, remember=remember_me == 'on')
            return redirect('/lab8/')
    return render_template('/lab8/login.html', error = "Ошибка входа: логин и/или пароль неверны")

@lab8.route('/lab8/articles/')
@login_required
def article_list():
    user_articles = articles.query.filter_by(user_id=current_user.id).all()
    return render_template('lab8/articles.html', articles=user_articles)

@lab8.route('/lab8/create', methods=['GET', 'POST'])
@login_required
def create_article():
    if request.method == 'GET':
        return render_template('lab8/create.html')
    
    title = request.form.get('title')
    article_text = request.form.get('article_text')
    
    if not title or not article_text:
        return render_template('lab8/create.html', error='Заголовок и текст статьи не могут быть пустыми')
    
    new_article = articles(title=title, article_text=article_text, user_id=current_user.id)
    db.session.add(new_article)
    db.session.commit()
    
    return redirect('/lab8/articles')

@lab8.route('/lab8/edit/<int:article_id>', methods=['GET', 'POST'])
@login_required
def edit_article(article_id):
    article = articles.query.get_or_404(article_id)
    
    if article.user_id != current_user.id:
        abort(403)
    
    if request.method == 'GET':
        return render_template('lab8/edit.html', article=article)
    
    title = request.form.get('title')
    article_text = request.form.get('article_text')
    
    if not title or not article_text:
        return render_template('lab8/edit.html', article=article, error='Заголовок и текст статьи не могут быть пустыми')
    
    article.title = title
    article.article_text = article_text
    db.session.commit()
    
    return redirect('/lab8/articles')

@lab8.route('/lab8/delete/<int:article_id>', methods=['POST'])
@login_required
def delete_article(article_id):
    article = articles.query.get_or_404(article_id)
    
    if article.user_id != current_user.id:
        abort(403)
    
    db.session.delete(article)
    db.session.commit()
    
    return redirect('/lab8/articles')

@lab8.route('/lab8/logout')
@login_required
def logout():
    logout_user()
    return redirect('/lab8/')