from flask import Blueprint, render_template, request, redirect, session
lab4 = Blueprint('lab4', __name__)

@lab4.route('/lab4/')
def lab():
    return  render_template('lab4/lab4.html')

@lab4.route('/lab4/div-form')
def div_form():
    return  render_template('lab4/div-form.html')

@lab4.route('/lab4/div', methods = ['POST'])
def div():
    operation = request.form.get('operation')
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')

    if x1 == '' or x2 == '':
        return render_template('lab4/div.html', error='Оба поля должны быть заполнены!')

    x1 = int(x1)
    x2 = int(x2)

    if operation == 'sum':
        result = x1 + x2
    elif operation == 'mul':
        result = x1 * x2
    elif operation == 'sub':
        result = x1 - x2
    elif operation == 'pow':
        if x1 == 0 and x2 == 0:
            return render_template('lab4/div.html', error='Невозможно возвести 0 в степень 0!')
        result = x1 ** x2
    elif operation == 'div':
        if x2 == 0:
            return render_template('lab4/div.html', error='На ноль делить нельзя!')
        result = x1 / x2
    else:
        return render_template('lab4/div.html', error='Неизвестная операция!')

    return render_template('lab4/div.html', operation=operation, x1=x1, x2=x2, result=result)  

tree_count = 0

@lab4.route('/lab4/tree', methods = ['GET', 'POST'])
def tree():
    global tree_count
    if request.method == 'GET':
        return render_template('/lab4/tree.html', tree_count=tree_count)
    
    operation = request.form.get('operation')

    if operation == 'cut':
        if tree_count > 0:
            tree_count -= 1
        else:
            tree_count = 0
    elif operation == 'plant':
        if tree_count <= 10:
            tree_count += 1
        else:
            tree_count = 10
    return redirect('/lab4/tree')

users = [
    {'login': 'alex', 'password': '123','name':'алекс диджей', 'sex':'мужской'},
    {'login': 'bob', 'password': '555','name':'просто боб', 'sex':'мужской'},
    {'login': 'stopudov', 'password': '111','name':'Стопудов', 'sex':'мужской'},
    {'login': 'minecraft', 'password': '777','name':'майнкрафт_босс_2010', 'sex':'алмазные блоки'},
]

@lab4.route('/lab4/login', methods = ['GET', 'POST'])
def login():
    name = ''
    sex = ''
    last_login = session.get('last_login', '') 
    if request.method == 'GET':
        if 'login' in session:
            authorized = True
            login = session['login']
            for user in users:
                if user['login'] == login:
                    name = user['name']
                    sex = user['sex']
                    break
        else:
            authorized = False
            login = ''
        return render_template('lab4/login.html', authorized=authorized, login=login, name=name, sex=sex, last_login=last_login)
    
    login = request.form.get('login')
    password = request.form.get('password')
    session['last_login'] = login

    for user in users:
        if login == user['login'] and password == user['password']:
            session['login'] = login
            return redirect('/lab4/login')

    error = ''

    if login == '':       
        error = 'введите логин'
    elif password == '':       
        error = 'введите пароль'

    return render_template('lab4/login.html', error=error, authorized=False, last_login=last_login)

@lab4.route('/lab4/logout', methods = ['POST'])
def logout():
    session.pop('login', None)
    return redirect('/lab4/login')

@lab4.route('/lab4/fridge', methods=['GET', 'POST'])
def fridge():
    snowflakes = 0
    temperature = request.form.get('temperature', '')
    output = ''

    if request.method == 'POST':
        if temperature == '':
            output = 'Ошибка: не задана температура'
        elif int(temperature) < -12:
            output = 'Не удалось установить температуру - слишком низкое значение'
        elif int(temperature) > -1:
            output = 'Не удалось установить температуру - слишком высокое значение'
        elif -12 <= int(temperature) <= -9:
            output = f'Установлена температура {temperature}'
            snowflakes = 3
        elif -8 <= int(temperature) <= -5:
            output = f'Установлена температура {temperature}'
            snowflakes = 2
        elif -4 <= int(temperature) <= -1:
            output = f'Установлена температура {temperature}'
            snowflakes = 1

        return render_template('/lab4/fridge.html', output=output, temperature=temperature, snowflakes=snowflakes)

    return render_template('/lab4/fridge.html', output=output, temperature=temperature, snowflakes=snowflakes)

@lab4.route('/lab4/corns', methods=['GET', 'POST'])
def corns():
    error = ''
    checked = False
    sale = False
    price = 0
    corn = request.form.get('corns')
    amount = request.form.get('amount')
    
    if request.method == 'POST':
        if amount == '':
            error = 'введите количество'
        elif int(amount) <= 0:
            error = 'введите верное количество'
        elif int(amount) > 500:
            error = 'такого объёма сейчас нет в наличии.'
        elif corn == 'ячмень':
            price = 12345 * int(amount)
            checked = True
        elif corn == 'овес':
            price = 8522 * int(amount)
            checked = True
        elif corn == 'пшеница':
            price = 8722 * int(amount)
            checked = True
        elif corn == 'рожь':
            price = 14111 * int(amount)
            checked = True
    
    if amount and int(amount) > 50:
        sale = True
        if sale:
            price = price - price * 0.1
    
    return render_template('/lab4/corn.html', error=error, checked=checked, price=price, corn=corn, amount=amount, sale=sale)
