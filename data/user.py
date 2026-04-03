import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase):
    """Эта таблица нужна для регистрации новых пользователей и авторизации при входе в систему"""
    __tablename__ = "users"

    # id пользователя
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True,
                           nullable=False, unique=True)
    # имя пользователя
    name = sqlalchemy.Column(sqlalchemy.String, primary_key=False, autoincrement=False,
                             nullable=False, unique=False)
    # хешированный пароль
    hashed_password = sqlalchemy.Column(sqlalchemy.String, primary_key=False, autoincrement=False,
                                        nullable=False, unique=False)
    # email пользователя, !нужно реализовать отправку письма
    email = sqlalchemy.Column(sqlalchemy.String, primary_key=False, autoincrement=False,
                              nullable=False, unique=True)
    # дата создания аккаунта, !можно добавить ещё дополнительной интересной информации или сделать новую таблицу с такими данными
    created_data = sqlalchemy.Column(sqlalchemy.DateTime, primary_key=False, autoincrement=False,
                                     nullable=False, unique=False, default=datetime.datetime.now)