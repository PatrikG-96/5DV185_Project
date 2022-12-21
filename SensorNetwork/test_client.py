from twisted.internet.protocol import Protocol, ClientFactory
from twisted.internet import reactor, defer, task
from time import sleep
import json
import imageio as iio
import base64
import PIL
path = "C:/Users/shirt/5DV185_Project/SensorNetwork/src"

class TestProtocol(Protocol):
    
    def __init__(self, factory):
        self.factory = factory
    
    def dataReceived(self, data: bytes):
        print(data.decode())
        
        input()
        #data = {"type":0, "model_name":"threat_model", "user_id":1}
        #self.transport.write(json.dumps(data).encode())


    
    def connectionMade(self):
        print("connected")
        super().connectionMade()
        image = iio.v3.imread(path + "/test1_success.png")
        imbytes = iio.v3.imwrite("<bytes>", image, extension=".png")
        #print(imbytes)
        b64 = base64.encodebytes(imbytes).decode('utf8')
        data = {"type":0, "model_name":"threat_model", "user_id":1}
        #self.transport.write(json.dumps(data).encode())
        headerlen = 10
        data = {"type":0, "model_name":"threat_model", "image": b64, "user_id":1}
        msg_string = json.dumps(data)
        length = str(len(msg_string))
        start  = str(length) +("." * (headerlen - len(length)))
        print(start)
        
        self.transport.write((start + json.dumps(data)).encode())
    
    def connectionLost(self, reason):
        print("disconnected")
        return super().connectionLost(reason)
    
class TestFactory(ClientFactory):
    
    protocol = TestProtocol
    
    def __init__(self):
        pass

    def buildProtocol(self, addr):
        return TestProtocol(self)

def connectToServer():
    ip = 'localhost'
    port = 1337

    reactor.connectTCP(ip, port, TestFactory())
    reactor.run()

connectToServer()
