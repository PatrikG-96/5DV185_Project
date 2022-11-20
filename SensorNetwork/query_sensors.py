from sensor_base import ApiSensor, Field, Type
from recognition import RegPlateRecognition

class RegPlateSensor(ApiSensor):

    def __init__(self, id, url):
        super().__init__(id, url)
        self.data_description = {"suspect_name" : ( Type.TEXT, None), "suspect_age" : ( Type.NUMERIC, None)}

    def query_sensor(self, query_info):
        plate_string = RegPlateRecognition.predict(query_info)
        result = super().query_sensor(plate_string)
        # parse api result to get a reasonable format

    
