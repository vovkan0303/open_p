import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import orm

from werkzeug.security import generate_password_hash, check_password_hash
from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    surname = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    age = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    position = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    speciality = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    address = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String, index=True, unique=True, nullable=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    avatarka = sqlalchemy.Column(sqlalchemy.String, nullable=True, default='0')
    avatarka_svoya = sqlalchemy.Column(sqlalchemy.BLOB, nullable=True)
    balance = sqlalchemy.Column(sqlalchemy.String, nullable=True, default='0')
    sk_1 = sqlalchemy.Column(sqlalchemy.String, nullable=True, default='0')
    sk_2 = sqlalchemy.Column(sqlalchemy.String, nullable=True, default='0')
    sk_3 = sqlalchemy.Column(sqlalchemy.String, nullable=True, default='0')
    sk_4 = sqlalchemy.Column(sqlalchemy.String, nullable=True, default='0')
    sk_5 = sqlalchemy.Column(sqlalchemy.String, nullable=True, default='0')
    sk_6 = sqlalchemy.Column(sqlalchemy.String, nullable=True, default='0')
    sk_7 = sqlalchemy.Column(sqlalchemy.String, nullable=True, default='0')
    sk_8 = sqlalchemy.Column(sqlalchemy.String, nullable=True, default='0')
    sk_9 = sqlalchemy.Column(sqlalchemy.String, nullable=True, default='0')
    sk_10 = sqlalchemy.Column(sqlalchemy.String, nullable=True, default='0')
    sk_11 = sqlalchemy.Column(sqlalchemy.String, nullable=True, default='0')
    sk_12 = sqlalchemy.Column(sqlalchemy.String, nullable=True, default='0')
    sk_13 = sqlalchemy.Column(sqlalchemy.String, nullable=True, default='0')
    sk_14 = sqlalchemy.Column(sqlalchemy.String, nullable=True, default='0')
    sk_15 = sqlalchemy.Column(sqlalchemy.String, nullable=True, default='0')
    sk_16 = sqlalchemy.Column(sqlalchemy.String, nullable=True, default='0')
    sk_17 = sqlalchemy.Column(sqlalchemy.String, nullable=True, default='0')
    sk_18 = sqlalchemy.Column(sqlalchemy.String, nullable=True, default='0')
    sk_19 = sqlalchemy.Column(sqlalchemy.String, nullable=True, default='0')
    sk_20 = sqlalchemy.Column(sqlalchemy.String, nullable=True, default='0')
    sk_21 = sqlalchemy.Column(sqlalchemy.String, nullable=True, default='0')
    sk_22 = sqlalchemy.Column(sqlalchemy.String, nullable=True, default='0')
    sk_26 = sqlalchemy.Column(sqlalchemy.String, nullable=True, default='0')

    def __repr__(self):
        return f'Пользователь с айди {self.id} {self.surname} {self.name}'

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

