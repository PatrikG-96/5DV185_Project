from src.framework.service import Service
import asyncio
from src.framework.sensor_network import SensorNetwork

def main():
    
    sn = SensorNetwork()
    service = Service(sn)

    asyncio.run(service.run())
    pass
