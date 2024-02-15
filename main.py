import re
from flask import render_template, request, url_for, flash, redirect

from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import app, db, Post, User
from services.auth_service import auth_module
login_manager = LoginManager(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def home():
    posts = Post.query.all()
    return render_template('home.html', posts=posts)

@app.route('/about')
def about():
    posts = Post.query.all()
    return render_template('about.html', posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Неправильное имя пользователя или пароль', 'error')
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    return auth_module.register_()
    

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        current_user.username = username
        current_user.email = email
        db.session.commit()
        flash('Ваши личные данные успешно обновлены', 'success')
        return redirect(url_for('dashboard'))
    return render_template('dashboard.html', user=current_user)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template('home.html')


@app.route('/add_post', methods=['GET', 'POST'])
def add_post():
    '''
        Функция add_post является функцией-обработчиком для маршрута `/add_post`.
        Когда вы переходите на данную страницу, то увидите шаблон из `add_post.html`
        Но когда вы попытаетесь заполнить форму какими-то данными и отправить запрос,
        то вы отправите POST запрос и создадите новый пост в БД
    '''
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        new_post = Post(title=title, content=content, author=current_user)
        db.session.add(new_post)
        db.session.commit()
        flash('Пост успешно добавлен', 'successfully')
        return redirect(url_for('home'))
    return render_template('add_post.html')

@app.route('/denis')
def denis():
    return render_template('denis.html')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)



