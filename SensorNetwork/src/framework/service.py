from .sensor_base import SensorType
from sensor_network import SensorNetwork
from protocol import MessageType, Protocol
from models import Model
import asyncio
from schemas import prediction_request, prediction_response, user_request, user_response, message_schema
import json

            
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
        self.sn = sn
        self.models : dict[str, Model]= {} 
        self.reasoners : dict[str, asyncio.StreamWriter] = {}
        self.clients : dict[str, Client] = {}
        self.is_running = False

    
    def add_model(self, name, model):
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

        #################################
        #            Start 1            #
        #################################
        
        msg = None

        # generate id
        id = 1

        self.clients[id] = Client(id, reader, writer)

        while msg != "quit":

            raw = (await reader.read(255)).decode('utf8')

            errors = message_schema.validate(raw)

            if errors:
                pass
                #handle error

            msg = json.loads(raw)

            type =  msg['type']

            if type == MessageType.USER_REQUEST:
                
                errors = user_request.validate(msg)

                if errors:
                    pass
                    #handle error

                model_name = msg['model_name']

                model = self.models[model_name]

                await model.fill_sensor_data(self.sn)

                result = model.data

                ################################
                #            Start 2           #
                ################################
                # generate sequence number
                seq = Protocol.seq()

                pred_req = {'type' : MessageType.PREDICTION_REQUEST,'client' : id, 'seq' : seq, 'data' : result}

                rwriter = self.reasoners[model_name]

                rwriter.write(json.dumps(pred_req).encode('utf-8'))

  


      

    async def start(self):
        self.is_running = True
        server = await asyncio.start_server(self.__handle_user, ADDR, PORT)
        async with server:
            await server.serve_forever()