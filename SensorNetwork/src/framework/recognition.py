from abc import ABC, abstractmethod

class Recognition(ABC):

    @abstractmethod
    def predict(self, data):
        raise NotImplementedError()