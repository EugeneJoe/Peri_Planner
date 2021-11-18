#!/usr/bin/python3
"""This module defines a class User"""
import sqlalchemy
from os import getenv
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

import models
from models.base_model import BaseModel, Base
from models.calendar import Calendar
from models.student import Student


class User(BaseModel, Base):
    """
    This class defines a user by various attributes

    Attributes:
        first_name (str): user's first name
        last_name (str): user's last name
        activity (str): user's instrument or activity e.g. a sport or language
        email (str): user's email address
    """
    if models.storage_t == 'db':
        __tablename__ = 'users'
        first_name = Column(String(128), nullable=False)
        last_name = Column(String(128), nullable=True)
        activity = Column(String(128), nullable=False)
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
    else:
        first_name = ""
        last_name = ""
        activity = ""
        email = ""
        password = ""

    def __init__(self, *args, **kwargs):
        """Initialize user"""
        super().__init__(*args, **kwargs)
        if self.first_name and self.last_name:
            self.full_name = self.first_name + " " + self.last_name

    def schedule(self):
        """Return a user's schedule"""
        from models import storage
        try:
            students = self.students
            schedule = []
            for student in students:
                lessons = student.lesson_logs
                if student.first_name and student.last_name:
                    full_name = student.first_name + ' ' + student.last_name
                else:
                    full_name = student.first_name
                for lesson in lessons:
                    if lesson.lesson_time:
                        schedule.append([lesson.lesson_time,
                                         full_name, student.id])
            #my_calendar = self.calendar()
            #lessons = my_calendar.to_dict()["lessons"]
            return schedule
        except:
            return None

    if models.storage_t != 'db':
        @property
        def students(self):
            """Return list of students taught by the user"""
            from models import storage
            students = storage.all("Student")
            student_list = []
            for v in students.values():
                if v.user_id == self.id:
                    student_list.append(v)
            return student_list

        @property
        def calendar(self):
            """Return the calendar for this user"""
            from models import storage
            calendars = storage.all("Calendar")
            for cal in calendars.values():
                if cal.user_id == self.id:
                    return cal
