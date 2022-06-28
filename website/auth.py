from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from .models import User, Company
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy import select
import datetime

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_Name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email is already used.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 4 characters.', category='error')
        elif len(first_Name) < 2:
            flash('First name must be greater than 1 characters.', category='error')
        elif password1 != password2:
            flash('Passwords need to match', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = User(email=email, first_Name=first_Name, password=generate_password_hash(
                password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)


@auth.route('/', methods=['GET', 'POST'])
@login_required
def search():
    if request.method == "POST":
        searchPhrase = request.form.get('search')
        sql = select(Company).where(Company.companyName == searchPhrase)
        result = db.session.execute(sql)

        return render_template("search.html", records=result.scalars().all())
    return render_template('home.html', user=current_user)


@auth.route('/e_register')
@login_required
def enterpriseRegister():
    return render_template("e_register.html", user=current_user)


@auth.route('/establishment', methods=['GET', 'POST'])
@login_required
def establishment():
    if request.method == 'POST':
        companyName = request.form.get('companyName')
        registryCode = request.form.get('registryCode')
        registrationDate = request.form.get('registrationDate')
        capital = request.form.get(str('capital'))
        format = '%Y-%m-%d'
        dateobject = datetime.datetime.strptime(registrationDate, format)

        companyname = Company.query.filter_by(
            companyName=companyName).first()
        registrycode = Company.query.filter_by(
            registryCode=registryCode).first()

        if companyname:
            flash('Company name is taken.', category='error')
        elif registrycode:
            flash('Registry code is already used.', category='error')
        elif len(companyName) < 3 or len(companyName) > 100:
            flash('Company name must be between 3 and 100 characters.',
                  category='error')
        elif len(registryCode) != 7:
            flash('Registry Code needs to be 7 characters', category='error')
        else:
            newCompany = Company(companyName=companyName,
                                 registryCode=registryCode,
                                 registrationDate=dateobject.date(),
                                 capital=capital)
            db.session.add(newCompany)
            db.session.commit()
            flash('Company was created!', category='success')
            return redirect(url_for('views.companydata', id=newCompany.id))

    return render_template("establishment.html", user=current_user)
