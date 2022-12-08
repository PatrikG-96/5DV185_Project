from framework.models import Model, SensorNetwork
import logging

REG_PLATE_ID = 1
REG_NAME_ID = 2
THREAT_ID = 3


class ThreatRecognitionModel(Model):

    def __init__(self, reasoner) -> None:
        super().__init__(reasoner)

    async def fill_sensor_data(self, sensor_network: SensorNetwork):
        
        logging.debug("Filling sensor data!")
        # should get image from camera here?
        image = "image"
        try:
            reg_number = await sensor_network.get_data(REG_PLATE_ID, image)
            logging.debug(f"Registration number: {reg_number}")
            suspect_name = await sensor_network.get_data(REG_NAME_ID, {'number':reg_number})
            logging.debug(f"Registration name: {suspect_name}")
            forms = [{'name' : suspect_name}]*2
            threat_data = await sensor_network.get_data(THREAT_ID, forms)
        except:
            print("e")

        # filter
        logging.debug(f"Data filled: '{threat_data}'")

        self.data = threat_data

    def perform_reasoning(self):
        return self.reasoner.reason(self.data) + str(self.data)
        