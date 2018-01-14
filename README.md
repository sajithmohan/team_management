# Team Management
This is a sample project which implemented HTTP REST API for team member management using Django, Django REST framework, MySQL
## Getting Started
To run this project you need to clone this project , install libraries and setup database.
please follow the instructions given below to setup and run the project
### Prerequisites
This project requires Python3, MySQL.please install if not already installed
### Installing
Clone this project into your system
```
git clone git@github.com:sajithmohan/team_management.git
```
Install libraries
```
pip install -r requirements.txt
```
### Setup database
Create a database and give the details in setting.py under DATABASES section.
Change the below part
```
DATABASES = {
    'default': {
        'NAME': 'team_management1',
        'ENGINE': 'django.db.backends.mysql',
        'USER': 'root',
        'PASSWORD': '12345',
        'HOST': 'localhost',
        'OPTIONS': {
          'autocommit': True,
        },
    }
}
```
then run migrations for creating  tables in the database
```
python manage.py migrate
```
## Running the project
```
python manage.py runserver
```
## Running tests
```
python manage.py test
```
## API Documentation
Please see the below link for Auto generated Api documentation
[http://127.0.0.1:8000/docs/](http://127.0.0.1:8000/docs/)

### Sample curl requests
#### CREATE team member
```
curl -XPOST -H "Content-type: application/json" -d '{
        "first_name": "sajith2",
        "last_name": "mohan",
        "email": "sajith@gmail.com",
        "role": "regular",
        "phone_number": "1234567890"
}' 'http://127.0.0.1:8000/team_members/'
```
#### GET Team member by id
```
curl -XGET -H "Content-type: application/json" 'http://127.0.0.1:8000/team_members/2/'
```
#### LIST Team members
```
curl -XGET -H "Content-type: application/json" 'http://127.0.0.1:8000/team_members/'
```
#### UPDATE Team members
```
curl -XPUT -H "Content-type: application/json" -d '{
        "first_name": "sajith",
        "last_name": "mohan",
        "email": "sajith@gmail.com",
        "role": "regular",
        "phone_number": "1234567890"
}' 'http://127.0.0.1:8000/team_members/1/'
```
#### UPDATE Partial data
```
curl -XPATCH -H "Content-type: application/json" -d '{
    "first_name": "aaa"
}' 'http://127.0.0.1:8000/team_members/1/'
```
#### DELETE
```
curl -XDELETE -H "Content-type: application/json" 'http://127.0.0.1:8000/team_members/1/'
```
