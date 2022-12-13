from .sensor_base import Sensor, QuerySensor, ActiveSensor
import logging

log = logging.getLogger()

class SensorNetwork:
    """
    Represents a set of sensors along with methods to access their data
    """

    def __init__(self) -> None:
        self.active_sensors : list[ActiveSensor] = []
        self.query_sensors : list[QuerySensor] = []
        self.sensor_data = {}

    def add_sensor(self, sensor : Sensor) -> None:
        """
        Adds a Sensor to the SensorNetwork

        Parameters:
            sensor (Sensor) : an instance of a Sensor subclass
        """
        log.debug(f"Adding sensor '{sensor.id}'")
        
        self.sensor_data[sensor.id] = {}

        if isinstance(sensor, ActiveSensor):
 
            self.active_sensors.append(sensor)
            sensor.callback = self.__insert_data
        else:
            self.query_sensors.append(sensor)


    def __insert_data(self, sensor_id : int, sensor_data : dict) -> None:

        # BEWARE, race conditions and shit

        self.sensor_data[sensor_id] = sensor_data



    async def get_data(self, sensor_id : int, input : dict = None) -> dict:
        """
        Gets the most recent data from the specified Sensor

        Parameters:
            sensor_id (int) : id of the sensor
            input (dict) : a dictionary containing input data for a QuerySensor, None if sensor is not a QuerySensor

        Returns:
            dictionary containing all the sensor data
        """
        log.debug(f"Getting data for sensor '{sensor_id}', input: {input}")

        if input is not None:

            await self.__trigger_query(sensor_id, input)       
        
        return self.sensor_data[sensor_id]

    async def __trigger_query(self, sensor_id : int, query_input : dict) -> None:
        """
        Queries a Sensor and updates its sensor data representation

        Parameters:
            sensor_id (int) : id of the sensor
            query_input (dict) : a dictionary containing input data for the query
        """

        log.debug("Finding query sensor")

        for sensor in self.query_sensors:
            
            if sensor.id == sensor_id:
                log.debug("Found sensor, performing query")
                
                result = await sensor.query_sensor(query_input)
    
                log.debug("Query done")
                self.sensor_data[sensor_id] = result
                return
        raise Exception()


    def connect_all(self) -> None:
        """
        Connects all sensors
        """
        for a_s in self.active_sensors:
            a_s.connect()
        for q_s in self.query_sensors:
            q_s.disconnect()

    def disconnect_all(self) -> None:
        """
        Disconnects all sensors
        """
        for a_s in self.active_sensors:
            a_s.disconnect()
        for q_s in self.query_sensors:
            q_s.disconnect()

    def start(self) -> None:
        """
        Starts all sensors
        """
        for a_s in self.active_sensors:
            a_s.start()
        for q_s in self.query_sensors:
            q_s.start()

    def stop(self) -> None:
        """
        Stops all sensors
        """
        for a_s in self.active_sensors:
            a_s.stop()
        for q_s in self.query_sensors:
            q_s.stop()
