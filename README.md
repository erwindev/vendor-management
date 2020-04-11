# Vendor Management System

This is a sample application that will be used to teach SheCanCodeIT members how to build a web application using Python and Flask.

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

## Setup the database
Note: For this application, we will be using SQLite.
```
$ flask db upgrade
```
If you made changes to the models code, you will need to run the migration script
```
$ flask migrate -m 'add comment here'
$ flask db upgrade
```

## Run the application
```
$ flask run
```

#### Bring up your application in your browser
* http://localhost:5000/

#### Using the REST API
Another way of interacting with this application is through a REST APIs.  To see the information about the REST API, you can access the Swagger docs
* http://localhost:5000/api/v1/


## Test the application
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

## Run in Docker
Before you can do this, you will ned to install `docker`.  You can find instructions on how to install Docker [here](https://docs.docker.com/get-docker/).

You will also need to create a `vms.env` file that contains settings for your database.  
```
$ touch vms.env
```

Add the following settings in the `vms.env` file.
```
SERVICE_NAME=Vendor Managetment Service
CURRENT_VERSION=1.0-uat
SECRET_KEY=secretkey
FLASK_ENV=production
POSTGRES_DB=vms
POSTGRES_USER=vms_user
POSTGRES_PASSWORD=vms_user
POSTGRES_HOST=vms-db
POSTGRES_PORT=5432
```

Build and run the docker containers.  `docker-compose build` will build your application into a docker image.  `docker-compose up` will run your application pointed to a Postgress database.  
```
$ cd compose
$ docker-compose build
$ docker-compose up
```

Access the application via this url - http://localhost:8080
Access the API via this url - http://localhost:8080/api/v1

## Load test the application
For load testing, we will use [Locust](http://locust.io).  The load testing script is located under the `loadtest` folder.  Curerntly, we are only load testing the `api/v1/auth/login` api.  To run the scrip,
```
$ cd loadtest
$ locust -f vmsloadtest.py
```
Bring up the Locust dashboard by going to http://localhost:8089.  Enter the following information,
```
Number of total users to simulate: 100
Hatch rate: 5
Host: http://localhost
```
