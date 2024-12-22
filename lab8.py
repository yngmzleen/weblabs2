from flask import Blueprint, url_for, redirect, abort, render_template, request, make_response, session, current_app, flash
from datetime import datetime
import sqlite3
from os import path

lab8 = Blueprint('lab8', __name__)
@lab8.context_processor
def inject_current_lab():
    return {'current_lab': '/lab8/'}

@lab8.route('/lab8/')
def lab():
    return render_template('lab8/lab8.html', login=session.get('login'))