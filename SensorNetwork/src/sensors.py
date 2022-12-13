from framework.sensor_base import SingleRequestApiSensor, MultiRequestApiSensor, RecognitionSensor
import logging

class RegistrationPlateSensor(RecognitionSensor):

    def __init__(self, id: int, model):
        super().__init__(id, model)


class RegistrationNameSensor(SingleRequestApiSensor):

    def __init__(self, id, url):
        super().__init__(id, url)

    async def query_sensor(self, query_string):
        logging.debug("Query for name...")
        api_result =  await super().query_sensor(query_string)
        
        # here we need to filter out some data
        logging.debug("Query done")
        return api_result


class ThreatInformationSensor(MultiRequestApiSensor):

    def __init__(self, id, urls):
        super().__init__(id, urls)

    async def query_sensor(self, query_strings):

        logging.debug("Query for threat information...")

        if isinstance(query_strings, list):
            api_result = await super().query_sensor(query_strings)
        elif isinstance(query_strings, str):
            api_result = await super().query_sensor([query_strings]*len(self.urls))

        # filter result
        logging.debug("Query done")

        return api_result