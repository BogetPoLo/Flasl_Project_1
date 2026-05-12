from flask import render_template
from flask import redirect
from flask import Blueprint

from flask_wtf import FlaskForm

from wtforms import StringField
from wtforms import EmailField
from wtforms import PasswordField
from wtforms import SubmitField

from wtforms.validators import DataRequired
from wtforms.validators import Length
from wtforms.validators import Email

from data import db_session
from data import user


reg = Blueprint("registration", __name__)


class RegistrationForm(FlaskForm):
    """
    Формочка для регистрации
    """

    name = StringField(
        validators=[
            DataRequired(),
            Length(min=7)
        ]
    )

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

    submit = SubmitField("Зарегистрироваться")


@reg.route("/registration", methods=["GET", "POST"])
def registration_func():
    """
    Регистрация пользователей
    """

    form = RegistrationForm()

    if form.validate_on_submit():

        db_sess = db_session.create_session()

        check_name = db_sess.query(user.User).filter(
            user.User.name == form.name.data
        ).first()

        if check_name:

            return render_template(
                "registration.html",
                message="Пользователь с таким именем уже существует",
                form=form
            )

        check_email = db_sess.query(user.User).filter(
            user.User.email == form.email.data
        ).first()

        if check_email:

            return render_template(
                "registration.html",
                message="Пользователь с таким email уже существует",
                form=form
            )

        new_user = user.User(
            name=form.name.data,
            hashed_password=form.password.data,
            email=form.email.data
        )

        db_sess.add(new_user)

        db_sess.commit()

        return redirect("/authorization")

    return render_template(
        "registration.html",
        form=form
    )