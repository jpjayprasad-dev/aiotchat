import requests
import pandas as pd

class SensorController:
    def __init__(self, portal_host):
        self._portal_url = 'http://' + portal_host

    def get_room_sensor_data(self, args):
        hotel_name = args.get("hotel_name")
        room_number = args.get("room_number")
        room_sensor = args.get("room_sensor")
        timespan = args.get("timespan")

        data = []

        hotels =  self._get_entities('hotels')
        for hotel in hotels:
            if hotel_name.lower() == hotel['name'].lower():
                hotel_id = hotel['id']
                floors = self._get_entities('hotels/' + str(hotel_id) + '/floors')
                for floor in floors:
                    floor_id = floor['id']
                    rooms= self._get_entities('floors/' + str(floor_id) + '/rooms')
                    for room in rooms:
                        if room_number.lower() == room['number'].lower():
                            room_id = room['id']
                            if timespan:
                                timespan_in_seconds = timespan * 60 *60
                                response = requests.request('GET', self._portal_url + '/rooms/' + str(room_id) + '/data/' + room_sensor, json={"timespan" : str(timespan_in_seconds)})
                            else:
                                response = requests.request('GET', self._portal_url + '/rooms/' + str(room_id) + '/data/' + room_sensor)
                            if response.status_code == 200:
                                records = response.json().get('data')
                            
                                for record in records:
                                    sensor_name = record["device_parameter_id"]["device_id"]["name"]
                                    param = record["device_parameter_id"]["param"]
                                    value = record["value"]
                                    room_id = record["room_id"]["id"]
                                    data.append({ "room_number" : room_number, "sensor_name" : sensor_name, "parameter" : param, "value": value })
        if data:
            df = pd.DataFrame(data)
            return df.to_csv(index=False)

        return



    def _get_entity_id(self, entity_type, entity_name):
        id = None
        response = requests.get(self._portal_url + '/' + entity_type + '/' + entity_name)
        if response.status_code == 200:
            id = response.json()['data'][0]['id']
        
        return id

    def _get_entities(self, path):
        ret = []
        response = requests.get(self._portal_url + '/' + path)
        if response.status_code == 200:
            ret = response.json()['data']
        return ret

    
