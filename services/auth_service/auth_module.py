import re
from flask import render_template, request, url_for, flash, redirect

from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import app, db, Post, User

def register_():
    pattern =r"(^[a-zA-Z]+$)"
    if request.method == 'POST':
        if re.search(pattern, request.form['username']):
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']
            existing_user = User.query.filter_by(username=username).first()
            existing_email = User.query.filter_by(email=email).first()
            if existing_user:
                flash('Пользователь с таким именем уже существует', category='error')
                return redirect(url_for('register'))
            if existing_email:
                flash('Пользователь с таким email уже существует', category='error')
                return redirect(url_for('register'))
            hashed_password = generate_password_hash(password)
            new_user = User(username=username, email=email, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))
        else:
            flash('Имя должно состоять только из латинских букв', 'error')
    return render_template('register.html')
