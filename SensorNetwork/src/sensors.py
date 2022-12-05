from framework.sensor_base import SingleRequestApiSensor, MultiRequestApiSensor, RecognitionSensor

class RegistrationPlateSensor(RecognitionSensor):

    def __init__(self, id: int, model):
        super().__init__(id, model)

    def predict(self, input):
        return self.model.predict(input)

class RegistrationNameSensor(SingleRequestApiSensor):

    def __init__(self, id, url):
        super().__init__(id, url)

    async def query_sensor(self, query_string):
        api_result =  await super().query_sensor(query_string)
        
        # here we need to filter out some data

        return api_result


class ThreatInformationSensor(MultiRequestApiSensor):

    def __init__(self, id):
        super().__init__(id)

    async def query_sensor(self, query_strings: list[str]):
        api_result =  await super().query_sensor(query_strings)

        # filter result

        return api_result