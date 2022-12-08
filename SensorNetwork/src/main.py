from threat_model import ThreatRecognitionModel, THREAT_ID, REG_NAME_ID, REG_PLATE_ID, SensorNetwork
from sensors import RegistrationNameSensor, RegistrationPlateSensor, ThreatInformationSensor
from framework.service import Service
from threat_reasoner import ThreatReasoner
from regplate_recoginition import RegPlateRecognition
import logging
import asyncio

URL_API = "http://127.0.0.1:5000"

async def main():

    logging.basicConfig(level=logging.DEBUG)

    model = ThreatRecognitionModel(ThreatReasoner(None))

    sn = SensorNetwork()

    reg_plate = RegistrationPlateSensor(REG_PLATE_ID, RegPlateRecognition())
    suspect_name = RegistrationNameSensor(REG_NAME_ID, URL_API+"/regplate")
    threat_data = ThreatInformationSensor(THREAT_ID, [URL_API+"/criminal", URL_API+"/gunowner"])

    sn.add_sensor(reg_plate)
    sn.add_sensor(suspect_name)
    sn.add_sensor(threat_data)

    service = Service(sn)

    service.add_model("threat_model", model)

    await service.start()


if __name__ == "__main__":

    asyncio.run(main())