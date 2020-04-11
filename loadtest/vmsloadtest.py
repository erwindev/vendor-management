import json
from locust import HttpLocust, TaskSet, between

def login(l):
    headers = {'content-type': 'application/json'}
    payload = {"username": "ealberto", "password": "test"}
    l.client.post(
            '/api/v1/auth/login',
            data=json.dumps(payload),
            headers=headers
        )

def index(l):
    l.client.get("/")

class VmsUserBehavior(TaskSet):
    tasks = {index: 2}

    def on_start(self):
        login(self)

    def on_stop(self):
        index(self)

class WebsiteUser(HttpLocust):
    task_set = VmsUserBehavior
    wait_time = between(5.0, 9.0)