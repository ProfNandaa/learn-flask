# Basic models for demonstration

import datetime
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

from werkzeug.security import generate_password_hash, check_password_hash

Base = declarative_base()

# engine = create_engine('sqlite:///db/app.db')
engine = create_engine('postgresql+psycopg2://postgres:BINLAN@localhost/learnFlask')
# engine = create_engine('postgresql://scott:tiger@localhost/mydatabase')
# pg8000
# engine = create_engine('postgresql+pg8000://scott:tiger@localhost/mydatabase')
# default
# engine = create_engine('mysql://miles:password@localhost/foo')
# mysql-python
# engine = create_engine('mysql+mysqldb://miles:password@localhost/foo')
# MySQL-connector-python
# engine = create_engine('mysql+mysqlconnector://miles:password@localhost/foo')


Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(100))
    last_name = Column(String(100))
    username = Column(String(100), nullable=False)
    email = Column(String(100))  # not currently in use
    password = Column(String(100))

    def rollback(self):
        session.rollback()

    def save(self):
        # hash the password
        self.password = generate_password_hash(self.password)
        session.add(self)
        session.commit()

    def valid_password(self, password):
        return check_password_hash(self.password, password)

    @classmethod
    def validate(cls, **kwargs):
        user = session.query(cls).filter(cls.username == kwargs.get('username'))
        if user.count() == 0:
            return False, {}
        user = user.one()
        return user.valid_password(kwargs.get('password')), user

    @classmethod
    def get(cls, user_id):
        user = session.query(cls).filter(cls.id == user_id)
        if user.count() == 1:
            return user.one()
        return None


class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True)
    title = Column(String(250), nullable=False)
    body = Column(Text)
    date_time = Column(DateTime, default=datetime.datetime.utcnow)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    def rollback(self):
        session.rollback()

    def save(self, user_id):
        self.user = User.get(user_id)
        session.add(self)
        session.commit()

    @classmethod
    def get(cls, **kwargs):
        if kwargs:
            pass
        return session.query(Post).all()
