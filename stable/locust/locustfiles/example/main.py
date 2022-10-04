# -*- coding: utf-8 -*-

from locust import HttpUser, task, between
from lib.example_functions import choose_random_page
from locust import events
import names 


default_headers = {'User-Agent': 'locust-test'} 
                   
                   # 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'}
        

@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    print("A new test is starting")

@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    print("A new test is ending")
    
class WebsiteUser(HttpUser):
    wait_time = between(1, 2)

    @task(1)
    def get_requests(self):
        print("User instance (%r) executing my_task" % self)
        self.client.get("/showtimes/list", headers=default_headers)
        self.client.get("/movies/list", headers=default_headers)
        self.client.get("/bookings/list", headers=default_headers)

    @task(2) 
    def add_user(self):

       new_user = {'Name': 'foo', 'LastName': 'bar'}

       new_user['Name'] = names.get_first_name()
       new_user['LastName'] = names.get_last_name()

       # headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
       self.client.post("/api/users/", json=new_user, headers=default_headers)
