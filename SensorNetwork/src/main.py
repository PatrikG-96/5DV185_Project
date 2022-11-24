from query_sensors import RegPlateSensor
from test_sensors import IncrementalValue, TestQuery
from sensor_network import SensorNetwork
from time import sleep

def print2(dic):
    value = dic["value"]
    print(value)

if __name__ == "__main__":
    
    # test = IncrementalValue("1")
    

    test = TestQuery(1)
    test2 = IncrementalValue(2)

    sn = SensorNetwork()
    sn.add_sensor(test)
    sn.add_sensor(test2)
    sn.connect_all()
    sn.start()

    i = 0
    while True:
        i+=1
        sn.trigger_query(1, i%6)
        print("\n----------------------\n", sn.get_data(1)["value"], sn.get_data(2)["value"],"\n----------------------\n")
        sleep(1)

