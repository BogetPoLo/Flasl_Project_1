import datetime
import sqlalchemy

from flask_login import UserMixin

from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase, UserMixin):
    """
    Таблица пользователей
    """

    __tablename__ = "users"

    id = sqlalchemy.Column(
        sqlalchemy.Integer,
        primary_key=True,
        autoincrement=True
    )

    name = sqlalchemy.Column(
        sqlalchemy.String,
        nullable=False
    )

    hashed_password = sqlalchemy.Column(
        sqlalchemy.String,
        nullable=False
    )

    email = sqlalchemy.Column(
        sqlalchemy.String,
        nullable=False,
        unique=True
    )

    created_data = sqlalchemy.Column(
        sqlalchemy.DateTime,
        default=datetime.datetime.now
    )