import unittest
from time import sleep
from test.endpoints import TestHttpClient, TestEndpoint
from test.test_sensors import TestApiSensor, TestActiveSensor, TestBasicQuerySensor, SensorType
from src.sensor_network import SensorNetwork, QueryChain, Link

class ApiSensorTests(unittest.TestCase):

    def test_request(self):

        data = {"value" : 1}
        netlocation = "www.test.com"
        path = "/data"

        client = TestHttpClient()
        endpoint = TestEndpoint(netlocation)
        endpoint.add_route(path, data)
        client.add_endpoint(endpoint)

        sensor = TestApiSensor(1, netlocation + path, client.get)

        result = sensor.query_sensor("")

        self.assertEqual(data, result)

class ActiveSensorTests(unittest.TestCase):

    ignore = False

    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)
        self.test_variable = 0

    def __sensor_cb(self, value):
        self.test_variable = value["value"]

    def test_frequency(self):

        if ActiveSensorTests.ignore:
            return

        frequency = 2
        max_value = 10
        leeway = 1
        
        sensor = TestActiveSensor(1, frequency, max_value)
        sensor.callback = self.__sensor_cb
        sensor.connect()
        sensor.start()

        sleep(max_value/frequency + leeway)

        self.assertEqual(max_value, self.test_variable)

        self.test_variable = 0

class SensorNetworkTests(unittest.TestCase):

    def test_handle_dependency(self):

        dictkey = "val"
        d1 = 2
        d2 = 3
        d3 = 4

        sn = SensorNetwork()

        s1 = TestBasicQuerySensor(1, dictkey, d1)
        s2 = TestBasicQuerySensor(2, dictkey, d2)
        s3 = TestBasicQuerySensor(3, dictkey, d3)

        sn.add_sensor(s1)
        sn.add_sensor(s2)
        sn.add_sensor(s3)

        chain = QueryChain()
        l1 = Link()
        l1.add_fixed(1, SensorType.QUERY, {dictkey : d1})
        l2 = Link()
        l2.add_dependency(2, SensorType.QUERY, 1)
        l3 = Link()
        l3.add_dependency(3, SensorType.QUERY, 2)

        chain.add_link(l1)
        chain.add_link(l2)
        chain.add_link(l3)

      

        result = sn.execute_query_chain(chain)



        self.assertEqual(result[3][dictkey], 2*d1+d2+d3)


    def test_sensor_dependency(self):
        pass

    def test_sensor_combination(self):
        pass

    def test_multiple_concurrent_sensors(self):
        pass


if __name__ == "__main__":
    ActiveSensorTests.ignore = True
    unittest.main()