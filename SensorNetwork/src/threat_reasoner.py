from framework.reasoner import Reasoner
import logging

class ThreatReasoner(Reasoner):

    def __init__(self, ontology) -> None:
        super().__init__(ontology)

    def reason(self, data: dict):
        
        logging.debug(f"Performing reasoning on data: '{data}'")
        
        return "reasoned"