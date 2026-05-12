import datetime

import sqlalchemy

from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class VpnKey(SqlAlchemyBase):

    __tablename__ = 'vpn_keys'

    id = sqlalchemy.Column(
        sqlalchemy.Integer,
        primary_key=True,
        autoincrement=True
    )

    user_id = sqlalchemy.Column(
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey("users.id")
    )

    key_name = sqlalchemy.Column(
        sqlalchemy.String,
        nullable=False
    )

    vpn_key = sqlalchemy.Column(
        sqlalchemy.String,
        nullable=False
    )

    created_date = sqlalchemy.Column(
        sqlalchemy.DateTime,
        default=datetime.datetime.now
    )

    user = orm.relationship('User')