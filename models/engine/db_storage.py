#!/usr/bin/python3
"""
Contains the class DBStorage
"""

import models
from models.user import User
from models.base_model import BaseModel, Base
from models.student import Student
from models.log import LessonLog
from models.calendar import Calendar, Detail

from os import getenv
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

classes = {"User": User, "Student": Student, "LessonLog": LessonLog,
           "Detail": Detail, "Calendar": Calendar}


class DBStorage:
    """interaacts with the MySQL database"""
    __engine = None
    __session = None

    def __init__(self):
        """Instantiate a DBStorage object"""
        PERI_MYSQL_USER = getenv('PERI_MYSQL_USER')
        PERI_MYSQL_PWD = getenv('PERI_MYSQL_PWD')
        PERI_MYSQL_HOST = getenv('PERI_MYSQL_HOST')
        PERI_MYSQL_DB = getenv('PERI_MYSQL_DB')
        PERI_ENV = getenv('PERI_ENV')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(PERI_MYSQL_USER,
                                             PERI_MYSQL_PWD,
                                             PERI_MYSQL_HOST,
                                             PERI_MYSQL_DB))
        if PERI_ENV == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """query on the current database session"""
        new_dict = {}
        for clss in classes:
            if cls is None or cls is classes[clss] or cls is clss:
                objs = self.__session.query(classes[clss]).all()
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + obj.id
                    new_dict[key] = obj
        return (new_dict)

    def new(self, obj):
        """add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current database session obj if not None"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """reloads data from the database"""
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session

    def close(self):
        """call remove() method on the private session attribute"""
        self.__session.remove()

    def get(self, cls, id):
        """ Retrieve one object from storage """
        try:
            for clss in classes:
                if cls is classes[clss] or cls is clss:
                    key = "{}.{}".format(clss, id)
            obj_dict = self.all(cls)
            return obj_dict[key]
        except:
            pass

    def count(self, cls=None):
        """ Return the number of objects in storage matching the given class.
            If no class is passed,, return the count of all objects in storage.
        """
        count = 0
        if cls:
            obj_dict = self.all(cls)
        else:
            obj_dict = self.all()
        return len(obj_dict)
