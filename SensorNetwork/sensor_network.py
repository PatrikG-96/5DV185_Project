from sensor_base import Sensor, QuerySensor, ActiveSensor
import typing

class SensorField:

    def __init__(self, field_name, sensor_id):
        self.field_name = field_name
        self.sensor_id = sensor_id

class SensorNetwork:

    def __init__(self):
        self.active_sensors : list[ActiveSensor] = []
        self.query_sensors : list[QuerySensor] = []
        self.sensor_data = {}
        self.sensor_descriptions = {}

    def add_sensor(self, sensor : Sensor):
        
        self.sensor_descriptions[sensor.id] = sensor.data_description

        self.sensor_data[sensor.id] = {}

        for field, (_, default) in sensor.data_description.items():
            self.sensor_data[sensor.id][field] = default

        if isinstance(sensor, ActiveSensor):
 
            self.active_sensors.append(sensor)
            sensor.callback = self.insert_data
        else:
            self.query_sensors.append(sensor)

    def remove_sensor(self, sensor):
        pass

    def insert_data(self, sensor_id : int, sensor_data : dict):

        self.sensor_data[sensor_id] = sensor_data

    def get_data(self, sensor_id):
        return self.sensor_data[sensor_id]

    def trigger_query(self, qsensor_id, query_info):
        for sensor in self.query_sensors:
            
            if sensor.id == qsensor_id:
                result = sensor.query_sensor(query_info)
                self.sensor_data[qsensor_id] = result
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
    
 
    