from abc import ABC, abstractmethod
from .sensor_network import SensorNetwork
from .reasoner import Reasoner
 
class Model(ABC):

    def __init__(self, reasoner : Reasoner) -> None:
        self.data = {}
        self.reasoner = reasoner
        super().__init__()

    def clear(self):
        self.data = {}

    @abstractmethod
    async def fill_sensor_data(self, sensor_network : SensorNetwork):
        raise NotImplementedError()

    @abstractmethod
    def perform_reasoning(self):
        raise NotImplementedError()

