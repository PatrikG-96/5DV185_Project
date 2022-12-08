from abc import ABC, abstractmethod
from enum import Enum
from threading import Thread
import asyncio
import aiohttp
import json
import logging

class Type(Enum):
    NUMERIC = 1,
    TEXT = 2

class SensorType(Enum):
    NONE = -1
    QUERY = 0,
    ACTIVE = 1

class SensorField:

    def __init__(self, field_name, type, default):
        self.field_name = field_name
        self.default = default
        self.type = type

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, SensorField):
            return False
        return self.field_name == __o.field_name and self.type == __o.type and self.default == __o.default


class Field:

    def __init__(self, name, type):
        self.name = name
        self.type = type

"""
Base abstract Sensor class. Defines simple methods that all sensor should have

Attributes:
    id (int): identifier for sensor
    data_description (dict): key value pairs for all data fields of the sensor. Key is the field name,
                             value is a tuple of the type (see Type enum) and a default value
"""
class Sensor(ABC):

    def __init__(self, id : int):
        self.id = id
        self.connected = False
        self.started = False
        self.data_description = {}

    @abstractmethod
    def connect(self):
        raise NotImplementedError

    @abstractmethod
    def disconnect(self):
        raise NotImplementedError

    @abstractmethod
    def start(self):
        raise NotImplementedError

    @abstractmethod
    def stop(self):
        raise NotImplementedError


class QuerySensor(Sensor):

    @abstractmethod
    async def query_sensor(self, query_info):
        raise NotImplementedError

class ActiveSensor(Sensor):

    def __init__(self, id):
        super().__init__(id)
        self.callback = None
        self.thread = Thread(target = self.run)
        self.running = False

    def start(self):
        print("started")
        self.thread.daemon = True
        self.thread.start()
        self.running = True

    def stop(self):
        self.running = False

    @abstractmethod
    def run(self):
        raise NotImplementedError()

class RecognitionSensor(QuerySensor):

    def __init__(self, id: int, model):
        super().__init__(id)
        self.model = model
    
    async def query_sensor(self, query_info):
        return self.model.predict(query_info)

    def connect(self):
        self.connected = True

    def disconnect(self):
        self.connected = False

    def start(self):
        self.started = True

    def stop(self):
        self.started = False


class SingleRequestApiSensor(QuerySensor):

    def __init__(self, id, url):
        super().__init__(id)
        self.url = url


    async def query_sensor(self, form):
        # make request to the url (maybe add some parameters)
        # return the raw response, let subclass handle it
        if not self.connected or not self.started:
            # do something
   

            async with aiohttp.ClientSession(json_serialize=json.dumps) as session:

                query = self.url
                logging.debug(f"Making request to {query} with data {form}")
                
                async with session.post(query, json=form) as response:
                    
                        return await response.json()
               
     

         

        
        return -1


    def connect(self):
        self.connected = True

    def disconnect(self):
        self.connected = False

    def start(self):
        self.started = True

    def stop(self):
        self.started = False


class MultiRequestApiSensor(QuerySensor):

    def __init__(self, id, urls):
        super().__init__(id)
        self.urls = urls



    async def make_request(self, session, url, json):

        async with session.post(url, json=json) as response:
            
                return await response.json()
 
        
  

    async def query_sensor(self, forms : list[dict]):
        # make request to the url (maybe add some parameters)
        # return the raw response, let subclass handle it
        if not self.connected or not self.started:
            # do something
            
            if len(forms) != len(self.urls):
                return -1
            final_result = {}

            async with aiohttp.ClientSession(json_serialize=json.dumps) as session:


                gathered_result = await asyncio.gather(*[self.make_request(session, self.urls[i], forms[i]) for i in range(len(forms))], return_exceptions=True)
            


            for single_result in gathered_result:
                final_result.update(single_result)

            logging.debug("Session closed") 
            return final_result


        
        return -1


    def connect(self):
        self.connected = True

    def disconnect(self):
        self.connected = False

    def start(self):
        self.started = True

    def stop(self):
        self.started = False