#!/usr/bin/python3
"""
Contains the TestUserDocs classes
"""

from datetime import datetime
import inspect
import models
from models import user, student, log
from models.base_model import BaseModel
import pep8
import unittest
User = user.User
Student = student.Student
LessonLog = log.LessonLog


class TestUserDocs(unittest.TestCase):
    """Tests to check the documentation and style of Student class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.lessonlog_f = inspect.getmembers(LessonLog, inspect.isfunction)

    def test_pep8_conformance_lessonlog(self):
        """Test that models/log.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/log.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_log(self):
        """Test that tests/test_models/test_lesson_logs.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_lesson_logs.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_user_module_docstring(self):
        """Test for the log.py module docstring"""
        self.assertIsNot(log.__doc__, None,
                         "user.py needs a docstring")
        self.assertTrue(len(log.__doc__) >= 1,
                        "user.py needs a docstring")

    def test_user_class_docstring(self):
        """Test for the City class docstring"""
        self.assertIsNot(LessonLog.__doc__, None,
                         "User class needs a docstring")
        self.assertTrue(len(LessonLog.__doc__) >= 1,
                        "User class needs a docstring")

    def test_user_func_docstrings(self):
        """Test for the presence of docstrings in User methods"""
        for func in self.lessonlog_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestLessonLog(unittest.TestCase):
    """Test the LessonLog class"""
    def test_is_subclass(self):
        """Test that Student is a subclass of BaseModel"""
        user = User()
        user_details = {"user_id": user.id, "first_name": "Joe"}
        student = Student(**user_details)
        log_details = {"user_id": user.id, "student_id": student.id}
        log = LessonLog(**log_details)
        self.assertIsInstance(log, BaseModel)
        self.assertTrue(hasattr(log, "id"))
        self.assertTrue(hasattr(log, "created_at"))
        self.assertTrue(hasattr(log, "updated_at"))

    def test_log_attrs(self):
        """Test that Student all attrs"""
        user = User()
        user_details = {"student_id": user.id, "first_name": "Joe"}
        student = Student(**user_details)
        log_details = {"user_id": user.id, "student_id": student.id}
        log = LessonLog(**log_details)
        self.assertTrue(hasattr(log, "plan"))
        self.assertTrue(hasattr(log, "comments"))
        self.assertTrue(hasattr(log, "homework"))
        self.assertTrue(hasattr(log, "location"))
        self.assertTrue(hasattr(log, "lesson_time"))
        self.assertTrue(hasattr(log, "user_id"))
        self.assertTrue(hasattr(log, "student_id"))

    def test_to_dict_creates_dict(self):
        """test to_dict method creates a dictionary with proper attrs"""
        user = User()
        user_details = {"student_id": user.id, "first_name": "Joe"}
        student = Student(**user_details)
        log_details = {"user_id": user.id, "student_id": student.id}
        u = LessonLog(**log_details)
        new_d = u.to_dict()
        self.assertEqual(type(new_d), dict)
        self.assertFalse("_sa_instance_state" in new_d)
        for attr in u.__dict__:
            if attr is not "_sa_instance_state":
                self.assertTrue(attr in new_d)
        self.assertTrue("__class__" in new_d)

    def test_to_dict_values(self):
        """test that values in dict returned from to_dict are correct"""
        t_format = "%Y-%m-%dT%H:%M:%S.%f"
        user = User()
        user_details = {"student_id": user.id, "first_name": "Joe"}
        student = Student(**user_details)
        log_details = {"user_id": user.id, "student_id": student.id}
        u = LessonLog(**log_details)
        new_d = u.to_dict()
        self.assertEqual(new_d["__class__"], "LessonLog")
        self.assertEqual(type(new_d["created_at"]), str)
        self.assertEqual(type(new_d["updated_at"]), str)
        self.assertEqual(new_d["created_at"], u.created_at.strftime(t_format))
        self.assertEqual(new_d["updated_at"], u.updated_at.strftime(t_format))

    def test_str(self):
        """test that the str method has the correct output"""
        user = User()
        user_details = {"student_id": user.id, "first_name": "Joe"}
        student = Student(**user_details)
        log_details = {"user_id": user.id, "student_id": student.id}
        log = LessonLog(**log_details)
        string = "[LessonLog] ({}) {} {} {} {} {}".format(log.id,
                                                          log.lesson_time,
                                                          log.location,
                                                          log.plan,
                                                          log.comments,
                                                          log.homework)
        self.assertEqual(string, str(log))
