# -*- coding: utf-8 -*-

from locust import HttpUser, task, between
from lib.example_functions import choose_random_page
from locust import events
import names 
import random
import requests
import json
import os

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

    @task(2)
    def get_requests(self):
        print("User instance (%r) executing my_task" % self)
        print(f"Successfully made a request to: {WebsiteUser.host}/api/bookings/")
        self.client.get("/showtimes/list", headers=default_headers)
        self.client.get("/movies/list", headers=default_headers)
        self.client.get("/bookings/list", headers=default_headers)

    @task(1) 
    def add_user(self):

       new_user = {'Name': 'foo', 'LastName': 'bar'}

       new_user['Name'] = names.get_first_name()
       new_user['LastName'] = names.get_last_name()

       # headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
       self.client.post("/api/users/", json=new_user, headers=default_headers)

    @task(3)
    def add_booking(self):
        bookings = self.client.get('/api/bookings/')
        showtimes = self.client.get('/api/showtimes/')
        users = self.client.get('/api/users/')
        movies = self.client.get('/api/movies/')
        
        user_ids = []
        showtime_ids = []
        movie_ids = []
      
        for key in users.json():
          user_ids.append(key['ID'])

        for key in showtimes.json():
           showtime_ids.append(key['ID'])

        for key in movies.json():
           movie_ids.append(key['ID'])
        
        rand_user = user_ids[random.randint(0, len(user_ids)-1)]
        rand_showtime = showtime_ids[random.randint(0, len(showtime_ids)-1)]
        rand_movie = movie_ids[random.randint(0, len(movie_ids)-1)]

        new_booking = {'UserID': rand_user, 'MovieID': rand_movie, 'ShowtimeID': rand_showtime}
      
        self.client.post('/api/bookings/', json=json.dumps(new_booking), headers=default_headers)
