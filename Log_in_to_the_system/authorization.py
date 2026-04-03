from flask import render_template, redirect, Blueprint  # основной модуль
from flask_wtf import FlaskForm # для удобства создания форм
from wtforms import StringField, EmailField, PasswordField, SubmitField  # для удобства создания форм
from wtforms.validators import DataRequired, Length  # для валидации
from wtforms.validators import Email  # для валидации
from data import db_session, user  # для дб

auth = Blueprint("authorization", __name__)

class AuthorizationForm(FlaskForm):
    """Формочка для АВТОРИЗАЦИИ пользователей"""
    name = StringField(validators=[DataRequired(), Length(min=7)])
    email = EmailField(validators=[DataRequired(), Email()])
    password = PasswordField(validators=[DataRequired(), Length(min=12)])
    submit = SubmitField("Войти")


@auth.route("/authorization", methods=["GET", "POST"])
def authorization_func():
    """авторизация пользователей"""
    form = AuthorizationForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        existing_user = db_sess.query(user.User).filter(user.User.email == form.email.data, user.User.hashed_password == form.password.data).first()
        if existing_user:
            return render_template("authorization.html", message="Пользователь с таким email уже существует", form=form)
        return redirect("/main_menu")
    return render_template("authorization.html", form=form)