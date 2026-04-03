from flask import render_template, redirect, Blueprint  # основной модуль
from flask_wtf import FlaskForm  # для удобства создания форм
from wtforms import StringField, EmailField, PasswordField, SubmitField  # для удобства создания форм
from wtforms.validators import DataRequired, Length  # для валидации
from wtforms.validators import Email  # для валидации
from data import db_session, user  # для дб

reg = Blueprint("registration", __name__)


class RegistrationForm(FlaskForm):
    """Формочка для РЕГИСТРАЦИИ новых пользователей, подумай над дополнительными параметрами"""
    name = StringField(validators=[DataRequired(), Length(min=7)])
    email = EmailField(validators=[DataRequired(), Email()])
    password = PasswordField(validators=[DataRequired(), Length(min=12)])
    submit = SubmitField("Войти")


@reg.route("/registration", methods=["GET", "POST"])
def registration_func():
    """регистрация пользователей"""
    form = RegistrationForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        check_name = db_sess.query(user.User).filter(user.User.name == form.name.data).first()
        print(check_name)
        if check_name:
            return render_template("registration.html", message="Пользователь с таким именем уже существует", form=form)

        check_email = db_sess.query(user.User).filter(user.User.email == form.email.data).first()
        print(check_email)
        if check_email:
            return render_template("registration.html", message="Пользователь с таким email уже существует", form=form)

        new_user = user.User(name=form.name.data, hashed_password=form.password.data, email=form.email.data)
        db_sess.add(new_user)
        db_sess.commit()
        return redirect("/main_menu")
    return render_template("registration.html", form=form)
