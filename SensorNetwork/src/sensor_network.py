from .sensor_base import Sensor, QuerySensor, ActiveSensor, SensorField, SensorType
import typing

class Link:

    def __init__(self) -> None:
        self.next = None
        self.sensors = []

    def add(self, id, type):
        self.sensors.append((id, type, None, None))

    def add_fixed(self, id, type, input):
        self.sensors.append((id, type, input, None))
        
    def add_dependency(self, id, type, dep_id):
        self.sensors.append((id, type, None, dep_id))

    def __str__(self):
        return str(self.sensors)


class QueryChain:

    def __init__(self) -> None:
        self.root : Link = None

    def add_link(self, link):
        
        if self.root is None:
            self.root = link
            return

        temp = self.root
        while (temp.next is not None):
            temp = temp.next

        temp.next = link

    def traverse(self):

        temp = self.root
        while True:
            print(temp)
            temp = temp.next

            if temp is None:
                break


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
        self.sensor_dependencies[sensor.id] = []

        for field in sensor.data_description:
            self.sensor_data[sensor.id][field.field_name] = field.default

        if isinstance(sensor, ActiveSensor):
 
            self.active_sensors.append(sensor)
            sensor.callback = self.insert_data
        else:
            self.query_sensors.append(sensor)

    def remove_sensor(self, sensor):
        pass


    def execute_query_chain(self, query_chain : QueryChain):

        link = query_chain.root
        
        prev_output = {}

        while True:

            output = {}
            for (id, type, input, dependency) in link.sensors:
                
                if type == SensorType.ACTIVE:

                    output[id] = self.get_data(id)

                if type == SensorType.QUERY:
                    
                    if dependency is None:

                        output[id] = self.get_data(id, input)
                    
                    else:
                        
                        output[id] = self.get_data(id, prev_output[dependency])
                   
            link = link.next
            prev_output = output
           
            if link is None:
                break
        
        

        return output


    def add_sensor_dependency(self, dep_sensor, sensor_id, field : SensorField):

        if sensor_id not in self.sensor_data or dep_sensor not in self.sensor_data:
            return #error

        if field not in self.sensor_descriptions[sensor_id]:
            return # error

        self.sensor_dependencies[dep_sensor].append((sensor_id, field))

    def insert_data(self, sensor_id : int, sensor_data : dict):

        self.sensor_data[sensor_id] = sensor_data

    def find_sensor_type(self, id):

        for a_s in self.active_sensors:
            if a_s.id == id:
                return SensorType.ACTIVE
        
        for q_s in self.query_sensors:
            if q_s.id == id:
                return SensorType.QUERY

        return -1

    def get_data(self, sensor_id, input = None):

        if not sensor_id in self.sensor_dependencies:
            return self.sensor_data[sensor_id]

        if input is not None:

            self.trigger_query(sensor_id, input)
            return self.sensor_data[sensor_id]
        
        raise Exception()

    def trigger_query(self, sensor_id, query_info):
        for sensor in self.query_sensors:
            
            if sensor.id == sensor_id:
                result = sensor.query_sensor(query_info)
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
    
 
    