# Jobs Portal
This is a simple jobs portal built using Django and Django Rest Framework. 
User can register and login to the portal. Once logged in, user can view the list of jobs posted by Admin. 
User can apply for the job by submitting the resume. User can also view the list of jobs applied by him.

The first thing to do is to clone the repository:
```shell
git clone "enter_here_link"
```

### Setup With Docker
1. Install Docker and Docker Compose
2. To build the image, run the command below:
```shell
docker build . -t docker-django-v0.0.1
```
To run the app, execute the below command:
```shell
docker run docker-django-v0.0.1
```
By default, the app will run on port 8000. To access the app, go to http://localhost:8000
### Setup Without Docker
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
By default, the app will run on port 8000. To access the app, go to http://localhost:8000