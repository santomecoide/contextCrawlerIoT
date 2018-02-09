from bluetooth.ble import BeaconService
from bluetooth.ble import DiscoveryService

class Beacon(object):
    def __init__(self):
        self.uuid = None
        self.major = None
        self.minor = None
        self.address = None
        self.name = None

        self.discovery_service = DiscoveryService()
        self.beacon_service = BeaconService()

    def __get_rssi(self, raw_data):
        return raw_data[4]

    def __put_data(self, data):
        self.uuid = data[0]
        self.major = data[1]
        self.minor = data[2]

    def get_url(self):
        split_name = self.name.split('_')
        url = split_name[0] + "." + str(int(split_name[1]))
        return url

    def is_beacon_ready(self):
        if self.name != None:
            return True
        return False

    def scanTask(self):
        devices = self.beacon_service.scan(3)
        for address, data in list(devices.items()):
            if self.__get_rssi(data) >= -40:
                near_devices = self.discovery_service.discover(3)
                for near_address, name in list(near_devices.items()):
                    if near_address == address:
                        self.name = name
                        self.address = address
                        self.__put_data(data)
                        return
