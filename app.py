from flask import Flask, url_for, redirect, render_template
from lab1 import lab1

app = Flask(__name__)
app.register_blueprint(lab1)

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
    style = url_for("static", filename = "lab1.css")
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
           </body>
           <footer>Иванов Егор Владиславович, ФБИ-22, 3 курс, 2024</footer>
        </html>''', 200

@app.route('/error/400')
def error_400():
    return 'Bad Request', 400

@app.route('/error/401')
def error_401():
    return 'Unauthorized', 401

@app.route('/error/402')
def error_402():
    return 'Payment Required', 402

@app.route('/error/403')
def error_403():
    return 'Forbidden', 403

@app.route('/error/405')
def error_405():
    return 'Method Not Allowed', 405

@app.route('/error/418')
def error_418():
    return "I'm a teapot", 418

@app.route('/trigger_error')
def trigger_error():
    return 1 / 0

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

@app.route('/lab2/a/')
def a():
    return 'ok'

@app.route('/lab2/a')
def a2():
    return 'okokokok'

flower_list = ['роза', 'тюльпан', 'незабудка', 'ромашка']

@app.route('/lab2/flowers/<int:flower_id>')
def flowers(flower_id):
    if flower_id >= len(flower_list):
        return "такого цветка нет", 404
    else:
        flower = flower_list[flower_id]
        return f'''
<!doctype html>
<html>
    <body>
    <h1>Цветок</h1>
    <p>Цветок: {flower}</p>
    <a href="/lab2/all_flowers">Все цветы</a>
    </body>
</html>
'''
    
@app.route('/lab2/add_flower/', defaults={'name': None})
@app.route('/lab2/add_flower/<name>')
def add_flower(name):
    if name is None:
        return "вы не задали имя цветка", 400
    flower_list.append(name)
    return f'''
<!doctype html>
<html>
    <body>
    <h1>Добавлен новый цветок</h1>
    <p>Название нового цветка: {name} </p>
    <p>Всего цветов: {len(flower_list)}</p>
    <p>Полный список: {flower_list}</p>
    </body>
</html>
'''

@app.route('/lab2/clear_flowers')
def clear_flowers():
    global flower_list
    flower_list = []
    return f'''
<!doctype html>
<html>
    <body>
    <h1>Список цветов очищен</h1>
    <a href="/lab2/all_flowers">Все цветы</a>
    </body>
</html>
'''

@app.route('/lab2/all_flowers')
def all_flowers():
    flower_list_html = ''.join(f'<li>{flower}</li>' for flower in flower_list)
    return f'''
<!doctype html>
<html>
    <body>
    <h1>Все цветы</h1>
    <p>Всего цветов: {len(flower_list)}</p>
    <ul>
    {flower_list_html}
    </ul>
    <a href="/lab2/all_flowers">Все цветы</a>
    </body>
</html>
'''

@app.route('/lab2/example')
def example():
    name = 'Егор Иванов'
    group = 'ФБИ-22'
    course = '3 курс'
    laba = 'Лабораторная работа 2'
    fruits = [
        {'name': 'яблоки', 'price': 100},
        {'name': 'груши', 'price': 120},
        {'name': 'апельсины', 'price': 80},
        {'name': 'мандарины', 'price': 95},
        {'name': 'манго', 'price': 321}
    ]
    return render_template('example.html', name=name, group=group, course=course, laba=laba, fruits=fruits)

@app.route('/lab2/')
def lab2():
    return render_template('lab2.html')

@app.route('/lab2/filters')
def filters():
    phrase = 'О <b>сколько</b> <u>нам</u> <i>открытий</i> чудных...'
    return render_template('filter.html', phrase=phrase)

@app.route('/lab2/calc/<int:a>/<int:b>')
def calc(a, b):
    sum_result = a + b
    sub_result = a - b
    mul_result = a * b
    div_result = a / b 
    pow_result = a ** b
    
    return f'''
<!doctype html>
<html>
    <body>
    <h1>Математические операции</h1>
    <p>Первое число: {a}</p>
    <p>Второе число: {b}</p>
    <p>{a} + {b} = {sum_result}</p>
    <p>{a} - {b} = {sub_result}</p>
    <p>{a} x {b} = {mul_result}</p>
    <p>{a} / {b} = {div_result}</p>
    <p>{a}<sup>{b}</sup> = {pow_result}</p>
    </body>
</html>
'''

@app.route('/lab2/calc/')
def calc_redirect():
    return redirect('/lab2/calc/1/1')

@app.route('/lab2/calc/<int:a>')
def calc_a_redirect(a):
    return redirect(f'/lab2/calc/{a}/1')

books = [
    {"author": "Стивен Кинг", "title": "Кэрри", "genre": "Ужасы", "pages": 199},
    {"author": "Стивен Кинг", "title": "Сияние", "genre": "Ужасы", "pages": 447},
    {"author": "Стивен Кинг", "title": "Мизери", "genre": "Триллер", "pages": 368},
    {"author": "Стивен Кинг", "title": "11/22/63", "genre": "Научная фантастика", "pages": 849},
    {"author": "Стивен Кинг", "title": "Под куполом", "genre": "Научная фантастика", "pages": 1074},
    {"author": "Стивен Кинг", "title": "Доктор Сон", "genre": "Ужасы", "pages": 531},
    {"author": "Стивен Кинг", "title": "Бегущий человек", "genre": "Научная фантастика", "pages": 310},
    {"author": "Стивен Кинг", "title": "Оно", "genre": "Ужасы", "pages": 1138},
    {"author": "Стивен Кинг", "title": "Зелёная миля", "genre": "Фэнтези", "pages": 592},
    {"author": "Стивен Кинг", "title": "Стрелок", "genre": "Фэнтези", "pages": 231}
]

@app.route('/lab2/books')
def show_books():
    return render_template('books.html', books=books)

characters = [
    {"name": "Абрамс", "description": "Рвётся в ближний бой.", "image": "abrams.png"},
    {"name": "Мираж", "description": "Совершает точные выстрелы и ловит убегающих врагов.", "image": "mirage.png"},
    {"name": "Серый Коготь", "description": "Точно стреляет издалека.", "image": "talon.png"},
    {"name": "Виндикта", "description": "Самый тихий и смертоносный снайпер.", "image": "vindicta.png"},
    {"name": "Фантом", "description": "Смертоносная охотница за головами.", "image": "wraith.png"}
]

@app.route('/lab2/deadlock')
def deadlock():
    return render_template('deadlock.html', characters=characters)