# -*- coding: utf-8 -*-

from locust import HttpUser, task, between
from lib.example_functions import choose_random_page
from locust import events


default_headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'}
        

@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    print("A new test is starting")

@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    print("A new test is ending")
    
class WebsiteUser(HttpUser):
    wait_time = between(1, 2)

    @task(1)
    def get_index(self):
        print("User instance (%r) executing my_task" % self)
        self.client.get("/", headers=default_headers)

    @task(3)
    def get_random_page(self):
        self.client.get(choose_random_page(), headers=default_headers)
