from framework.reasoner import Reasoner
from ontology_interface import *
import logging

class ThreatReasoner(Reasoner):
    
    ASP_WEIGHT = 1/4

    def __init__(self, ontology_path) -> None:
        ontology = loadOntology(ontology_path)
        super().__init__(ontology)

    def reason(self, data: dict):
        """_summary_
        
        "license_plate"
        "asp"
        "criminal_record"
        "gun_ownership"
        "stolen"
        
        Args:
            data (dict): _description_
        """
        logging.debug(f"Performing reasoning on data: '{data}'")
        
        license_plate = data["license_plate"]
        
        setCurrentNumberPlate(self.onto, license_plate)
        syncReasoner()
        
        stolen = getNumberPlateThreatLevels(self.onto, license_plate)
        
        
        if len(stolen) > 0:
            
            return stolen[0][0]
            
        
        criminal = getCriminalRecordThreatEstimate(self.onto, license_plate)
        
        if len(criminal) > 0:
            
            result = max(criminal, key = lambda x : x[0])
                
            return result[0]
                
            
        
        asp = getASPThreatLevels(self.onto, license_plate)
        
        if len(asp) > 0:
            
            result = max(asp) * ThreatReasoner.ASP_WEIGHT
            
            return result
        
        return 0
        
            
        
        
        
        
        
