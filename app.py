from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from gpt_prompts import get_answer_from_gpt

app = Flask(__name__)
app.secret_key = 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['UPLOAD_FOLDER'] = 'datasets'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)


@app.route('/', methods=['GET'])
def main():
    if 'username' in session:
        return render_template('index.html')
    elif 'first_visit' not in session:
        session['first_visit'] = True
        return redirect(url_for('login'))
    else:
        flash('Ви повинні спочатку увійти', 'danger')
        return redirect(url_for('login'))



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            session['username'] = user.username
            return redirect(url_for('main'))
        else:
            flash('Неправильний логін або пароль', 'danger')


    elif 'username' in session:
        return redirect(url_for('main'))

    return render_template('login.html')



@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        print(request.form)
        username = request.form['username']
        password = request.form['password']
        confirmPassword = request.form['confirmPassword']

        if password != confirmPassword:
            flash('Паролі не співпадають')
            return render_template('register.html')
        elif len(password) <6:
            flash('Пароль повинний бути більше 6 символів')
            return render_template('register.html')

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Користувач з таким ім\'ям вже існує', 'danger')
        else:
            # Создаем нового пользователя
            new_user = User(username=username, password=password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return redirect(url_for('main'))

    elif 'username' in session:
        return redirect(url_for('main'))

    return render_template('register.html')



@app.route('/api/get_answer', methods=['POST'])
def api_data():
    data = request.get_json()
    category = data.get('category')
    text = data.get('text')
    answer = get_answer_from_gpt(category, text)
    return jsonify({'status': 'ok', 'answer': answer})


@app.route('/about', methods=['GET'])
def about():
    if 'username' in session:
        return render_template('about.html')
    else:
        return redirect(url_for('main'))

@app.route('/contact', methods=['GET'])
def contact():
    if 'username' in session:
        return render_template('contact.html')
    else:
        return redirect(url_for('main'))

@app.route('/generate', methods=['GET', 'POST'])
def generate():
    if 'username' in session:
        return render_template('generate.html')
    else:
        return redirect(url_for('main'))

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
