![VMS application](https://github.com/erwindev/vendor-management/workflows/VMS%20application/badge.svg?branch=master)

# Vendor Management System

This is a sample application that will be used to teach SheCanCodeIT members how to build a web application using Python and Flask.

## Get Started
Install Python 3
* [Windows](https://realpython.com/installing-python/#windows)
* [MacOSX](https://realpython.com/installing-python/#macos-mac-os-x)

Install Pip
* [Windows](https://www.liquidweb.com/kb/install-pip-windows/)
* [Mac](https://www.shellhacks.com/python-install-pip-mac-ubuntu-centos/)

Install Virtualenv (Globally)
```
$ pip install virtualenv
```

## Setup the app
Clone the repo
* git clone https://github.com/erwindev/vendor-management.git

Setup the development environment
```
$ cd vendor-management
$ virtualenv venv
$ . venv/bin/activate
```
Note: This will setup a virtual environment in your machine.

Install application requirements in your virtual environment
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
$ flask db migrate -m 'add comment here'
$ flask db upgrade
```

## Run the application
```
$ flask run
```

Bring the Auth REST API

Another way of interacting with this application is through a REST APIs.  To see the information about the REST API, you can access the Swagger docs
* Auth API (http://localhost:5000/u/v1/)
* Product API (http://localhost:5000/p/v1)
* Notes API (http://localhost:5000/n/v1)
* Contacts API (http://localhost:5000/c/v1)
* Attachment API (http://localhost:5000/a/v1)

## Test the application
Run unittest
```
$ export FLASK_ENV=test
$ flask test
```
Run test coverage and show coverage reports
```
$ export FLASK_ENV=test
$ coverage run vms_test_suite.py
$ coverage report --omit="app/*/test/*.py" app/*/*/*.py
$ coverage html --omit="app/*/test/*.py" app/*/*/*.py 
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
$ cd deployment/compose
$ docker-compose build
$ docker-compose up
```

Access the Auth API via this url - http://localhost/u/v1

## Run in Kubernetes - Minikube
minikube is a tool that allows to easily runs a local Kubernetes environment.  To install it,

```
$ brew update
$ brew install kubectl
$ brew install minikube
```

To run it,

```
$ minikube config set vm-driver hyperkit
$ minikube start
$ minikube dashboard
```

If you run into some problems, you can easily delete it.

```
$ minkube delete
$ minikube delete
$ rm /usr/local/bin/minikube
$ rm -rf ~/.minikube
```

To deploy the application, first create the Postgres database.

```
$ cd deployment/minikube
$ kubectl apply -f ./persistent-volume.yml
$ kubectl apply -f ./persistent-volume-claim.yml
$ kubectl apply -f ./secret.yml
$ kubectl create -f ./postgres-deployment.yml
$ kubectl create -f ./postgres-service.yml
$ POD_NAME=$(kubectl get pod -l service=postgres -o jsonpath="{.items[0].metadata.name}")
$ kubectl exec $POD_NAME --stdin --tty -- createdb -U vms_user vms
```

Before we deploy the application, first build the VMS docker image
```
$ cd ../..
$ docker build -t ealberto/vms-app:latest .
$ docker push ealberto/vms-app:latest
```

Deploy the application
```
$ cd deployment/minikube
$ kubectl create -f ./vms-app-deployment.yml
$ kubectl create -f ./vms-app-service.yml
$ minikube addons enable ingress
$ kubectl apply -f ./minikube-ingress.yml
$ echo "$(minikube ip) erwindev.io" | sudo tee -a /etc/hosts
```

## Run in Kubernetes - GKE

Create the cluster
```
$ gcloud container clusters create vms-cluster --zone us-east1-b --machine-type=n1-standard-1 --max-nodes=3 --min-nodes=1
```

List the cluster
```
$ gcloud container clusters list
```

Scale down the cluster
```
$ gcloud container clusters resize vms-cluster --size 0 --zone us-east1-b
```

Get credentials for the cluster
```
$ gcloud container clusters get-credentials vms-cluster --zone us-east1-b
```

Upload the service the database service credentials
```
$ kubectl create secret generic vms-cloudsql-instance-credentials --from-file=sql_credentials.json=/Users/ealberto/mystuff/erwindev-vms-db-b1dca3f9d9a1.json
```

Create the username and password as secrets
```
$ kubectl create secret generic vms-cloudsql-db-credentials --from-literal=username=vms_user --from-literal=password=D3qvzsAJHarhELzvK9
```

Create deployment
```
$ cd deployment/gcp
$ kubectl create -f vms-app-deployment.yml
```

List deployed apps
```
$ kubectl get deployments
```

Create service
```
$ kubectl create -f vms-app-service.yml
```

List Services
```
$ kubectl get services
```

Create a static IP
```
$ gcloud compute addresses create vms-static-ip --global
$ gcloud compute addresses list
```

If working with multiple, context
```
$ kubectl config get-contexts
$ kubectl config use-context [CONTEXT]
```

## Load test the application
For load testing, we will use [Locust](http://locust.io).  The load testing script is located under the `loadtest` folder.  Curerntly, we are only load testing the `/u/v1/auth/login` api.  To run the script,
```
$ cd loadtest
$ locust -f vmsloadtest.py
```

Bring up the Locust dashboard by going to http://localhost:8089.  Enter the following information,
```
Number of total users to simulate: 100
Hatch rate: 5
Host: http://localhost:5000
```
Note: Before we can load test, please start the application.  The URL will be what you will provide in the "Host" parameter.