Python version: 3.10.0

Description:

A learning management system with a simple interface, where teachers can create different types of tasks for students: tests, general-purpose tasks, and materials. Students can complete these tasks and receive grades. The system also includes permission-based storage for files for each student group and an option to view statistics for an individual or an entire subject. There are two separate flows for dynamically constructing and taking a test. A test can have a custom number of answers. After taking a test, a grade is generated automatically. The general-purpose task allows adding files and then evaluating the student's answer, including the option to 'chat' with a student multiple times about the task if needed (via the 'must be redone' option). There is also a login subsystem and a separate flow for each type of task.
The login form and the part of the project responsible for creating and taking tests were taken from one of my first projects (a very old one), so the related part of the frontend may not look optimal for all monitor resolutions (seems to look alright with 1920 * 1080).
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
    
    pylint --load-plugins pylint_django --django-settings-module=lms.settings --ignore=migrations univ_app
