# Software Vendor Tracking Tool

This is a sample application that will be used to teach SheCanCodeIT members how to build a web application using Flask.

## Get Started
#### Install Python 3
* [Windows](https://realpython.com/installing-python/#windows)
* [MacOSX](https://realpython.com/installing-python/#macos-mac-os-x)

#### Install Pip
* [Windows](https://www.liquidweb.com/kb/install-pip-windows/)
* [Mac](https://www.shellhacks.com/python-install-pip-mac-ubuntu-centos/)

#### Install Virtualenv (Globally)
```
$ pip install virtualenv
```

## Setup the app
#### Clone the repo
* git clone https://github.com/erwindev/vendor-management.git

#### Setup the development environment
```
$ cd vendor-management
$ virtualenv venv
$ . venv/bin/activate
```
Note: This will setup a virtual environment in your machine.

#### Install application requirements in your virtual environment
```
$ pip install -r requirements.txt
```

#### Setup the database
Note: For this application, we will be using SQLite.
```
$ flask db upgrade
```
If you made changes to the models code, you will need to run the migration script
```
$ flask migrate -m 'add comment here'
$ flask db upgrade
```

#### Create the environment settings
```
$ cat .env
```
Add the following entries
```
SERVICE_NAME=Vendor Managetment Service
CURRENT_VERSION=0.1
SECRET_KEY=yourverysecuresecretkey
```

#### Run the application
```
$ export FLASK_APP=application.py
$ export FLASK_ENV=development
$ flask run
```

#### Bring up your application in your browser
* http://localhost:5000/

#### Using the REST API
Another way of interacting with this application is through a REST APIs.  To see the information about the REST API, you can access the Swagger docs
* http://localhost:5000/api/v1/


#### Test the application
Run unittest
```
$ flask test
```
Run test coverage and show coverage reports
```
$ coverage run -m unittest app/test/test*.py
$ coverage report app/vendor/*/*.py
$ coverage html app/vendor/*/*.py 
```

The html coverage report will be generated under htmlcov folder.  Under that folder launch index.html in your favorite browser.
