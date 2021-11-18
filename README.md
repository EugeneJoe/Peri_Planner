# Peri Planner App

## Introduction
Peri Planner App is a web-based application to aid peripatetic tutors organise and plan their lessons. It works as a lesson planner for tutors who work in various schools or in their own studios and need a way to keep track of all their students' progress in one central, easily accessible place.

## Motivation
The motivation to build this app came from my personal experience as a peripatetic tutor in Nairobi. We work in dynamic environments in different schools that have slightly different rules about how they like their things done and in our private studios with private students who each have different needs. I saw the need for a centralised place where one can do their own lesson planning and track the progress of each student.

The Peri Planner App seeks to meet this need for tutors and even coaches and provide them a personal platform to plan their lessons and track students' progress.

## Tech Stack
- Python
- MySQL

- HTML
- CSS using Bootstrap 4
- Javascript, Jquery

## Installation

Peri Planner App is a flask application running on Python 3.4 and using MySQL database for data storage.
To run it on your local machine:
1. Clone the repository
2. Install the required libraries in the requirements.txt file
3. Run the setup_mysql_dev.sql to setup the required database as follows:

```
cat setup_mysql_dev.sql | mysql -uroot -p
```

4. Start the flask app, passing the required environment variables as follows:

```python
PERI_MYSQL_USER=peri_dev PERI_MYSQL_PWD=peri_dev_pwd PERI_MYSQL_HOST=localhost PERI_MYSQL_DB=peri_dev_db PERI_TYPE_STORAGE=db ./peri_dynamic.py
```

You can now access the web app from your browser on '''http://127.0.0.1:5001'''
The project can also be deployed using Nginx and Gunicorn

## Usage
Peri Planner App enables its users to create an account and log in from where they can:
1. Add new students they are teaching and the instrument/activity they are learning.
2. View all your existing students and their instruments/activity
3. View and update each student's existing lesson logs. Each lesson log contains the following fields:
   - Lesson time
   - Location
   - Lesson plan: A description of what you intended to cover in that lesson
   - Lesson comments: A description of how the lesson went and any details you noticed.
   - Lesson homework: Any homework you may have assigned your student
4. Add new lesson logs for each student. When adding a new lesson log, the lesson plan field is required and cannot be left empty. Other fields can be left empty as this is information that may change before or after the lesson  has occured.
5. View you schedule depending on the scheduled lessons. This only works for lesson logs whose lesson time field has been filled.

You can check out the live project [here](https://periplanner.joebnb.tech/login)

## Screenshots
### Students Display Page

<p align="center">
   <img align="center" src="https://github.com/EugeneJoe/EugeneJoe.github.io/blob/9793eb30b6d801b99608afab04712c568f3e393b/images/students.png?raw=true" alt="Students Page" />
</p>

### Lessons Display Page
<p align="center">
   <img align="center" src="https://github.com/EugeneJoe/EugeneJoe.github.io/blob/9793eb30b6d801b99608afab04712c568f3e393b/images/lessons.png?raw=true" alt="Lessons Page" />
</p>

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## Author
Eugene Muthui
- LinkedIn: [@Eugene Joe Muthui](https://www.linkedin.com/in/eugene-joe-muthui-954b633a)
- Twitter: [@MuthuiJoe](https://twitter.com/MuthuiJoe)
- Github: [@EugeneJoe](https://github.com/EugeneJoe)

## Licensing
MIT License

Copyright (c) [2021] [Eugene Joe Muthui] (https://github.com/EugeneJoe)
This project is [MIT] (https://github.com/EugeneJoe/Peri_Planner/blob/master/LICENSE) licensed.
