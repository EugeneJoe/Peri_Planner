#!/usr/bin/python3
"""
Contains the TestUserDocs classes
"""

from datetime import datetime
import inspect
import models
from models import user, student
from models.base_model import BaseModel
import pep8
import unittest
User = user.User
Student = student.Student


class TestUserDocs(unittest.TestCase):
    """Tests to check the documentation and style of Student class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.student_f = inspect.getmembers(Student, inspect.isfunction)

    def test_pep8_conformance_student(self):
        """Test that models/student.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/student.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_student(self):
        """Test that tests/test_models/test_student.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_student.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_student_module_docstring(self):
        """Test for the student.py module docstring"""
        self.assertIsNot(student.__doc__, None,
                         "student.py needs a docstring")
        self.assertTrue(len(student.__doc__) >= 1,
                        "student.py needs a docstring")

    def test_student_class_docstring(self):
        """Test for the City class docstring"""
        self.assertIsNot(Student.__doc__, None,
                         "Student class needs a docstring")
        self.assertTrue(len(Student.__doc__) >= 1,
                        "Student class needs a docstring")

    def test_user_func_docstrings(self):
        """Test for the presence of docstrings in Student methods"""
        for func in self.student_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestStudent(unittest.TestCase):
    """Test the Student class"""
    def test_is_subclass(self):
        """Test that Student is a subclass of BaseModel"""
        user = User()
        user_details = {"user_id": user.id, "first_name": "Joe"}
        student = Student(**user_details)
        self.assertIsInstance(student, BaseModel)
        self.assertTrue(hasattr(student, "id"))
        self.assertTrue(hasattr(student, "created_at"))
        self.assertTrue(hasattr(student, "updated_at"))
        self.assertTrue(hasattr(student, "user_id"))

    def test_first_name_attr(self):
        """Test that Student has attr first_name"""
        user = User()
        user_details = {"student_id": user.id, "first_name": "Joe"}
        student = Student(**user_details)
        self.assertTrue(hasattr(student, "first_name"))
        if models.storage_t == 'db':
            self.assertEqual(student.first_name, "Joe")
        else:
            self.assertEqual(student.first_name, "Joe")

    def test_last_name_attr(self):
        """Test that Student has attr last_name, and it's an empty string"""
        user = User()
        user_details = {"student_id": user.id, "first_name": "Joe"}
        student = Student(**user_details)
        self.assertTrue(hasattr(student, "last_name"))
        if models.storage_t == 'db':
            self.assertEqual(student.last_name, None)
        else:
            self.assertEqual(student.last_name, "")

    def test_activity_attr(self):
        """Test that Student has attr activity, and it's an empty string"""
        user = User()
        user_details = {"student_id": user.id, "first_name": "Joe"}
        student = Student(**user_details)
        self.assertTrue(hasattr(student, "activity"))
        if models.storage_t == 'db':
            self.assertEqual(student.activity, None)
        else:
            self.assertEqual(student.activity, "")

    def test_to_dict_creates_dict(self):
        """test to_dict method creates a dictionary with proper attrs"""
        user = User()
        user_details = {"student_id": user.id, "first_name": "Joe"}
        u = Student(**user_details)
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
        u = Student(**user_details)
        new_d = u.to_dict()
        self.assertEqual(new_d["__class__"], "Student")
        self.assertEqual(type(new_d["created_at"]), str)
        self.assertEqual(type(new_d["updated_at"]), str)
        self.assertEqual(new_d["created_at"], u.created_at.strftime(t_format))
        self.assertEqual(new_d["updated_at"], u.updated_at.strftime(t_format))

    def test_str(self):
        """test that the str method has the correct output"""
        user = User()
        user_details = {"student_id": user.id, "first_name": "Joe"}
        student = Student(**user_details)
        string = "[Student] ({}) {}".format(student.id, student.to_dict())
        self.assertEqual(string, str(student))
