from src.sensor_base import ActiveSensor, QuerySensor, Type, ApiSensor, SensorField, SensorType
from time import sleep
from threading import Thread

class TestBasicQuerySensor(QuerySensor):

    def __init__(self, id: int, key, data : int):
        super().__init__(id)
        self.data = data
        self.key = key
        self.data_description = [SensorField(key, Type.NUMERIC, None)]

    def query_sensor(self, query_info):
        val = query_info[self.key]
        return {self.key : self.data + val}

    def connect(self):
        pass

    def disconnect(self):
        pass

    def start(self):
        pass

    def stop(self):
        pass


class TestApiSensor(ApiSensor):

    def __init__(self, id, url, client_get):
        super().__init__(id, url, client_get)


    def query_sensor(self, query_info):
        # build query string
        result = super().query_sensor(query_info)

        return result

class TestActiveSensor(ActiveSensor):

    def __init__(self, id, frequency, max_value):
        super().__init__(id)
        self.delay = 1/frequency
        self.max = max_value

    def run(self):
        i = 0
        while(self.running and i <= self.max):
            self.callback({"value" : i})
            i += 1
            sleep(self.delay)
        
        self.stop()

    def connect(self):
        pass

    def disconnect(self):
        pass