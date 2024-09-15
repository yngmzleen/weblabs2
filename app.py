from flask import Flask, url_for, redirect

app = Flask(__name__)

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
                <a href='/lab1'>Первая лабораторная</a>
           </body>
           <footer>Иванов Егор Владиславович, ФБИ-22, 3 курс, 2024</footer>
        </html>''', 200

@app.route('/lab1')
def lab1():
    style = url_for("static", filename = "lab1.css")
    return '''<!doctype html>
        <html>
        <head>
            <link rel = "stylesheet" href="''' + style +'''"
            <title>Лабораторная 1</title>
        </head>
           <body>
                <p>
                    Flask — фреймворк для создания веб-приложений на языке
                    программирования Python, использующий набор инструментов
                    Werkzeug, а также шаблонизатор Jinja2. Относится к категории так
                    называемых микрофреймворков — минималистичных каркасов
                    веб-приложений, сознательно предоставляющих лишь самые базовые возможности.
                </p>
                <a href="/">Главная страница</a>
           </body>
           <footer>Иванов Егор Владиславович, ФБИ-22, 3 курс, 2024</footer>
        </html>''', 200

@app.route('/lab1/web')
def start():
    return '''<!doctype html>
        <html>
           <body>
                <h1>web-сервер на flask</h1>
                <a href='author'>author</a>  
                <a href='/lab1/oak'>дуб</a> 
           </body>
        </html>''', 200, {
            'X-Server,': 'sample',
            'Content-type': 'text/plain; charset=utf-8'
                          }

@app.route('/lab1/author')
def author():
    name = 'Иванов Егор Владиславович'
    group = 'ФБИ-22'
    faculty = 'ФБ'

    return '''<!doctype html>
        <html>
           <body>
                <p>Студент: ''' + name + '''</p>
                <p>Группа: ''' + group + '''</p>
                <p>Факультет: ''' + faculty + '''</p>
                <a href='web'>web</a>
                <a href='/lab1/oak'>дуб</a>
           </body>
        </html>'''

@app.route('/lab1/oak')
def oak():
    path = url_for("static", filename = "oak.jpg")
    style = url_for("static", filename = "lab1.css")
    return '''
<!doctype html>
<html>
    <link rel = "stylesheet" href="''' + style +'''"
    <body>
        <h1>Дуб необходимо сажать на хорошо освещенном месте. Лучше избегать тяжелых глинистых почв или песчаных участков. Важно учесть размеры взрослого дуба и предусмотреть пространство его развития. Рекомендуемое расстояние от других деревьев или строений – 10-15 метров.</h1>
        <img src="''' + path + '''" class="oak-image">
    </body>
</html>
'''

count = 0

@app.route('/lab1/counter')
def counter():
    global count
    count += 1
    reset_link = url_for('reset_counter')
    return '''
<!doctype html>
<html>
    <body>
        Сколько раз вы сюда заходили: ''' + str(count) + '''
        <br>
        <a href="''' + reset_link + '''">Очистить счётчик</a>
    </body>
</html>
'''

@app.route('/lab1/reset_counter')
def reset_counter():
    global count
    count = 0
    return redirect(url_for('counter'))

@app.route('/lab1/info')
def info():
    return redirect('/lab1/author')

@app.route('/lab1/created')
def created():
    return '''
<!doctype html>
<html>
    <body>
        <h1>Создано успешно</h1>
        <div><i>что-то создано...</i></div>
    </body>
</html>
''', 201

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

if __name__ == '__main__':
    app.run(debug=True)