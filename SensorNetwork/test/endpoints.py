from urllib.parse import urlparse
from time import sleep
import random

class TestEndpoint:

    FAIL = -1

    def __init__(self, base_url):
        self.base_url = base_url
        self.routes = {}

    def add_route(self, route, data):
        self.routes[route] = data

    def get_data(self, route : str):

        if route not in self.routes:
            return TestEndpoint.FAIL

        return self.routes[route]

    
class TestHttpClient:

    def __init__(self):
        self.endpoints = {}
        

    def add_endpoint(self, endpoint : TestEndpoint):
        self.endpoints[endpoint.base_url] = endpoint

    def get(self, url):

        delay = random.uniform(0.1, 1.0)

        result = urlparse("http://"+url)
        
        if not result.netloc in self.endpoints:
            sleep(delay)
            return {"error" : 404}

        answer = self.endpoints[result.netloc].get_data(result.path)

        sleep(delay)

        return answer