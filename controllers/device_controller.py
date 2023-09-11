import requests

class DeviceController:
    def __init__(self, portal_host):
        self._portal_url = 'http://' + portal_host

    def send_room_device_control(self, args):
        hotel_name = args.get("hotel_name")
        room_number = args.get("room_number")
        room_device = args.get("room_device")
        room_device_param = args.get("room_device_param")
        room_device_value = args.get("room_device_value")

        ret = "Failed to send the command to the device"

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
                            url = self._portal_url + "/rooms/" + str(room_id) +  "/control/" + room_device
                            response = requests.post(url, {'param' : room_device_param, 'value' : room_device_value })
                            if response.status_code == 201:
                                ret = "Successfully sent the command to the device"

        return ret

    def _get_entities(self, path):
        ret = []
        response = requests.get(self._portal_url + '/' + path)
        if response.status_code == 200:
            ret = response.json()['data']
        return ret