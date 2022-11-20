from abc import ABC, abstractmethod
from enum import Enum

class Type(Enum):
    NUMERIC = 1,
    TEXT = 2

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


class ApiSensor(QuerySensor):

    def __init__(self, id, url):
        super().__init__(id)
        self.url = url

    def query_sensor(self, query_info):
        # make request to the url (maybe add some parameters)
        # return the raw response, let subclass handle it
        if not self.connected or not self.started:
            # do something
            return
        pass

    def connect(self):
        self.connected = True

    def disconnect(self):
        self.connected = False

    def start(self):
        self.started = True

    def stop(self):
        self.started = False