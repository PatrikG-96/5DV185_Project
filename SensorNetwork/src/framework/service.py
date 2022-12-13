
from .sensor_network import SensorNetwork
from .models import Model
from asyncio import StreamReader, StreamWriter, start_server, run
from .schemas import prediction_request, prediction_response, user_request, user_response, message_schema
import json
from enum import Enum
import logging

            
ADDR = 'localhost'
PORT = 1337

log = logging.getLogger()

class MessageType(Enum):
    USER_REQUEST = 0

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
     

    async def __handle_user(self, reader : StreamReader, writer : StreamWriter) -> None:
        """
        Client handler for asyncio start_server method
        """

        log.debug('Handling client...')
        print("connected")



        msg = None

        while msg != "quit":

            log.debug("Waiting for user request...")

            raw = (await reader.read(255)).decode('utf8')

            writer.write("hej".encode())

            if reader.at_eof():
                break

            log.debug(f"Recieved user request : '{raw}'")

            try:
                msg = json.loads(raw)
            except:
                print("not json")
                continue

            errors = message_schema.validate(msg)

            if errors:
                log.debug(f"Failed to validate user request with errors: '{errors}'")
                pass
                #handle error

            

            type =  msg['type']
            if int(type) == MessageType.USER_REQUEST.value:
                
                errors = user_request.validate(msg)

                if errors:
                    log.debug(f"Failed to validate user request with errors: '{errors}'")
                    pass
                    #handle error

                model_name = msg['model_name']

                model = self.models[model_name]

                log.debug("Filling model with sensor data...")

          
                await model.fill_sensor_data(self.sn)
           

                result = model.perform_reasoning()

                log.debug(f"Model reasoning: {result}")

                writer.write(result.encode())
                await writer.drain()


      

    async def start(self) -> None:
        log.debug('Starting service')
        self.is_running = True
        server = await start_server(self.__handle_user, ADDR, PORT)
        async with server:
            await server.serve_forever()
            log.debug('Service online')