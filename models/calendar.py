#!/usr/bin/python3
""" This module defines the Calendar class for scheduling lessons """
import models
from models.base_model import BaseModel, Base
from models.student import Student
from models.log import LessonLog

from datetime import datetime
from os import getenv
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship, backref

time = "%Y/%m/%d %H:%M"


class Detail(BaseModel, Base):
    """Hold details of each lesson entry"""
    if models.storage_t == "db":
        __tablename__ = "details"
        slot = Column(String(60), nullable=False)
        lesson_id = Column(String(60), ForeignKey("lessonlogs.id"),
                           nullable=False)
        student_id = Column(String(60), ForeignKey("students.id"),
                            nullable=False)
        calendar_id = Column(String(60), ForeignKey("calendars.id"),
                             nullable=False)


class Calendar(BaseModel, Base):
    """
    This class stores the lesson slots per student for a user.
    Each user has a calendar object to store his scheduled lessons
    Attributes:
        lessons (dict): Dictionary containing scheduled lessons for a student
    """

    if models.storage_t == "db":
        __tablename__ = "calendars"
        details = relationship("Detail", backref="calendar")
        user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
        user = relationship("User", backref=backref("calendar", uselist=False))
    else:
        lessons = {}
        user_id = ""

    def __init__(self, *args, **kwargs):
        """Initializes a calendar object"""
        super().__init__(*args, **kwargs)

    def create_lessons(self):
        """Create dict lessons when using database storage"""
        if models.storage_t == "db":
            lessons = {}
            my_lessons = models.storage.all(Detail).values()
            for ml in my_lessons:
                if ml.calendar_id == self.id:
                    lessons[ml.slot] = [ml.student_id, ml.lesson_id]
            return lessons

    def is_available(self, date_time):
        """
        Checks whether a requested date and time slot is available or not.
        Argument should be in %d/%m/%Y %H:%M format.
        Returns a datetime object if the slot is available.
        """
        slot = datetime.strptime(date_time, time)
        if models.storage_t == "db":
            lessons = self.create_lessons()
        else:
            lessons = self.lessons
        if slot not in lessons.keys():
            return slot

    def schedule_lesson(self, student_id, lesson_log_id, date_time,
                        duration=None):
        """
        Schedules a lesson for a user and their selected student
        Attributes:
            student_id (str): id of student to schedule lesson for
            lesson_log_id (str): id of lesson log for lesson to be scheduled
            date_time (str): time to slot in lesson.
                             argument should be in %d/%m/%Y %H:%M format
            duration (strargument should be in minutes
        """
        slot = self.is_available(date_time)
        if slot:
            if models.storage_t != "db":
                self.lessons[slot] = [student_id, lesson_log_id]
            else:
                new_lesson = Detail()
                new_lesson.slot = slot
                new_lesson.lesson_id = lesson_log_id
                new_lesson.student_id = student_id
                new_lesson.calendar_id = self.id
                new_lesson.save()
            return True
        else:
            print("Slot not available.")
            return False

    def display_calendar(self):
        """Display a user's schedule"""
        if models.storage_t == "db":
            lessons = self.create_lessons()
        else:
            lessons = self.lessons
        if len(lessons) > 0:
            ss = {}
            for k, v in lessons.items():
                student = models.storage.get("Student", v[0])
                lesson_log = models.storage.get("LessonLog", v[1])
                s = "[{}]: {} {}\t{}".format(k, student.first_name,
                                             student.last_name, str(lesson_log))
                fullname = student.first_name + " " + student.last_name
                ss[k] = [fullname, lesson_log]
                print(s)
            return ss

    def to_dict(self):
        """Returns a dictionary representation of a calendar object"""
        time2 = "%Y-%m-%dT%H:%M:%S.%f"
        new_dict = super().to_dict()
        lesson_dict = {}
        if models.storage_t == "db":
            lessons = self.create_lessons()
        else:
            lessons = self.lessons
        for key, value in lessons.items():
            k = key.strftime(time2)
            lesson_dict[k] = value
        new_dict["lessons"] = lesson_dict

        return new_dict
