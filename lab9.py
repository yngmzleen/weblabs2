from flask import Blueprint, render_template, request, redirect, url_for, session

lab9 = Blueprint('lab9', __name__)

@lab9.route('/lab9/', methods=['GET', 'POST'])
def main():
    if 'congrats_text' in session and 'gift' in session and 'image' in session:
        congrats_text = session['congrats_text']
        gift = session['gift']
        image = session['image']
        return render_template('lab9/congratulation.html', congrats_text=congrats_text, gift=gift, image=image)

    if request.method == 'POST':
        name = request.form.get('name')
        return redirect(url_for('lab9.age', name=name))
    return render_template('lab9/index.html')

@lab9.route('/lab9/age', methods=['GET', 'POST'])
def age():
    name = request.args.get('name')
    if request.method == 'POST':
        age = request.form.get('age')
        return redirect(url_for('lab9.gender', name=name, age=age))
    return render_template('lab9/age.html', name=name)

@lab9.route('/lab9/gender', methods=['GET', 'POST'])
def gender():
    name = request.args.get('name')
    age = request.args.get('age')
    if request.method == 'POST':
        gender = request.form.get('gender')
        return redirect(url_for('lab9.preference', name=name, age=age, gender=gender))
    return render_template('lab9/gender.html', name=name, age=age)

@lab9.route('/lab9/preference', methods=['GET', 'POST'])
def preference():
    name = request.args.get('name')
    age = request.args.get('age')
    gender = request.args.get('gender')
    if request.method == 'POST':
        preference = request.form.get('preference')
        return redirect(url_for('lab9.final_preference', name=name, age=age, gender=gender, preference=preference))
    return render_template('lab9/preference.html', name=name, age=age, gender=gender)

@lab9.route('/lab9/final_preference', methods=['GET', 'POST'])
def final_preference():
    name = request.args.get('name')
    age = request.args.get('age')
    gender = request.args.get('gender')
    preference = request.args.get('preference')
    if request.method == 'POST':
        final_preference = request.form.get('final_preference')
        return redirect(url_for('lab9.congratulation', name=name, age=age, gender=gender, preference=preference, final_preference=final_preference))
    return render_template('lab9/final_preference.html', name=name, age=age, gender=gender, preference=preference)

@lab9.route('/lab9/congratulation')
def congratulation():
    name = request.args.get('name')
    age = request.args.get('age')
    gender = request.args.get('gender')
    preference = request.args.get('preference')
    final_preference = request.args.get('final_preference')

    if gender == 'male':
        gender_text = 'мальчик' if int(age) < 18 else 'мужчина'
        congrats_text = f"Поздравляю тебя, {name}, желаю, чтобы ты быстро вырос, был умным и успешным!"
    else:
        gender_text = 'девочка' if int(age) < 18 else 'женщина'
        congrats_text = f"Поздравляю тебя, {name}, желаю, чтобы ты быстро выросла, была умной и успешной!"

    if preference == 'tasty':
        if final_preference == 'sweet':
            gift = 'сладость'
            image = 'slad.jpg'
        else:
            gift = 'сытный подарок'
            image = 'hotdog.jpg'
    else:
        if final_preference == 'beautiful':
            gift = 'лисянчик'
            image = 'decor.png'
        else:
            gift = 'лисянчик'
            image = 'decor.png'

    session['congrats_text'] = congrats_text
    session['gift'] = gift
    session['image'] = image

    return render_template('lab9/congratulation.html', name=name, age=age, gender=gender_text, congrats_text=congrats_text, gift=gift, image=image)

@lab9.route('/lab9/reset')
def reset():
    session.pop('congrats_text', None)
    session.pop('gift', None)
    session.pop('image', None)
    return redirect(url_for('lab9.main'))