from .sensor_base import SensorType
from sensor_network import SensorNetwork

class Link:

    def __init__(self) -> None:
        self.input = []
        self.sensor_id = []
        self.sensor_type = []
        self.output = []

    def add(self, input_type, sensor_id, sensor_type, output):
        self.input.append(input_type)
        self.sensor_id.append(sensor_id)
        self.sensor_type.append(sensor_type)
        self.output.append(output)

    def length(self):
        return len(self.input)

class SensorDependencyChain:

    INPUT = 0
    PREV = 1

    def __init__(self) -> None:
        self.links = []

    def add_link(self, link):
        self.links.append(link)

    def execute_chain(self, sn : SensorNetwork):

        output = []

        for link in self.links:

            


class Service:

    def __init__(self):
        pass

    
    def add_chain(self, chain):
        pass