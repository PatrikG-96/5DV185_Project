
from .sensor_network import SensorNetwork
from .models import Model
from asyncio import StreamReader, StreamWriter, start_server, run
from .schemas import prediction_request, prediction_response, user_request, user_response, message_schema
import json
from enum import Enum
import logging
import base64
import numpy as np
import cv2
import io
from PIL import Image
import imutils
            
ADDR = '0.0.0.0'
PORT = 1337

log = logging.getLogger()

class MessageType(Enum):
    USER_REQUEST = 0,
    USER_RESPONSE = 1

class Service:

    def __init__(self, sn : SensorNetwork) -> None:
        log.debug('Creating service')
        self.sn = sn
        self.models : dict[str, Model]= {} 
        self.is_running = False

    
    def add_model(self, name : str, model : Model) -> None:
        """
        Adds a model to the Service
        """
        log.debug('Adding model')
        self.models[name] = model
     
    async def __test(self, reader : StreamReader, writer):
        
        data = bytearray()
        i = 0
        print("connected")
        
        header = (await reader.readexactly(10)).decode("utf8")
        
        size = int(header.replace('.', ''))
        
        chunk_size = 1024
        
        chunks = round(size/chunk_size + 0.5)
        
        print(f"{chunks} chunks")
        
        for i in range(chunks):
            #print("waiting...")
            braw = await reader.read(1024)
            #print("reading chunk")
            data += braw
        
        try:
            decoded = data.decode()
            msg = json.loads(decoded)        
            decoded_image = base64.b64decode(msg['image'])
            image = Image.open(io.BytesIO(decoded_image))
            opencvImage = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            im = opencvImage.astype("uint8")
            im = imutils.resize(im, width=600)
            
            msg['image'] = im
    
        except Exception as e:
            print(e)
        
        return msg

    async def __handle_user(self, reader : StreamReader, writer : StreamWriter) -> None:
        """
        Client handler for asyncio start_server method
        """

        log.debug('Handling client...')
        print("connected")
        
        msg = None

        while msg != "quit":

            log.debug("Waiting for user request...")

            #raw = (await reader.read(1024)).decode('utf8')

            msg = await self.__test(reader, writer)
            
            #errors = message_schema.validate(msg)
            errors = False

            if errors:
                log.debug(f"Failed to validate user request with errors: '{errors}'")
                pass
                #handle error

            

            type =  msg['type']
            print(type, MessageType.USER_REQUEST.value)
            if int(type) in MessageType.USER_REQUEST.value:
                
                
                #errors = user_request.validate(msg)
                errors = False

                if errors:
                    log.debug(f"Failed to validate user request with errors: '{errors}'")
                    pass
                    #handle error

                model_name = msg['model_name']

                model = self.models[model_name]

                log.debug("Filling model with sensor data...")

          
                await model.fill_sensor_data(msg, self.sn)
           

                result = model.perform_reasoning()

                log.debug(f"Model reasoning: {result}")

                json_result = json.dumps(result)
                
                writer.write(json_result.encode())
                #writer.write("hej".encode())
                await writer.drain()


      

    async def start(self) -> None:
        log.debug('Starting service')
        self.is_running = True
        self.sn.connect_all()
        self.sn.start()
        server = await start_server(self.__handle_user, ADDR, PORT)
        async with server:
            await server.serve_forever()
            log.debug('Service online')