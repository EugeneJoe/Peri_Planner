#!/usr/bin/python3
"""
This module defines a storage class to save objects in json format to a file
as well as retrieve stored objects and convert them to python objects
"""

import json
from models.base_model import BaseModel
from models.user import User
from models.log import LessonLog
from models.student import Student
from models.calendar import Calendar

classes = {"BaseModel": BaseModel, "User": User, "Student": Student,
           "Calendar": Calendar, "LessonLog": LessonLog}


class FileStorage:
    """Serialize objects to JSON file and deserialize them back to objects"""

    # path to JSON file
    __file_path = "file.json"
    # dictionary to store all objects by <class name>.id
    __objects = {}

    def all(self, cls=None):
        """Returns a dictionary of all objects of the specified class.
           If no class is given, return a dictionary of all created objects
        """
        if cls is not None:
            new_dict = {}
            for k, v in self.__objects.items():
                if cls == v.__class__ or cls == v.__class__.__name__:
                    new_dict[k] = v
            return new_dict
        return self.__objects

    def new(self, obj):
        """Add new object to dict of objects with the key <obj class name>/id"""
        if obj is not None:
            key = obj.__class__.__name__ + "." + obj.id
            self.__objects[key] = obj

    def save(self):
        """Serialize dict of objects to the JSON file (path: __file_path)"""
        json_objects = {}
        for key in self.__objects:
            json_objects[key] = self.__objects[key].to_dict()
        with open(self.__file_path, mode='w', encoding='UTF-8') as f:
            json.dump(json_objects, f)

    def reload(self):
        """Deserialize JSON file to __objects"""
        try:
            with open(self.__file_path, mode='r', encoding='UTF-8') as f:
                json_objects = json.load(f)
            for k, v in json_objects.items():
                class_name = v['__class__']
                self.__objects[k] = classes[class_name](**v)
        except:
            pass

    def delete(self, obj=None):
        """Delete obj from __objects if it exists"""
        if obj is not None:
            key = obj.__class__.__name__ + '.' + obj.id
            if key in self.__objects:
                del self.__objects[key]

    def close(self):
        """Call reload() method to deserialize JSON file to objects"""
        self.reload()

    def get(self, cls, id):
        """Return the object of specified class name and id if it exists, or
           None if not found
        """
        for clss in classes:
            if cls is clss or cls is classes[clss]:
                key = "{}.{}".format(clss, id)
                if key in self.__objects:
                    return self.__objects[key]

    def count(self, cls=None):
        """Count the number of objects of a given class in storage, or
           number of all objects
        """
        all_class = classes.values()

        if not cls:
            count = 0
            for clss in all_class:
                count += len(self.all(clss).values())
        else:
            count = len(self.all().values())

        return count
