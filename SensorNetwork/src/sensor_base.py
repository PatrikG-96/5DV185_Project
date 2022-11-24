from abc import ABC, abstractmethod
from .communication import HttpClient
from enum import Enum
from threading import Thread
from cachetools import TTLCache

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
    def query_sensor(self, query_info):
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

# class CachingQuerySensor(QuerySensor):

#     CACHE_SIZE = 1

#     def __init__(self, id: int, timeout : int):
#         super().__init__(id)
#         self.cache = TTLCache(maxsize=CachingQuerySensor.CACHE_SIZE, ttl = timeout)


#     def __cache(self, )

class ApiSensor(QuerySensor):

    def __init__(self, id, url, client_get):
        super().__init__(id)
        self.url = url
        self.get = client_get

    def query_sensor(self, query_string):
        # make request to the url (maybe add some parameters)
        # return the raw response, let subclass handle it
        if not self.connected or not self.started:
            # do something
            return self.get(self.url + query_string)
        
        return -1


    def connect(self):
        self.connected = True

    def disconnect(self):
        self.connected = False

    def start(self):
        self.started = True

    def stop(self):
        self.started = False