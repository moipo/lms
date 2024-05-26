Python version: 3.10.0

A learning management system with a simple interface

Demo teacher credentials:
    login: teacher1         
    password: some_password
there are also teacher2 and teacher3 with the same password


Demo student credentials:
    login: student1
    password: some_password
there are also student2 student3, student4, student5, student6 with the same password


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
