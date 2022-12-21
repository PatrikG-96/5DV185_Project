from threat_model import ThreatRecognitionModel, THREAT_ID, REG_NAME_ID, REG_PLATE_ID, SensorNetwork
from sensors import RegistrationNameSensor, RegistrationPlateSensor, ThreatInformationSensor
from framework.service import Service
from threat_reasoner import ThreatReasoner
from regplate_recoginition import RegPlateRecognition, ANPR, cv2, imutils
#from yolov4 import alpr
import logging
import asyncio


URL_API = "http://127.0.0.1:5000"
path = "C:/Users/shirt/5DV185_Project/SensorNetwork/src"

async def main():

    logging.basicConfig(level=logging.DEBUG)

    model = ThreatRecognitionModel(ThreatReasoner(path+"/ontology.owl"))

    sn = SensorNetwork()

    reg_plate = RegistrationPlateSensor(REG_PLATE_ID, RegPlateRecognition())
    suspect_name = RegistrationNameSensor(REG_NAME_ID, URL_API+"/regplate")
    threat_data = ThreatInformationSensor(THREAT_ID, [URL_API+"/criminal", URL_API+"/gunowner", URL_API+"/asp"])

    sn.add_sensor(reg_plate)
    sn.add_sensor(suspect_name)
    sn.add_sensor(threat_data)

    service = Service(sn)

    service.add_model("threat_model", model)

    await service.start()

    # anpr = ANPR(debugMode=True)

    # image = cv2.imread(path+"/test1_success.png")

    # image = image.astype('uint8')

    # image = imutils.resize(image, width=600)

    # text = anpr.find_license_plate(image, clear_border=False)

    # print(text)

    # config_path = "C:/Users/shirt/5DV185_Project/SensorNetwork/data/yolo4-obj.cfg"
    # data_path = "C:/Users/shirt/5DV185_Project/SensorNetwork/data/obj.data"
    # weight_path = "C:/Users/shirt/5DV185_Project/SensorNetwork/data/yolo4-obj_best.weights"
    # image_path = "C:/Users/shirt/5DV185_Project/SensorNetwork/data/test_car.jpg"
    # batch_size = 1
    # thresh = 0.6

    # alpr(image_path, config_path, data_path, weight_path, batch_size, thresh)



if __name__ == "__main__":

    asyncio.run(main())