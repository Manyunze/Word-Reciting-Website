# Word-Reciting-Website

This is a demo Word Reciting Website for `B/S Software Design` class.

## 1. Introduction
The _*VocalMem*_ website is a simple B/S website for word reciting. It contains user registration and login, information saving and checking, study plan setting and managing, note adding, deleting and editing. 

On this Framework, you can easily change the front-end HTML, as well as Django backend. This is a demo so any change is welcomed. 

#### 1.1 Design Graph
![Design]()

#### 1.1 Environment
- Database: MySQL
- Python version: 3.6
- Framework: Django 1.11
- OS：Windows, Linux, Mac
- Browser: Chrome, Firefox, Safari (Others are not tested)

## 2. Demo



## 2. How to deploy and run the website
#### 2.1 By PythonAnyWhere (deprecated)
The website has been deployed on PythonAnyWhere, You can type http://manyz.pythonanywhere.com/ in browser to view.

__*(Note that PythonAnyWhere account has expired, so you might want to use Method 2)*__

#### 2.2 Run locally by source code
###### 2.2.1 Activate virtual environment venv
venv is not included because of its size
Basically, you need:
- Django 1.11
- Python 3.6
- Database MySQL
###### 2.2.2 Install Prerequisit
> _mysql database client_: Default is mysqlclient
###### 2.2.3 Change setting file
Inside `mysite/settings.py`
```python
    DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'django_bs',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': '127.0.0.1',  # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '3306',       # Set to empty string for default.
    }
}
```
- change `NAME` into the name of database in MySQL
- change `USER` and `PASSWORD` according to your own database 

###### 2.2.4 Migrate the data
Run following commands
```python
python manage.py makemigrations
python manage.py migrate
```

###### 2.2.5 Import dictionary
```python
python add_words_full.py
```

###### 2.2.6 Deploy
```python
python manage.py runserver
```

###### Now you can see the website in 127.0.0.1

## 3. How to use website
- Check HOME and About for the information about the website
- Then register and login to use certain functions of the website
- Enter Vocabulary module, set the study plan and begin to learn
- You can add notes at anytime when you are reciting the words
- Chech your notes in Notebook 
