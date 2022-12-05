from .sensor_base import Sensor, QuerySensor, ActiveSensor, SensorField, SensorType
import typing
from util import copy_dict_subset
from abc import ABC, abstractmethod




class SensorNetwork:

    def __init__(self):
        self.active_sensors : list[ActiveSensor] = []
        self.query_sensors : list[QuerySensor] = []
        self.sensor_data = {}
        self.sensor_descriptions = {}
        self.sensor_dependencies = {}

    def add_sensor(self, sensor : Sensor):
        
        self.sensor_descriptions[sensor.id] = sensor.data_description

        self.sensor_data[sensor.id] = {}

        for field in sensor.data_description:
            self.sensor_data[sensor.id][field.field_name] = field.default

        if isinstance(sensor, ActiveSensor):
 
            self.active_sensors.append(sensor)
            sensor.callback = self.insert_data
        else:
            self.query_sensors.append(sensor)


    def insert_data(self, sensor_id : int, sensor_data : dict):

        self.sensor_data[sensor_id] = sensor_data



    async def get_data(self, sensor_id, input = None):

        if input is not None:

            await self.trigger_query(sensor_id, input)       
        
        return self.sensor_data[sensor_id]

    async def trigger_query(self, sensor_id, query_info):
        for sensor in self.query_sensors:
            
            if sensor.id == sensor_id:
                result = await sensor.query_sensor(query_info)
                self.sensor_data[sensor_id] = result
                return
        raise Exception()


    def connect_all(self):
        for a_s in self.active_sensors:
            a_s.connect()
        for q_s in self.query_sensors:
            q_s.disconnect()

    def disconnect_all(self):
        for a_s in self.active_sensors:
            a_s.disconnect()
        for q_s in self.query_sensors:
            q_s.disconnect()

    def start(self):
        for a_s in self.active_sensors:
            a_s.start()
        for q_s in self.query_sensors:
            q_s.start()

    def stop(self):
        for a_s in self.active_sensors:
            a_s.stop()
        for q_s in self.query_sensors:
            q_s.stop()
