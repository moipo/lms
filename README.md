Python version: 3.10.0

Description:
A learning management system with a simple interface, where teachers can create
different types of tasks for students:  Test, General-purpose task and Materials.
Students can do these tasks and get grades.
The system also includes permission-based storage for files for each of the student groups, 
and an option to view statistics of an individual or an entire subjects.
There are two separate flows for dynamically constructing and taking a test. A test has a custom
amount of answers. After taking a test a grade is generated automatically.
General-purpose task allows to add files and then evaluate student's answer and even 'chat' with a
student many times on the topic of the task if needed (via 'must be redone' option).
There are also a login subsystem and a separate flow for each type of the task.

Login form and a part of the project accountable for creating and taking tests was taken from one of my first
projects (a very old one) so related part of frontend may not look very well for all the
monitor resolutions (seems to look alright with 1920 * 1080)


     
Demo teacher credentials:
    login: teacher1         
    password: some_password

Demo student credentials:
    login: student2
    password: some_password

(there are also teacher2, teacher3, student1, student3, student4, student5, student6
with the same password)


commands to launch the project locally(Linux):
        python3 -m venv myvenv
        source myvenv/bin/activate
        pip install -r requirements.txt
        python3 manage.py runserver 


static analysis tools:
    black univ_app
    autoflake --remove-all-unused-imports -i -r univ_app
    isort univ_app
    pylint --load-plugins pylint_django --django-settings-module=lms.settings --ignore=migrations /c/Users/moipo/projects/lms/univ_app
