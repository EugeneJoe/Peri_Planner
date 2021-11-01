#!/usr/bin/python3
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.student import Student
from models.log import LessonLog
from models.calendar import Calendar

user_details = {"first_name": "Eugene", "last_name": "Muthui", "email": "joemuthui@rocketmail.com", "activity": "Trumpet", "password": "root"}
user1 = User(**user_details)
storage.new(user1)

student_details = {"first_name": "Lyn", "last_name": "Gathaiya",
                   "activity": "Trumpet", "user_id": user1.id}
student1 = Student(**student_details)
storage.new(student1)
calendar_details = {"user_id": user1.id}
u1_calendar = Calendar(**calendar_details)
storage.new(u1_calendar)

#user_id = "3a071aee-985c-4c20-bc30-915b3a886a99"
#student_id = "875d2368-0666-421b-9229-a0ca0023ecc7"

#user1 = storage.get(User, user_id)
#u1_calendar = user1.calendar
#student1 = storage.get(Student, student_id)

lesson_details = {"student_id": student1.id, "user_id": user1.id}
lessonlog = LessonLog(**lesson_details)
lessonlog.plan = "Work on breathing exercises and long tones"
lessonlog.comments = "Needs to work on not upsetting her embouchure just before playing"
lessonlog.homework = "Long tones: C chromatic scale, 20 seconds"
storage.new(lessonlog)

u1_calendar.schedule_lesson(student1.id, lessonlog.id, "15/10/2021 14:30")

lesson_details = {"student_id": student1.id, "user_id": user1.id}
lessonlog2 = LessonLog(**lesson_details)
lessonlog2.plan = "Sight-reading exercises"
lessonlog2.comments = "Needs to work on not upsetting her embouchure just before playing"
lessonlog2.homework = "Grade 5 scales: range: 12th speed: 80bpm"
storage.new(lessonlog2)

u1_calendar.schedule_lesson(student1.id, lessonlog2.id, "15/10/2021 15:30")

lesson_details = {"student_id": student1.id, "user_id": user1.id}
lessonlog3 = LessonLog(**lesson_details)
lessonlog3.plan = "Work on breathing exercises and long tones"
lessonlog3.comments = "Needs to work on not upsetting her embouchure just before playing"
lessonlog3.homework = "Long tones: C chromatic scale, 20 seconds"
storage.new(lessonlog3)

u1_calendar.schedule_lesson(student1.id, lessonlog3.id, "15/10/2021 16:00")

u1_calendar.display_calendar()
print("-----------------------------\n\n")
print(user1.schedule())

print("-----------------------------\n\n")
print(user1.students)

user1.save()
student1.save()
u1_calendar.save()
lessonlog.save()
lessonlog2.save()
lessonlog3.save()
