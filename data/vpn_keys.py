from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey

from datetime import datetime

from data.db_session import SqlAlchemyBase


class VpnKey(SqlAlchemyBase):

    __tablename__ = "vpn_keys"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    key_name = Column(String)

    vpn_key = Column(String)

    client_id = Column(String)

    created_date = Column(
        DateTime,
        default=datetime.utcnow
    )