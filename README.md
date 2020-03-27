# Software Vendor Tracking Tool

This is a sample application that will be used to teach SheCanCodeIT members how to build a web application using Flask.

## Get Started
#### Install Python 3
* [Windows](https://realpython.com/installing-python/#windows)
* [MacOSX](https://realpython.com/installing-python/#macos-mac-os-x)

#### Install Pip
* [Windows](https://www.liquidweb.com/kb/install-pip-windows/)
* [Mac](https://www.shellhacks.com/python-install-pip-mac-ubuntu-centos/)

#### Install Virtualend (Globally)
```
$ pip install virtualenv
```

## Setup the app
#### Clone the repo
* git clone https://github.com/erwindev/shecancodeit-vms.git

#### Setup the development environment
```
$ cd shecancodeit
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

#### Run the application
```
$ flask run
```

#### Bring up your application in your browser
* http://127.0.0.1:5000/



