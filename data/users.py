import sqlalchemy
from .db_session import SqlAlchemyBase

# класс базы данных
# в нём четыре колонки
# в каждой строке записаны
# номер записи имя пользователя,
# пароль и история его поиска
# история поиска записана
# в строку, каждое слово в
# истории поиска записано в
# паре (слово + языковая семья)

# содержит 4 колонки:
# id - порядковый номер записи
# username - имя пользователя
# password - пароль пользователя


class User(SqlAlchemyBase):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    username = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    words = sqlalchemy.Column(sqlalchemy.String, nullable=True)
