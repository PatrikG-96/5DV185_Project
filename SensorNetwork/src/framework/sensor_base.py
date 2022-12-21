from abc import ABC, abstractmethod
from enum import Enum
from threading import Thread
from .recognition import Recognition
import asyncio
import aiohttp
import json
import logging

log = logging.getLogger()

class Sensor(ABC):
    """
    Base abstract Sensor class. Defines simple methods that all sensor should have

    Attributes:
        id (int): identifier for sensor
        
    """

    def __init__(self, id : int):
        self.id = id
        self.connected = False
        self.started = False

    @abstractmethod
    def connect(self) -> None:
        raise NotImplementedError()

    @abstractmethod
    def disconnect(self) -> None:
        raise NotImplementedError()

    @abstractmethod
    def start(self) -> None:
        raise NotImplementedError()

    @abstractmethod
    def stop(self) -> None:
        raise NotImplementedError()


class QuerySensor(Sensor):

    @abstractmethod
    async def query_sensor(self, query_info : dict):
        raise NotImplementedError()
    
    def connect(self):
        self.connected = True

    def disconnect(self):
        self.connected = False

    def start(self):
        self.started = True

    def stop(self):
        self.started = False


class ActiveSensor(Sensor):

    def __init__(self, id : int) -> None:
        super().__init__(id)
        self.callback = None
        self.thread = Thread(target = self.run)
        self.running = False

    def start(self):
        self.thread.daemon = True
        self.thread.start()
        self.running = True

    def stop(self):
        self.running = False

    @abstractmethod
    def run(self) -> None:
        raise NotImplementedError()

class RecognitionSensor(QuerySensor):

    def __init__(self, id: int, model : Recognition) -> None:
        super().__init__(id)
        self.model = model
    
    async def query_sensor(self, query_info : dict) -> dict:
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

    def __init__(self, id : int, url : str) -> None:
        super().__init__(id)
        self.url = url


    async def query_sensor(self, form : dict) -> dict:

        if self.connected and self.started:
  
            async with aiohttp.ClientSession(json_serialize=json.dumps) as session:

                query = self.url
                log.debug(f"Making request to {query} with data {form}")
                
                async with session.post(query, json=form) as response:
                    
                        return await response.json()
        
        log.debug("not started or conneted")
        return -1


    

class MultiRequestApiSensor(QuerySensor):

    def __init__(self, id : int, urls : list[str]) -> None:
        super().__init__(id)
        self.urls = urls

    async def __make_request(self, session, url, json):

        async with session.post(url, json=json) as response:
            
                return await response.json()
 

    async def query_sensor(self, forms : list[dict]) -> dict:
        # make request to the url (maybe add some parameters)
        # return the raw response, let subclass handle it
        if self.connected and self.started:
            # do something
            
            if len(forms) != len(self.urls):
                return -1
            final_result = {}

            async with aiohttp.ClientSession(json_serialize=json.dumps) as session:


                gathered_result = await asyncio.gather(*[self.__make_request(session, self.urls[i], forms[i]) for i in range(len(forms))], return_exceptions=True)
            


            for single_result in gathered_result:
                final_result.update(single_result)

            log.debug("Session closed") 
            return final_result


        log.debug("not started/connected")
        
        return -1


    def connect(self):
        self.connected = True

    def disconnect(self):
        self.connected = False

    def start(self):
        self.started = True

    def stop(self):
        self.started = False