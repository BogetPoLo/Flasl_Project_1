from flask import Flask, render_template, redirect  # основной модуль
from data import db_session, user  # для дб
from flask_login import LoginManager  # для регистрации
from flask_wtf import FlaskForm  # для удобства создания форм
from wtforms import StringField, EmailField, PasswordField, SubmitField  # для удобства создания форм
from wtforms.validators import DataRequired, Length  # для валидации
from wtforms.validators import Email  # для валидации
from Log_in_to_the_system import registration, authorization

app = Flask(__name__)
# ! сделай норм защиту
app.config['SECRET_KEY'] = "сделай нормальный ключ и перенеси его в другой файл"

app.register_blueprint(registration.reg)
app.register_blueprint(authorization.auth)

# нужно для регистрации пользователя
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.get(user.User, user_id)


@app.route("/mail_memu")
def main_menu():
    """Главное меню"""
    return render_template("main_menu.html")


def main():
    # ! Придумай другое название базы данных
    db_session.global_init("db/blogs.db")
    app.run()


if __name__ == '__main__':
    main()
