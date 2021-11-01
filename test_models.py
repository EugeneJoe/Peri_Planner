#!/usr/bin/python3
import models
from models import storage
from models.user import User
from models.student import Student
from models.log import LessonLog
from models.calendar import Calendar

user_1 = User(first_name="Joe", last_name="Mwiti", activity="Trumpet",
              email="jj@gmail.com", password="jjmm")
user_1.save()
calendar_1 = Calendar(user_id=user_1.id)
calendar_1.save()
student_1 = Student(first_name="Jess", last_name="Njeri", activity="Trumpet",
                    user_id=user_1.id)
student_1.save()
lesson_1 = LessonLog(plan="Breath Control excercises", user_id=user_1.id,
                     student_id=student_1.id)
lesson_1.save()
print(user_1.id)
print(calendar_1.user_id)
calendar = user_1.calendar
ss = calendar.schedule_lesson(student_1.id, lesson_1.id, "23/10/2021 4:30")
print(ss)
