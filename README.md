# Jobs Portal
This is a simple jobs portal built using Django and Django Rest Framework. 
User can register and login to the portal. Once logged in, user can view the list of jobs posted by Admin. 
User can apply for the job by submitting the resume. User can also view the list of jobs applied by him.

### Setup

The first thing to do is to clone the repository:
```shell
git clone "enter_here_link"
```
Create a virtual environment to install dependencies in and activate it:
run following command to install python-env

```shell
sudo apt-get install python3-venv  
mkdir djangoenv
```

create and activate virtual environment

```shell
python3 -m venv djangoenv 
source djangoenv/bin/activate 
```
Then install the dependencies:

```shell
pip install -r requirements.txt
```

After installing dependencies run following command to migrate changes in db:

```shell
python manage.py migrate
```

Note the (env) in front of the prompt. This indicates that this terminal session operates in a virtual environment:

Now you can run the development server using following command:

```shell
python manage.py runserver
```


