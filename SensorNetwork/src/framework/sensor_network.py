from .sensor_base import Sensor, QuerySensor, ActiveSensor, SensorField, SensorType
import typing
from abc import ABC, abstractmethod
import logging



class SensorNetwork:

    def __init__(self):
        self.active_sensors : list[ActiveSensor] = []
        self.query_sensors : list[QuerySensor] = []
        self.sensor_data = {}
        self.sensor_descriptions = {}
        self.sensor_dependencies = {}

    def add_sensor(self, sensor : Sensor):

        logging.debug(f"Adding sensor '{sensor.id}'")
        
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

        logging.debug(f"Getting data for sensor '{sensor_id}', input: {input}")

        if input is not None:

            await self.trigger_query(sensor_id, input)       
        
        return self.sensor_data[sensor_id]

    async def trigger_query(self, sensor_id, query_info):

        logging.debug("Finding query sensor")

        for sensor in self.query_sensors:
            
            if sensor.id == sensor_id:
                logging.debug("Found sensor, performing query")
                
                result = await sensor.query_sensor(query_info)
    
                logging.debug("Query done")
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
