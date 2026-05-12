from flask import Blueprint
from flask import render_template
from flask import redirect

from flask_login import login_required
from flask_login import current_user

from flask_wtf import FlaskForm

from wtforms import StringField
from wtforms import EmailField
from wtforms import PasswordField
from wtforms import BooleanField
from wtforms import SubmitField

from wtforms.validators import DataRequired
from wtforms.validators import Length
from wtforms.validators import Email
from wtforms.validators import Optional

from data import db_session
from data import user


edit_profile_blueprint = Blueprint(
    "edit_profile",
    __name__
)


class EditProfileForm(FlaskForm):

    change_name = BooleanField("Изменить имя")

    change_email = BooleanField("Изменить email")

    change_password = BooleanField("Изменить пароль")

    new_name = StringField(
        validators=[
            Optional(),
            Length(min=7)
        ]
    )

    new_email = EmailField(
        validators=[
            Optional(),
            Email()
        ]
    )

    new_password = PasswordField(
        validators=[
            Optional(),
            Length(min=12)
        ]
    )

    submit = SubmitField("Подтвердить изменения")


@edit_profile_blueprint.route(
    "/edit_profile",
    methods=["GET", "POST"]
)
@login_required
def edit_profile():

    form = EditProfileForm()

    if form.validate_on_submit():

        db_sess = db_session.create_session()

        current_db_user = db_sess.get(
            user.User,
            current_user.id
        )

        # Проверка имени

        if form.change_name.data:

            if not form.new_name.data:

                return render_template(
                    "edit_profile.html",
                    form=form,
                    message="Введите новое имя"
                )

            current_db_user.name = form.new_name.data

        # Проверка email

        if form.change_email.data:

            if not form.new_email.data:

                return render_template(
                    "edit_profile.html",
                    form=form,
                    message="Введите новый email"
                )

            current_db_user.email = form.new_email.data

        # Проверка пароля

        if form.change_password.data:

            if not form.new_password.data:

                return render_template(
                    "edit_profile.html",
                    form=form,
                    message="Введите новый пароль"
                )

            current_db_user.hashed_password = form.new_password.data

        db_sess.commit()

        return redirect("/main_menu")

    return render_template(
        "edit_profile.html",
        form=form
    )