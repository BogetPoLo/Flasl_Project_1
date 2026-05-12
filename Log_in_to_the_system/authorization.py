from flask import render_template
from flask import redirect
from flask import Blueprint

from flask_login import login_user

from flask_wtf import FlaskForm

from wtforms import EmailField
from wtforms import PasswordField
from wtforms import SubmitField

from wtforms.validators import DataRequired
from wtforms.validators import Length
from wtforms.validators import Email

from data import db_session
from data import user


auth = Blueprint("authorization", __name__)


class AuthorizationForm(FlaskForm):
    """
    Форма авторизации
    """

    email = EmailField(
        validators=[
            DataRequired(),
            Email()
        ]
    )

    password = PasswordField(
        validators=[
            DataRequired(),
            Length(min=12)
        ]
    )

    submit = SubmitField("Войти")


@auth.route("/authorization", methods=["GET", "POST"])
def authorization_func():
    """
    Авторизация пользователя
    """

    form = AuthorizationForm()

    if form.validate_on_submit():

        db_sess = db_session.create_session()

        existing_user = db_sess.query(user.User).filter(
            user.User.email == form.email.data,
            user.User.hashed_password == form.password.data
        ).first()

        if existing_user:

            login_user(existing_user)

            return redirect("/main_menu")

        return render_template(
            "authorization.html",
            message="Неверный email или пароль",
            form=form
        )

    return render_template(
        "authorization.html",
        form=form
    )