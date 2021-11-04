#!/usr/bin/python3
"""This module defines a Student Class"""
import sqlalchemy
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship, backref
from os import getenv

import models
from models.base_model import BaseModel, Base
from models.log import LessonLog


class Student(BaseModel, Base):
    """
    This class defines a student through various attributes

    Attributes:
        first_name (str): student's first name
        last_name (str): student's last name
        activity (str): their instrument, or sport/game they play, or language
        user_id (str): associated user's user id
        lesson_logs (list): a list of lesson log ids for lesson logs for
                            for this student
    """
    if models.storage_t == 'db':
        __tablename__ = 'students'
        first_name = Column(String(128), nullable=False)
        last_name = Column(String(128), nullable=True)
        activity = Column(String(128), nullable=True)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
        lesson_logs = relationship("LessonLog", backref="student")
        user = relationship("User", backref="students")
    else:
        first_name = ""
        last_name = ""
        activity = ""
        user_id = ""
        lesson_logs = []

    def __init__(self, *args, **kwargs):
        """Initialize a new student"""
        super().__init__(*args, **kwargs)
        if self.first_name and self.last_name:
            self.fullname = self.first_name + " " + self.last_name

    if models.storage_t != "db":
        @property
        def lesson_logs(self):
            """Getter for list of lesson logs for the student"""
            all_lessons = models.storage.all(LessonLog)
            for lesson in all_lessons.values():
                if lesson.student_id == self.id:
                    self.lesson_logs.append(lesson)
            return self.lesson_logs
