#!/usr/bin/python3
""" Starts a Flask Web Application """
from os import environ
from datetime import timedelta, datetime
from flask import Flask, render_template, request, redirect, url_for, session
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, HiddenField, DateTimeField
from wtforms.validators import DataRequired

from models import storage
from models.student import Student
from models.user import User
from models.calendar import Calendar
from models.log import LessonLog


app = Flask(__name__)
app.secret_key = ""
app.permanent_session_lifetime = timedelta(minutes=20)
time2 = "%Y-%m-%dT%H:%M:%S.%f"
# app.jinja_env.trim_blocks = True
# app.jinja_env.lstrip_blocks = True


#create forms
class NewLesson(FlaskForm):
    """Form to collect data to create new lesson log"""
    lesson_time = StringField(validators=[DataRequired()])
    location = StringField(validators=[DataRequired()])
    plan = TextAreaField("Lesson plan", validators=[DataRequired()])
    comments = TextAreaField("Lesson comments")
    homework = TextAreaField("Homework")
    std_id = HiddenField(validators=[DataRequired()])
    new_lesson = SubmitField("New Lesson Log")


class UpdateLesson(FlaskForm):
    """Form to collect data to update an existing lesson log"""
    lesson_time = StringField(validators=[DataRequired()])
    location = StringField(validators=[DataRequired()])
    plan = TextAreaField("Lesson plan", validators=[DataRequired()])
    comments = TextAreaField("Lesson comments")
    homework = TextAreaField("Homework")
    lesson_id = HiddenField(validators=[DataRequired()])
    submit = SubmitField("New Lesson Log")


class NewStudent(FlaskForm):
    """Form to collect data to create new student"""
    name = StringField(validators=[DataRequired()])
    activity = StringField(validators=[DataRequired()])
    submit = SubmitField()


class ShowLessons(FlaskForm):
    """Form to collect data to show lesson logs for a student"""
    submit = SubmitField("Lesson Logs")
    std_id = HiddenField()


def validate_user(email, password):
    """ Check given credentials against stored data to log in a user """
    print("Validating")
    users = storage.all(User).values()
    try:
        for u in users:
            if u.email == email:
                print(u.email)
                if u.password == password:
                    print("password matched")
                    return u
        return None
    except:
        return None

@app.teardown_appcontext
def close_db(error):
    """ Remove the current SQLAlchemy Session """
    storage.close()

@app.route('/login', methods=['GET', 'POST'], strict_slashes=False)
def handle_login():
    """ Handle login for existing users """
    if request.method == 'GET':
        if "user" in session:
            return redirect(url_for("handle_students"))
        return render_template('login.html')
    else:
        email = request.form["email"]
        psswrd = request.form["pwd"]
        logged_in = validate_user(email, psswrd)
        if logged_in is not None:
            session.permanent = True
            session["user"] = logged_in.id
            return redirect(url_for("handle_students"))
        else:
            return redirect(url_for("handle_login"))

@app.route('/user/students', methods=['GET', 'POST'], strict_slashes=False)
def handle_students():
    """ Web page for all students taught by a user/tutor """
    form = NewStudent()
    form2 = ShowLessons()
    if "user" in session:
        user_id = session["user"]
        user = storage.get(User, user_id)
    else:
        return redirect(url_for("handle_login"))
    if request.method == 'POST':
        if form.validate():
            name = form.name.data
            print(name)
            form.name.data = ''
            first_name = name.split(' ')[0]
            last_name = name.split(' ')[-1]
            activity = form.activity.data
            form.activity.data = ''
            std = {"first_name": first_name, "last_name": last_name,
                   "activity": activity, "user_id": user_id}
            student = Student(**std)
            student.save()
        return redirect(url_for("handle_students"))
    else:
        students = user.students
        students = sorted(students, key=lambda k: k.first_name)
        return render_template('students.html',
                               students=students, form=form, form2=form2)

@app.route('/user/student/<student_id>/lessons', methods=['GET', 'POST'],
           strict_slashes=False)
