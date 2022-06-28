from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from .models import Company
from . import db
from sqlalchemy import select


views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == "POST":
        searchPhrase = request.form.get('search')
        companyNameLikePhrase = "%{}%".format(searchPhrase)
        companiesByName = Company.query.filter(
            Company.companyName.like(companyNameLikePhrase)).all()
        companiesByCode = Company.query.filter(
            Company.registryCode == searchPhrase).all()
        if len(companiesByName) > 0:
            searchingcompanies = companiesByName
        else:
            searchingcompanies = companiesByCode
        return render_template("home.html", user=current_user,
                               companies=searchingcompanies)
    else:
        return render_template("home.html", user=current_user)


@views.route('/e_register')
@login_required
def e_register():
    companies = Company.query.all()
    return render_template("e_register.html", companies=companies, user=current_user)


@views.route('/companydata/<id>')
@login_required
def companydata(id):
    company = Company.query.get(id)
    return render_template("companydata.html", company=company, user=current_user)
