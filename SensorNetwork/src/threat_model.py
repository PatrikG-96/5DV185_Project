from framework.models import Model, SensorNetwork

REG_PLATE_ID = 1
REG_NAME_ID = 2
THREAT_ID = 3


class ThreatRecognitionModel(Model):

    def __init__(self) -> None:
        super().__init__()
        self.data = {}

    async def fill_sensor_data(self, sensor_network: SensorNetwork, image):
        
        reg_number = await sensor_network.get_data(REG_PLATE_ID, image)
        suspect_name = await sensor_network.get_data(REG_NAME_ID, reg_number)
        threat_data = await sensor_network.get_data(THREAT_ID, suspect_name)

        # filter

        self.data = threat_data
        