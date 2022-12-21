from framework.models import Model, SensorNetwork
import logging

REG_PLATE_ID = 1
REG_NAME_ID = 2
THREAT_ID = 3


class ThreatRecognitionModel(Model):

    def __init__(self, reasoner) -> None:
        super().__init__(reasoner)

    async def fill_sensor_data(self, msg, sensor_network: SensorNetwork):
        
        logging.debug("Filling sensor data!")
        # should get image from camera here?
        result = {}
        image = msg['image']
        try:
            reg_number = await sensor_network.get_data(REG_PLATE_ID, {'image' : image})
            result["license_plate"] = reg_number
            logging.debug(f"Registration number: {reg_number}")
            registration = await sensor_network.get_data(REG_NAME_ID, {'number':reg_number})
            suspect_name = registration['owner']
            result.update(registration)
            logging.debug(f"Registration: {registration}")
            forms = [{'name' : suspect_name}]*3
            threat_data = await sensor_network.get_data(THREAT_ID, forms)
            result.update(threat_data)
        except Exception as e:
            print(e)
            return

        # filter
        
        logging.debug(f"Data found: '{result}'")

        self.data = result

    def perform_reasoning(self):
        prediction =  self.reasoner.reason(self.data)
        result = self.data.copy()
        result.update({'prediction' : prediction})
        return result
        
        