#!/usr/bin/python3

from models import storage
from models.user import User
from models.student import Student
from models.log import LessonLog
from models.calendar import Calendar

user_id = "3a071aee-985c-4c20-bc30-915b3a886a99"
student_id = "875d2368-0666-421b-9229-a0ca0023ecc7"

user = storage.get(User, user_id)
sss = user.students
for ss in sss:
    print(ss)
print("------------------------")
student = storage.get(Student, student_id)
print(student)

#for ss in student.lesson_logs:
#    print(ss)
