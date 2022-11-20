from sensor_base import ActiveSensor, QuerySensor, Type
from time import sleep
from threading import Thread

class IncrementalValue(ActiveSensor):

    def __init__(self, id):
        super().__init__(id)
        self.value = 0
        self.thread = None
        self.stop_flag = False
        self.data_description = {"value" : (Type.NUMERIC, -1)}

    def loop(self):

        while not self.stop_flag:
            self.callback(self.id, {"value" : self.value})
            self.value += 1
            sleep(2)

    def connect(self):
        pass
    
    def disconnect(self):
        pass

    def start(self):
        self.stop_flag = False
        self.thread = Thread(target = self.loop)
        self.thread.daemon = True
        self.thread.start()
        
    def stop(self):
        self.stop_flag = True
    

class TestQuery(QuerySensor):

    def __init__(self, id):
        super().__init__(id)
        self.data = {0:".",1:"H", 2:"E", 3:"L", 4:"L", 5:"O"}
        self.data_description = {"value" : (Type.TEXT, " ")}

    def connect(self):
        pass

    def disconnect(self):
        pass

    def start(self):
        pass

    def stop(self):
        pass

    def query_sensor(self, query_info : int):
        return {"value":self.data[query_info]}