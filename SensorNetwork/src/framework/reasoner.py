from abc import ABC, abstractmethod

class Reasoner(ABC):

    def __init__(self, ontology) -> None:
        super().__init__()
        self.onto = ontology

    @abstractmethod
    def reason(self, data : dict) -> dict:
        raise NotImplementedError()