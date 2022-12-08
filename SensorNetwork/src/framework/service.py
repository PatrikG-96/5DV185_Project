from .sensor_base import SensorType
from .sensor_network import SensorNetwork
from .protocol import MessageType, Protocol
from .models import Model
import asyncio
from .schemas import prediction_request, prediction_response, user_request, user_response, message_schema
import json
import logging

            
ADDR = 'localhost'
PORT = 1337

class Client:

    def __init__(self, id, reader : asyncio.StreamReader, writer : asyncio.StreamWriter):
        self.id = id
        self.reader = reader
        self.writer = writer
        self.data = {}

    def queue_data(self, data, seq):
        self.data[seq] = data

    def pop(self, seq):
        return self.data[seq]

class Service:

    def __init__(self, sn : SensorNetwork):
        logging.debug('Creating service')
        self.sn = sn
        self.models : dict[str, Model]= {} 
        self.clients : dict[str, Client] = {}
        self.is_running = False

    
    def add_model(self, name, model):
        logging.debug('Adding model')
        self.models[name] = model

    async def connect_reasoner(self, name, host, port):

        if not self.is_running:
            return

        reader, writer = asyncio.open_connection(host, port)

        self.reasoners[name] = writer

        await self.__handle_reasoner(reader, writer)

    async def __handle_reasoner(self, reader: asyncio.StreamReader, writer : asyncio.StreamWriter):

        msg = None

        while msg != "quit":

            ################################
            #            Start 3           #
            ################################

            raw = (await reader.read(255)).decode('utf8')

            msg = json.loads(raw)

            errors = message_schema.validate(msg)

            if errors:
                pass
                #handle error

            
            type =  msg['type']

            if type == MessageType.PREDICTION_RESPONSE:

                errors = prediction_response.validate(msg)

                if errors:
                    pass
                    #handle error

                ################################
                #            Start 4           #
                ################################

                client = self.clients[msg['client']]
                seq = msg['seq']
                response = {'seq' : seq, 'prediction' : msg['prediction'], 'optional': client.pop(seq), 'type' : MessageType.USER_RESPONSE}

                client.writer.write(json.dumps(response).encode('utf-8'))

                

    async def __handle_user(self, reader, writer):


        logging.debug('Handling client...')
        msg = None

        # generate id
        id = 1

        logging.debug(f'Assigning user id: {id}')

        self.clients[id] = Client(id, reader, writer)

        empty = b''

        while msg != "quit":

            logging.debug("Waiting for user request...")
            raw = (await reader.read(255)).decode('utf8')

            if reader.at_eof():
                break

            logging.debug(f"Recieved user request : '{raw}'")

            msg = json.loads(raw)

            errors = message_schema.validate(msg)

            if errors:
                logging.debug(f"Failed to validate user request with errors: '{errors}'")
                pass
                #handle error

            

            type =  msg['type']
            if int(type) == MessageType.USER_REQUEST.value:
                
                errors = user_request.validate(msg)

                if errors:
                    logging.debug(f"Failed to validate user request with errors: '{errors}'")
                    pass
                    #handle error

                model_name = msg['model_name']

                model = self.models[model_name]

                logging.debug("Filling model with sensor data...")

          
                await model.fill_sensor_data(self.sn)
           

                result = model.perform_reasoning()

                logging.debug(f"Model reasoning: {result}")

                writer.write(result.encode())
                await writer.drain()


      

    async def start(self):
        logging.debug('Starting service')
        self.is_running = True
        server = await asyncio.start_server(self.__handle_user, ADDR, PORT)
        async with server:
            await server.serve_forever()
            logging.debug('Service online')