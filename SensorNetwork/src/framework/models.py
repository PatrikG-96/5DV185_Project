from abc import ABC, abstractmethod
from sensor_network import SensorNetwork
 
class Model(ABC):

    def __init__(self) -> None:
        self.data = {}
        super().__init__()

    def clear(self):
        self.data = {}

    @abstractmethod
    async def fill_sensor_data(self, sensor_network : SensorNetwork):
        raise NotImplementedError()

