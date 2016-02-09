from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    Unicode,
    UnicodeText,
    DateTime
    )

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )

from zope.sqlalchemy import ZopeTransactionExtension

from datetime import datetime as time

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class MyModel(Base):
    __tablename__ = 'models'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    value = Column(Integer)

Index('my_index', MyModel.name, unique=True, mysql_length=255)

class Entry(Base):
    # Name database table "entries
    __tablename__ = 'entries'

    # Primary key field
    id = Column('id', Integer, primary_key=True)

    # Create a 'title' field that accepts unicode text  up to 255 characters in length.
    # The title must be unique and it should be impossible to save an entry without a title.
    title = Column('title', Unicode(255), nullable=False)

    # Create a 'body' field which accepts unicode text of any length (including none).
    body = Column('body', UnicodeText, nullable=True)

    # Create a 'created' field which stores the date and time the object was created.
    created = Column('created', DateTime, default=time.utcnow())

    # Create an 'edited' field which stores the UTC date and time the object was updated.
    edited = Column('edited', DateTime, default=time.utcnow(), onupdate=time.utcnow)

    @classmethod
    def all(cls):
        """
        :return: All the entries in the database, ordered so that the most recent entry is first.
        """
        return DBSession.query(cls).order_by(cls.created.desc()).all()


    @classmethod
    def b_id(cls, id):
        """
        :param id: Identifier of the Entry object
        :return: Returns the Entry object associated with the given identifier.
        """
        return DBSession.query(cls).get(id)
