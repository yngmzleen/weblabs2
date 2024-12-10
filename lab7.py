from flask import Blueprint, render_template, request, session, current_app, abort, request
from random import randint
import sqlite3
from os import path

lab7 = Blueprint('lab7', __name__)

@lab7.route('/lab7/')
def lab():
    return render_template('/lab7/lab7.html')

films = [
    {
        "title": "28 Days Later",
        "title_ru": "28 дней спустя",
        "year": 2002,
        "description": "Группа «зеленых» экстремистов вторгается в центр исследования приматов \
            и выпускает из секретной научной лаборатории обезьяну, зараженную вирусом неудержимой агрессии.\
            Смертельный вирус, передающийся через кровь за считанные секунды, приводит к мгновенному заражению и,\
            соприкоснувшись с любым живым существом, превращает его в кровожадного монстра."
    },
    {
        "title": "Pulp Fiction",
        "title_ru": "Криминальное чтиво",
        "year": 1994,
        "description": "Двое бандитов Винсент Вега и Джулс Винфилд ведут философские беседы в перерывах между разборками и решением проблем \
        с должниками криминального босса Марселласа Уоллеса.В первой истории Винсент проводит незабываемый вечер с женой Марселласа Мией.\
        Во второй Марселлас покупает боксёра Бутча Кулиджа, чтобы тот сдал бой. В третьей истории Винсент и Джулс по нелепой случайности попадают в неприятности."
    },
    {
        "title": "Star Wars. Episode III",
        "title_ru": "Звёздные войны. Эпизод III",
        "year": 2005,
        "description": "Идёт третий год Войн клонов. Галактическая Республика, некогда бывшая спокойным и гармоничным государством, превратилась в поле битвы между армиями клонов,\
        возглавляемых канцлером Палпатином, и армадами дроидов, которых ведёт граф Дуку, тёмный лорд ситхов. Республика медленно погружается во тьму.\
        Лишь рыцари-джедаи, защитники мира и справедливости, могут противостоять злу, которое вскоре поглотит галактику. Но настоящая битва идёт в душе у молодого рыцаря-джедая Энакина,\
        который разрывается между долгом джедая и любовью к своей жене, сенатору Падме Амидале. И от того, какое чувство в нём победит, зависит будущее всего мира."
    },
]

@lab7.route('/lab7/rest-api/films/', methods=['GET'])
def get_films():
    return films

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['GET'])
def get_film(id):
    if id >= len(films):
        return abort(404)
    else:
        return films[id]
    
@lab7.route('/lab7/rest-api/films/<int:id>', methods=['DELETE'])
def del_film(id):
    if id >= len(films):
        return abort(404)
    else:
        del films[id]
        return '', 204
    
@lab7.route('/lab7/rest-api/films/<int:id>', methods=['PUT'])
def put_film(id):
    if id >= len(films):
        return abort(404)
    else:
        film = request.get_json()
        if film['description'] == '':
            return {'description': 'Заполните описание!'}, 400
        films[id] = film
        return films[id]
    
@lab7.route('/lab7/rest-api/films/', methods=['POST'])
def add_film():
    film = request.get_json() 
    if not film or not all(k in film for k in ('title', 'title_ru', 'year', 'description')):
        return abort(400, "Invalid film data")  
    
    films.append(film) 
    return {'id': len(films) - 1}, 201  
