#!/usr/bin/python3
""" This module defines the lessonLog class """
import models
from models.base_model import BaseModel, Base

from os import getenv
from datetime import datetime
from sqlalchemy import Column, String, ForeignKey, DateTime

time = "%Y/%m/%d %H:%M"


class LessonLog(BaseModel, Base):
    """
    This class defines a lesson log by its attributes
    Attributes:
        student_id (str): id of student associated with the lesson log
        user_id (str): id of user who is managing the lesson log
        plan (str): Detailed description of what is to be covered in the
                           lesson
        comments (str): Comments on how the lesson went and any interesting
                        thing you noticed about the student's technique
        homework(str): Any homework assigned, if any
    """

    if models.storage_t == 'db':
        __tablename__ = "lessonlogs"
        student_id = Column(String(60), ForeignKey("students.id"),
                            nullable=False)
        user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
        plan = Column(String(1024), nullable=True)
        comments = Column(String(1024), nullable=True)
        homework = Column(String(1024), nullable=True)
        lesson_time = (Column(DateTime, default=datetime.now))
        location = Column(String(1024), nullable=True)
    else:
        student_id = ""
        user_id = ""
        plan = ""
        comments = ""
        homework = ""
        location = ""
        lesson_time = ""

    def __init__(self, *args, **kwargs):
        """Initialize new Lesson log"""
        super().__init__(*args, **kwargs)

    def __str__(self):
        """Return a string representation of a lesson log"""
        return "[{}] ({}) {} {} {} {} {}".format(self.__class__.__name__,
                                                 self.id, self.lesson_time,
                                                 self.location, self.plan,
                                                 self.comments, self.homework)

    def to_dict(self):
        """Return a dict representation of a lesson log"""
        new_dict = super().to_dict()
        new_dict["student_id"] = self.student_id
        new_dict["user_id"] = self.user_id
        new_dict["plan"] = self.plan
        new_dict["comments"] = self.comments
        new_dict["homework"] = self.homework
        if self.lesson_time:
            new_dict["lesson_time"] = self.lesson_time.strftime(time)
        else:
            new_dict["lesson_time"] = "Y/m/d H:M"
        new_dict["location"] = self.location
        return new_dict

    if models.storage_t != "db":
        @property
        def lesson_time(self):
            """Return value for lesson_time attribute
            """
            return self.lesson_time

        @lesson_time.setter
        def lesson_time(self, value):
            """Create lesson time datetime object from given values
               format for datetime object: %Y/%m/%d H:M
            """
            self.lesson_time = datetime.strptime(value, time)
