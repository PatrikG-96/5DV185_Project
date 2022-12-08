from twisted.internet.protocol import Protocol, ClientFactory
from twisted.internet import reactor, defer, task
from time import sleep
import json


class TestProtocol(Protocol):
    
    def __init__(self, factory):
        self.factory = factory
    
    def dataReceived(self, data: bytes):
        print(data.decode())
        


    
    def connectionMade(self):
        print("connected")
        super().connectionMade()
        data = {"type":0, "model_name":"threat_model", "user_id":1}
        self.transport.write(json.dumps(data).encode())
    
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
