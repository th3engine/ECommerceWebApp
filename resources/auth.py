from flask import Blueprint, render_template, redirect, url_for, flash, session, request
from forms import UserLogin, RegisterUser
from flask_login import login_user, logout_user, login_required
from werkzeug.security import check_password_hash
from werkzeug.routing import BuildError
from .decorators import logout_required
from db import db, Users

bp = Blueprint("Auth",__name__)

@bp.route('/login',methods=["GET","POST"])
@logout_required
def login():
    form = UserLogin()
    if form.validate_on_submit():
        user = db.session.execute(db.select(Users).where(Users.email == form.email.data)).scalar()
        if user and check_password_hash(user.password,form.password.data):
            login_user(user)
            next = request.args.get('next','none')
            try:
                next = url_for(next)
            except BuildError:
                next = None
            return redirect(next or url_for('Home.index'))
        flash("Incorrect Credentials","danger")
        return redirect(url_for('Auth.login',next=request.args.get('next')))
    return render_template('auth/login.html',form=form)

@bp.route('/register',methods=["GET","POST"])
@logout_required
def register():
    form = RegisterUser()
    if form.validate_on_submit():
        user = db.session.execute(db.select(Users).where(Users.email == form.email.data)).scalar()
        if user:
            flash("User with this email already exists.","warning")
            return redirect(url_for('Auth.login'))
        else:
            new_user = Users(name=form.first_name.data,email=form.email.data,password=form.password.data)
            db.session.add(new_user)
            db.session.commit()
            flash("Successfully registered","info")
            login_user(new_user)
            return redirect(url_for('Profile.index'))
    return render_template('auth/register.html',form=form)

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()
    return redirect(url_for('Home.index'))