def handle_lesson_logs(student_id):
    """ Web page displaying all lesson logs for a particular student """
    form2 = ShowLessons()
    form = NewLesson()
    updateform = UpdateLesson()
    if request.method == 'POST':
        if "user" in session:
            student_id = form2.std_id.data
            form2.std_id.data = ''
            student = storage.get(Student, student_id)
            lessons = student.lesson_logs
            lessons = sorted(lessons, key=lambda k: k.created_at, reverse=True)
            return render_template('lessons.html',
                                   student=student, lessons=lessons, form=form,
                                   updateform=updateform)
        else:
            return redirect(url_for("handle_login"))
    else:
        try:
            student = storage.get(Student, student_id)
            lessons = student.lesson_logs
            lessons = sorted(lessons, key=lambda k: k.created_at, reverse=True)
            return render_template('lessons.html',
                                   student=student, lessons=lessons, form=form,
                                   updateform=updateform)
        except:
            return redirect(url_for("handle_students"))

@app.route('/user/student/lessons/new', methods=['GET', 'POST'],
           strict_slashes=False)
def handle_new_lessons():
    """ Add new lesson logs for a student """
    form = NewLesson()
    updateform = UpdateLesson()
    if form.validate_on_submit():
        if "user" in session:
            student_id = form.std_id.data
            student = storage.get(Student, student_id)
            user_id = session["user"]
            plan = form.plan.data
            comments = form.comments.data
            homework = form.homework.data
            lesson_time = form.lesson_time.data
            location = form.location.data
            lesson_details = {"user_id": user_id, "plan": plan,
                              "comments": comments,
                              "homework": homework,
                              "lesson_time": lesson_time,
                              "location": location,
                              "student_id": student_id}
            form.plan.data = ''
            form.comments.data = ''
            form.homework.data = ''
            lesson = LessonLog(**lesson_details)
            lesson.save()
            lessons = student.lesson_logs
            lessons = sorted(lessons, key=lambda k: k.created_at, reverse=True)
            return render_template('lessons.html',
                                   student=student, lessons=lessons, form=form,
                                   updateform=updateform)
        else:
            return redirect(url_for("handle_login"))
    return redirect(url_for("handle_students"))

@app.route('/user/student/lessons/<lesson_id>/update', methods=['POST', 'GET'],
           strict_slashes=False)
def handle_update_lessons(lesson_id):
    """Handle updating an existing lesson log"""
    updateform = UpdateLesson()
    form = NewLesson()
    if updateform.validate_on_submit():
        lesson_id = updateform.lesson_id.data
        lesson_time = updateform.lesson_time.data
        updateform.lesson_time.data = ''
        location = updateform.location.data
        updateform.location.data = ''
        plan = updateform.plan.data
        updateform.plan.data = ''
        comments = updateform.comments.data
        updateform.comments.data = ''
        homework = updateform.homework.data
        updateform.homework.data = ''
        lesson = storage.get(LessonLog, lesson_id)
        setattr(lesson, 'plan', plan)
        lesson.save()
        setattr(lesson, 'comments', comments)
        lesson.save()
        setattr(lesson, 'homework', homework)
        lesson.save()
        setattr(lesson, 'lesson_time', lesson_time)
        lesson.save()
        setattr(lesson, 'location', location)
        lesson.save()
        student = storage.get(Student, lesson.student_id)
        lessons = student.lesson_logs
        lessons = sorted(lessons, key=lambda k: k.created_at)
        form.plan.data = ''
        form.comments.data = ''
        form.homework.data = ''
        return render_template('lessons.html',
                               student=student, lessons=lessons, form=form,
                               updateform=updateform)
    else:
        updateform = UpdateLesson()
        lesson = storage.get(LessonLog, lesson_id)
        updateform.lesson_time.data = lesson.lesson_time
        updateform.location.data = lesson.location
        updateform.plan.data = lesson.plan
        updateform.comments.data = lesson.comments
        updateform.homework.data = lesson.homework
        return render_template('update_lesson.html', updateform=updateform,
                               lesson_id=lesson_id)


@app.route('/user/logout', strict_slashes=False)
def handle_logout():
    """Handle logging out a signed in user"""
    if "user" in session:
        session.pop('user', None)
        return redirect(url_for('handle_home'))


@app.route('/user/schedule', strict_slashes=False)
def handle_schedule():
    """ Display calendar view with user's daily schedule """
    if "user" in session:
        user_id = session["user"]
        user = storage.get(User, user_id)
        ss = user.schedule()
        if ss is not None:
            ss = sorted(ss, key=lambda s: s[0], reverse=True)
            return render_template('calendar.html', ss=ss)
        else:
            return "<p> No lessons scheduled </p>"
    else:
        return redirect(url_for('handle_login'))


if __name__ == "__main__":
    """ Main Function """
    app.run(host='0.0.0.0', port=8080, debug=True)
