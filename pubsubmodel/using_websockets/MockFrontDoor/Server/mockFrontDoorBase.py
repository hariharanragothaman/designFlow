import json

class MockFrontDoorBase(object):
    current_volume = 30
    wifiData = {"wifiScanResult": [{
        "frequencyKhz": "2412000",
        "security": "WPA_OR_WPA2",
        "signalDbm": "-27",
        "ssid": "B-PRODUCT"
    }]}

    def parser(self, jsonMessage):
        resource = jsonMessage['header']["resource"].replace('/', '_')
        jsonMessage['header']['msgtype'] = 'RESPONSE'
        try:
            getattr(self, resource)(jsonMessage)
        except AttributeError:
            self.logger.error("%s not implemented" % resource)
            jsonMessage.pop('body', None)
            jsonMessage['header']['status'] = 500
            jsonMessage['error'] = {
                "GUID": "1",
                "code": 1,
                "message": "WEBSOCKET_API_NOT_REGISTERED",
                "subcode": 2002
            }
        return jsonMessage
    
    def _startDiscoveryAdvertisement(self, jsonMsg):
        self.logger.info("_startDiscoveryAdvertisement")
        if jsonMsg['header']["method"] == 'POST':
            data = json.dumps({
	                "header": {
		                "device": "1",
		                "resource": "/startDiscoveryAdvertisement",
		                "method": "POST",
		                "msgtype": "REQUEST",
		                "reqID": 45,
		                "version": 1.000000
	                },
	                "body": {
		                "deviceName": "6E3A0B HS 500",
		                "guid": "5b4c9e97-0e75-eb87-73dc-725b88c73bd4",
		                "ecosys": "ECO2",
		                "productType": "eddie",
		                "productName": "Bose Home Speaker 500",
		                "productColor": "1",
		                "softwareVersion": "5.0.7-0+d11a62e",
		                "productLanguage": "en"}}, indent=4)
            jsonMsg['body'] = json.loads(data)
            jsonMsg['header']['method'] = 'NOTIFY'
            del jsonMsg['header']['msgtype']
        return jsonMsg

    def _system_language(self, jsonMsg):
        self.logger.info("_system_language")
        data = json.dumps({"code": "en", "properties": { \
            "supported_language_codes": [ \
                "da", "de", "en-US", "es", "fr", \
                "it", "nl", "sv", "ja", "zh", \
                "ko", "th", "cs", "fi", "el", \
                "no", "pl", "pt", "ro", "ru", \
                "sl", "tr", "hu"]}}, indent=4)
        jsonMsg['body'] = json.loads(data)
        return jsonMsg

    def _system_productSourcesReady(self, jsonMsg):
        self.logger.info("_system_productSourcesReady")
        if jsonMsg['header']["method"] == 'POST':
            data = json.dumps({
                  "ready" : "true"
                }, indent=4)
            jsonMsg['body'] = json.loads(data)
            jsonMsg['header']['method'] = 'NOTIFY'
            del jsonMsg['header']['msgtype']
        return jsonMsg

    def _system_sources(self, jsonMsg):
        self.logger.info("_system_sources")
        if jsonMsg['header']["method"] == 'PUT':
            data = json.dumps({"sources" : [ {
                        "accountid" : "27a3c068-f7e0-423b-932e-692ad4316eda",
                        "details" : {
                          "activationKey" : "ACTIVATION_KEY_TV",
                          "cableProvider" : "AT&T U-verse TV",
                          "ciCode" : "T1234",
                          "deviceType" : "DEVICE_TYPE_SMART_TV",
                          "friendlyName" : "FRIENDLY_NAME_CABLE_BOX",
                          "inputRoute" : "INPUT_ROUTE_TV",
                          "parentInput" : "PARENT_INPUT_TV",
                          "sequenceNumber" : "0"
                        },
                        "displayName" : "My Playlist",
                        "local" : "false",
                        "modifiable" : "false",
                        "multiroom" : "false",
                        "sourceAccountName" : "ranjeettr@gmail.com",
                        "sourceName" : "Spotify",
                        "status" : "AVAILABLE",
                        "visible" : "false"}]}, indent=4)
            jsonMsg['body'] = json.loads(data)
            jsonMsg['header']['method'] = 'NOTIFY'
            del jsonMsg['header']['msgtype']
        return jsonMsg

    def subscription(self, jsonMsg):
        self.logger.info("subscription(")
        return jsonMsg;

    def _accessories(self, jsonMsg):
        self.logger.info("_audio_volume")
        if jsonMsg['header']["method"] == 'PUT':
            if 'value' in jsonMsg["body"]:
                _volume = int(jsonMsg["body"]["value"])
                self.current_volume = _volume
                data = json.dumps({"disbandAccessories" : false,
                                   "enabled" : {
                                     "rears" : false,
                                     "subs" : false
                                  },
                                   "pairing" : true
                                }
                                , indent=4)
                jsonMsg["body"] = json.loads(data)
            jsonMsg['header']['method'] = 'NOTIFY'
            del jsonMsg['header']['msgtype']
            self.logger.info("The notification to the client is: %s", json.dumps(jsonMsg, indent=4))
        return jsonMsg

    def _audio_defaultVolume(self, jsonMsg):
        self.logger.info("_audio_defaultVolume")
        default_volume = 30
        self.logger.info("The current default volume is: %s", default_volume)
        if jsonMsg['header']["method"] == 'POST':
            self.current_volume = default_volume
            data = json.dumps({"defaultOn": 30,
                               "min": 0,
                               "feedback":{
                                   "enable": "true"
                                   },
                               "muted": "false",
                               "max": 70,
                               "min": 30,
                               "value": self.current_volume,
                               "properties":{
                                   "maxLimit": 70,
                                   "minLimit": 30}}, indent=4)
            jsonMsg['header']['method'] = 'NOTIFY'
            jsonMsg['header']['resource'] = '/audio/volume'
            del jsonMsg['header']['msgtype']
            jsonMsg["body"] = json.loads(data)
            self.logger.info("The notification to the client is: %s", json.dumps(jsonMsg, indent=4))
        return jsonMsg


    def _ui_alive(self, jsonMsg):
        self.logger.info("UI Alive Status")
        if jsonMsg['header']["method"] == 'POST':
            jsonMsg['header']['method'] = 'NOTIFY'
            del jsonMsg['header']['msgtype']
            self.logger.info("The notification to the client is: %s", json.dumps(jsonMsg, indent=4))
        return jsonMsg

    def _audio_volume(self, jsonMsg):
        self.logger.info("_audio_volume")
        _volume = 30
        if jsonMsg['header']["method"] == 'GET':
            data = json.dumps({"value": self.current_volume}, indent=4)
            jsonMsg['body'] = json.loads(data)

        elif jsonMsg['header']["method"] == 'PUT':
            if 'value' in jsonMsg["body"]:
                _volume = int(jsonMsg["body"]["value"])
                self.current_volume = _volume
                data = json.dumps({"defaultOn": 30,
                                   "min": 30,
                                   "feedback":{
                                       "enable": "true"
                                       },
                                   "muted": "false",
                                   "max": 70,
                                   "value": self.current_volume,
                                   "properties": {
                                   "maxLimit": 70,
                                   "minLimit": 30}}, indent=4)
                jsonMsg["body"] = json.loads(data)
            
            elif 'muted' in jsonMsg["body"]:
                self.logger.info("The muted flag has been set")
                muted_flag = jsonMsg["body"]["muted"]
                self.logger.info("The muted flag is: %s", muted_flag)
                data = json.dumps({"defaultOn": 30,
                                   "min": 30,
                                   "feedback":{
                                       "enable": "true"
                                       },
                                   "muted": muted_flag,
                                   "max": 70,
                                   "value": self.current_volume,
                                   "properties": {
                                   "maxLimit": 70,
                                   "minLimit": 30}}, indent=4)
                jsonMsg["body"] = json.loads(data)

            jsonMsg['header']['method'] = 'NOTIFY'
            del jsonMsg['header']['msgtype']
            self.logger.info("The notification to the client is: %s", json.dumps(jsonMsg, indent=4))
        return jsonMsg

    def _audio_volume_increment(self, jsonMsg):
        self.logger.info("_audio_volume_increment")
        default_volume = 30
        self.logger.info("The current default volume is: %s", default_volume)
        if jsonMsg['header']["method"] == 'PUT':
            _volume = default_volume + int(jsonMsg["body"]["delta"])
            self.current_volume = _volume
            data = json.dumps({"defaultOn": 30,
                               "min": 0,
                               "feedback":{
                                   "enable": "true"
                                   },
                               "muted": "false",
                               "max": 70,
                               "min": 30,
                               "value": self.current_volume,
                               "properties":{
                                   "maxLimit": 70,
                                   "minLimit": 30}}, indent=4)
            jsonMsg['header']['method'] = 'NOTIFY'
            jsonMsg['header']['resource'] = '/audio/volume'
            del jsonMsg['header']['msgtype']
            jsonMsg["body"] = json.loads(data)
            self.logger.info("The notification to the client is: %s", json.dumps(jsonMsg, indent=4))
        return jsonMsg

    def _audio_volume_decrement(self, jsonMsg):
        self.logger.info("_audio_volume_decrement")
        default_volume = 30
        self.logger.info("The current default volume is: %s", default_volume)

        if jsonMsg['header']["method"] == 'PUT':
            _volume = default_volume - int(jsonMsg["body"]["delta"])
            self.current_volume = _volume
            data = json.dumps({"defaultOn": 30,
                               "min": 0,
                               "feedback":{
                                   "enable": "true"
                                   },
                               "muted": "false",
                               "max": 100,
                               "value": self.current_volume,
                               "properties":{
                                   "maxLimit": 70,
                                   "minLimit": 30}}, indent=4)
            jsonMsg['header']['method'] = 'NOTIFY'
            jsonMsg['header']['resource'] = '/audio/volume'
            del jsonMsg['header']['msgtype']
            jsonMsg["body"] = json.loads(data)
            self.logger.info("The notification to the client is: %s", json.dumps(jsonMsg, indent=4))
        return jsonMsg

    def _system_capsInitializationStatus(self, jsonMsg):
        self.logger.info("Getting CAPS Initialization Status")
        if jsonMsg['header']["method"] == 'GET':
            data = json.dumps({"CapsInitialized" : "true"}, indent=4)
            jsonMsg["body"] = json.loads(data)
        return jsonMsg

    def _bluetooth_sink_list(self, jsonMsg):
        self.logger.info("Getting Bluetooth Sink Status")
        if jsonMsg['header']["method"] == 'GET':
            data = json.dumps({"devices" : []}, indent=4)
            jsonMsg["body"] = json.loads(data)
        return jsonMsg

    def _bluetooth_sink_status(self, jsonMsg):
        self.logger.info("Getting Bluetooth Sink Status")
        if jsonMsg['header']["method"] == 'GET':
            data = json.dumps({"devices" : [],"status" : "APP_INACTIVE"}, indent=4)
            jsonMsg["body"] = json.loads(data)
        return jsonMsg

    def _internal_capabilities(self, jsonMsg):
        self.logger.info("_internal_capabilities")
        data = json.dumps({"capability": [
            {
                "group": "CAPS",
                "handler": "Caps",
                "resource": "/addZoneSlave",
                "scope": "PUBLIC",
                "version": 1
            },
            {
                "group": "CAPS",
                "handler": "Caps",
                "resource": "/system/capsInitializationStatus",
                "scope": "PUBLIC",
                "version": 1
            },
            {
                "group": "ProductController",
                "handler": "ProductController",
                "resource": "/audio/bass",
                "scope": "PUBLIC",
                "version": 1
            },
            {
                "group": "CAPS",
                "handler": "Caps",
                "resource": "/audio/defaultVolume",
                "scope": "PUBLIC",
                "version": 1
            },
            {
                "group": "ProductController",
                "handler": "ProductController",
                "resource": "/audio/treble",
                "scope": "PUBLIC",
                "version": 1
            },
            {
                "group": "CAPS",
                "handler": "Caps",
                "resource": "/audio/volume",
                "scope": "PUBLIC",
                "version": 1
            },
            {
                "group": "CAPS",
                "handler": "Caps",
                "resource": "/audio/volume/decrement",
                "scope": "PUBLIC",
                "version": 1
            },
            {
                "group": "CAPS",
                "handler": "Caps",
                "resource": "/audio/volume/increment",
                "scope": "PUBLIC",
                "version": 1
            },
            {
                "group": "CAPS",
                "handler": "Caps",
                "resource": "/audio/volumeMax",
                "scope": "PUBLIC",
                "version": 1
            },
            {
                "group": "CAPS",
                "handler": "Caps",
                "resource": "/audio/volumeMin",
                "scope": "PUBLIC",
                "version": 1
            },
            {
                "group": "CAPS",
                "handler": "Caps",
                "resource": "/audio/zone",
                "scope": "PUBLIC",
                "version": 1
            },
            {
                "group": "Bluetooth",
                "handler": "BLEFrontDoorClient",
                "resource": "/bluetooth/le/setupActivate",
                "scope": "PUBLIC",
                "version": 1
            },
            {
                "group": "Bluetooth",
                "handler": "BLEFrontDoorClient",
                "resource": "/bluetooth/le/setupDeactivate",
                "scope": "PUBLIC",
                "version": 1
            },
            {
                "group": "Bluetooth",
                "handler": "BLEFrontDoorClient",
                "resource": "/bluetooth/le/setupStatus",
                "scope": "PUBLIC",
                "version": 1
            },
            {
                "group": "Bluetooth",
                "handler": "BTSinkController",
                "resource": "/bluetooth/sink/connect",
                "scope": "PUBLIC",
                "version": 1
            },
            {
                "group": "Bluetooth",
                "handler": "BTSinkController",
                "resource": "/bluetooth/sink/connectionStatus",
                "scope": "PUBLIC",
                "version": 1
            },
            {
                "group": "Bluetooth",
                "handler": "BTSinkController",
                "resource": "/bluetooth/sink/disconnect",
                "scope": "PUBLIC",
                "version": 1
            },
            {
                "group": "Bluetooth",
                "handler": "BTSinkController",
                "resource": "/bluetooth/sink/list",
                "scope": "PUBLIC",
                "version": 1
            },
            {
                "group": "Bluetooth",
                "handler": "BTSinkController",
                "resource": "/bluetooth/sink/macAddr",
                "scope": "PUBLIC",
                "version": 1
            },
            {
                "group": "Bluetooth",
                "handler": "BTSinkController",
                "resource": "/bluetooth/sink/pairable",
                "scope": "PUBLIC",
                "version": 1
            },
            {
                "group": "Bluetooth",
                "handler": "BTSinkController",
                "resource": "/bluetooth/sink/remove",
                "scope": "PUBLIC",
                "version": 1
            },
            {
                "group": "Bluetooth",
                "handler": "BTSinkController",
                "resource": "/bluetooth/sink/status",
                "scope": "PUBLIC",
                "version": 1
            },
            {
                "group": "ProductController",
                "handler": "ProductController",
                "resource": "/clock",
                "scope": "PUBLIC",
                "version": 1
            },
            {
                "group": "Passport",
                "handler": "Passport",
                "resource": "/cloudSync",
                "scope": "PUBLIC",
                "version": 1
            },
            {
                "group": "CAPS",
                "handler": "Caps",
                "resource": "/content/allowSourceSelect",
                "scope": "PRIVATE",
                "version": 1
            },
            {
                "group": "CAPS",
                "handler": "Caps",
                "resource": "/content/nowPlaying",
                "scope": "PUBLIC",
                "version": 1
            },
            {
                "group": "CAPS",
                "handler": "Caps",
                "resource": "/content/nowPlaying/favorite",
                "scope": "PUBLIC",
                "version": 1
            },
            {
                "group": "CAPS",
                "handler": "Caps",
                "resource": "/content/nowPlaying/rating",
                "scope": "PUBLIC",
                "version": 1
            },
            {
                "group": "CAPS",
                "handler": "Caps",
                "resource": "/content/nowPlaying/repeat",
                "scope": "PUBLIC",
                "version": 1
            },
            {
                "group": "CAPS",
                "handler": "Caps",
                "resource": "/content/nowPlaying/shuffle",
                "scope": "PUBLIC",
                "version": 1
            },
            {
                "group": "CAPS",
                "handler": "Caps",
                "resource": "/content/playbackRequest",
                "scope": "PUBLIC",
                "version": 1
            },
            {
                "group": "CAPS",
                "handler": "Caps",
                "resource": "/content/selectLastSource",
                "scope": "PUBLIC",
                "version": 1
            },
            {
                "group": "CAPS",
                "handler": "Caps",
                "resource": "/content/selectLastStreamingSource",
                "scope": "PUBLIC",
                "version": 1
            },
            {
                "group": "CAPS",
                "handler": "Caps",
                "resource": "/content/stopPlayback",
                "scope": "PRIVATE",
                "version": 1
            },
            {
                "group": "CAPS",
                "handler": "Caps",
                "resource": "/content/transportControl",
                "scope": "PUBLIC",
                "version": 1
            },
            {
                "group": "Unknown",
                "handler": "DataCollectionService",
                "resource": "/datacollection/udc",
                "scope": "PRIVATE",
                "version": 1
            },
            {
                "group": "Unknown",
                "handler": "demo",
                "resource": "/demo",
                "scope": "PUBLIC",
                "version": 1
            },
            {
                "group": "Unknown",
                "handler": "demo",
                "resource": "/demo/chimes",
                "scope": "PUBLIC",
                "version": 1
            },
            {
                "group": "Unknown",
                "handler": "demo",
                "resource": "/demo/keyConfig",
                "scope": "PUBLIC",
                "version": 1
            },
            {
                "group": "FrontDoor",
                "handler": "FrontDoorSelfService",
                "resource": "/deregister",
                "scope": "PUBLIC",
                "version": 2
            },
            {
                "group": "Unknown",
                "handler": "GalapagosClient",
                "resource": "/galapagos/reauthenticate",
                "scope": "PRIVATE",
                "version": 1
            },
            {
                "group": "ProductActivation",
                "handler": "GalapagosClient",
                "resource": "/galapagos/services",
                "scope": "PRIVATE",
                "version": 1
            },
            {
                "group": "CAPS",
                "handler": "Caps",
                "resource": "/getZone",
                "scope": "PUBLIC",
                "version": 1
            },
            {
                "group": "FrontDoor",
                "handler": "FrontDoorSelfService",
                "resource": "/internal/capabilities",
                "scope": "PUBLIC",
                "version": 1
            },
            {
                "group": "FrontDoor",
                "handler": "FrontDoorSelfService",
                "resource": "/internal/capabilities",
                "scope": "PUBLIC",
                "version": 2
            },
            {
                "group": "FrontDoor",
                "handler": "FrontDoorSelfService",
                "resource": "/network/ping",
                "scope": "PUBLIC",
                "version": 1
            },
            {
                "group": "FrontDoor",
                "handler": "FrontDoorSelfService",
                "resource": "/network/ping",
                "scope": "PUBLIC",
                "version": 2
            },
            {
                "group": "Unknown",
                "handler": "NetworkServiceFrontDoorIF",
                "resource": "/network/status",
                "scope": "PUBLIC",
                "version": 1
            },
            {
                "group": "Unknown",
                "handler": "NetworkServiceFrontDoorIF",
                "resource": "/network/wifi/ap",
                "scope": "PUBLIC",
                "version": 1
            },
            {
                "group": "Unknown",
                "handler": "NetworkServiceFrontDoorIF",
                "resource": "/network/wifi/profile",
                "scope": "PUBLIC",
                "version": 1
            },
            {
                "group": "Unknown",
                "handler": "NetworkServiceFrontDoorIF",
                "resource": "/network/wifi/siteScan",
                "scope": "PUBLIC",
                "version": 1
            },
            {
                "group": "Unknown",
                "handler": "NetworkServiceFrontDoorIF",
                "resource": "/network/wifi/status",
                "scope": "PUBLIC",
                "version": 1
            },
            {
                "group": "FrontDoor",
                "handler": "FrontDoorSelfService",
                "resource": "/register",
                "scope": "PUBLIC",
                "version": 2
            },
            {
                "group": "CAPS",
                "handler": "Caps",
                "resource": "/removeZoneSlave",
                "scope": "PUBLIC",
                "version": 1
            },
            {
                "group": "SASS",
                "handler": "SASSControllerMain",
                "resource": "/sass/debug",
                "scope": "PUBLIC",
                "version": 1
            },
            {
                "group": "SASS",
                "handler": "SASSControllerMain",
                "resource": "/sass/error",
                "scope": "PUBLIC",
                "version": 1
            },
            {
                "group": "SASS",
                "handler": "SASSControllerMain",
                "resource": "/sass/frontingRequest",
                "scope": "PUBLIC",
                "version": 1
            },
            {
                "group": "SASS",
                "handler": "SASSControllerMain",
                "resource": "/sass/playRequest",
                "scope": "PUBLIC",
                "version": 1
            },
            {
                "group": "SASS",
                "handler": "SASSControllerMain",
                "resource": "/sass/sassToggle",
                "scope": "PUBLIC",
                "version": 1
            },
            {
                "group": "SASS",
                "handler": "SASSControllerMain",
                "resource": "/sass/stopAll",
                "scope": "PUBLIC",
                "version": 1
            },
            {
                "group": "SASS",
                "handler": "SASSControllerMain",
                "resource": "/sass/streamStatus",
                "scope": "PUBLIC",
                "version": 1
            },
            {
                "group": "CAPS",
                "handler": "Caps",
                "resource": "/setZone",
                "scope": "PUBLIC",
                "version": 1
            },
            {
                "group": "CAPS",
                "handler": "Caps",
                "resource": "/startDiscoveryAdvertisement",
                "scope": "PUBLIC",
                "version": 1
            },
            {
                "group": "ProductActivation",
                "handler": "GalapagosClient",
                "resource": "/system/activated",
                "scope": "PUBLIC",
                "version": 1
            },
            {
                "group": "Unknown",
                "handler": "GalapagosClient",
                "resource": "/system/activationArtifacts",
                "scope": "PRIVATE",
                "version": 1
            },
            {
                "group": "Unknown",
                "handler": "GalapagosClient",
                "resource": "/system/activationData",
                "scope": "PRIVATE",
                "version": 1
            },
            {
                "group": "Unknown",
                "handler": "GalapagosClient",
                "resource": "/system/activationError",
                "scope": "PRIVATE",
                "version": 1
            },
            {
                "group": "ProductActivation",
                "handler": "GalapagosClient",
                "resource": "/system/authentication",
                "scope": "PUBLIC",
                "version": 1
            },
            {
                "group": "Unknown",
                "handler": "GalapagosClient",
                "resource": "/system/authentication/productToken",
                "scope": "PRIVATE",
                "version": 1
            },
            {
                "group": "Unknown",
                "handler": "GalapagosClient",
                "resource": "/system/authenticationError",
                "scope": "PRIVATE",
                "version": 1
            },
            {
                "group": "ProductController",
                "handler": "ProductController",
                "resource": "/system/buttonEvent",
                "scope": "PUBLIC",
                "version": 1
            },
            {
                "group": "FrontDoor",
                "handler": "FrontDoorSelfService",
                "resource": "/system/capabilities",
                "scope": "PUBLIC",
                "version": 1
            },
            {
                "group": "FrontDoor",
                "handler": "FrontDoorSelfService",
                "resource": "/system/capabilities",
                "scope": "PUBLIC",
                "version": 2
            },
            {
                "group": "CAPS",
                "handler": "Caps",
                "resource": "/system/capsInitializationStatus",
                "scope": "PRIVATE",
                "version": 1
            },
            {
                "group": "ProductActivation",
                "handler": "GalapagosClient",
                "resource": "/system/challenge",
                "scope": "PUBLIC",
                "version": 1
            },
            {
                "group": "ProductController",
                "handler": "ProductController",
                "resource": "/system/configuration/status",
                "scope": "PUBLIC",
                "version": 1
            },
            {
                "group": "ProductController",
                "handler": "ProductController",
                "resource": "/system/info",
                "scope": "PUBLIC",
                "version": 1
            },
            {
                "group": "ProductController",
                "handler": "ProductController",
                "resource": "/system/language",
                "scope": "PUBLIC",
                "version": 1
            },
            {
                "group": "ProductController",
                "handler": "ProductController",
                "resource": "/system/power/control",
                "scope": "PUBLIC",
                "version": 1
            },
            {
                "group": "ProductController",
                "handler": "ProductController",
                "resource": "/system/power/timeouts",
                "scope": "PUBLIC",
                "version": 1
            },
            {
                "group": "ProductController",
                "handler": "ProductController",
                "resource": "/system/productSettings",
                "scope": "PUBLIC",
                "version": 1
            },
            {
                "group": "CAPS",
                "handler": "Caps",
                "resource": "/system/productSourcesReady",
                "scope": "PRIVATE",
                "version": 1
            },
            {
                "group": "ProductController",
                "handler": "ProductController",
                "resource": "/system/reset",
                "scope": "PUBLIC",
                "version": 1
            },
            {
                "group": "ProductController",
                "handler": "ProductController",
                "resource": "/system/setup",
                "scope": "PUBLIC",
                "version": 1
            },
            {
                "group": "CAPS",
                "handler": "Caps",
                "resource": "/system/sources",
                "scope": "PUBLIC",
                "version": 1
            },
            {
                "group": "ProductController",
                "handler": "ProductController",
                "resource": "/system/state",
                "scope": "PUBLIC",
                "version": 1
            },
            {
                "group": "Update",
                "handler": "SoftwareUpdateService",
                "resource": "/system/update/install",
                "scope": "PRIVATE",
                "version": 1
            },
            {
                "group": "Update",
                "handler": "SoftwareUpdateService",
                "resource": "/system/update/install-local",
                "scope": "PRIVATE",
                "version": 1
            },
            {
                "group": "ProductController",
                "handler": "ProductController",
                "resource": "/system/update/start",
                "scope": "PUBLIC",
                "version": 1
            },
            {
                "group": "Update",
                "handler": "SoftwareUpdateService",
                "resource": "/system/update/status",
                "scope": "PUBLIC",
                "version": 1
            },
            {
                "group": "Unknown",
                "handler": "ProductController",
                "resource": "/systemeventservice/register",
                "scope": "PUBLIC",
                "version": 1
            },
            {
                "group": "ProductController",
                "handler": "ProductController",
                "resource": "/ui/Display",
                "scope": "PUBLIC",
                "version": 1
            },
            {
                "group": "ProductController",
                "handler": "ProductController",
                "resource": "/ui/alive",
                "scope": "PUBLIC",
                "version": 1
            },
            {
                "group": "ProductController",
                "handler": "ProductController",
                "resource": "/ui/display",
                "scope": "PUBLIC",
                "version": 1
            },
            {
                "group": "Lightbar",
                "handler": "ProductController",
                "resource": "/ui/lightbar",
                "scope": "PUBLIC",
                "version": 1
            },
            {
                "group": "Unknown",
                "handler": "AVS",
                "resource": "/voice/listen",
                "scope": "PUBLIC",
                "version": 1
            },
            {
                "group": "Unknown",
                "handler": "AVS",
                "resource": "/voice/mic",
                "scope": "PUBLIC",
                "version": 1
            },
            {
                "group": "VFE",
                "handler": "VFE",
                "resource": "/vfe/mute",
                "scope": "PUBLIC",
                "version": 1
            },
            {
                "group": "Unknown",
                "handler": "AVS",
                "resource": "/voice/status",
                "scope": "PUBLIC",
                "version": 1
            },
            {
                "group": "VPAController",
                "handler": "VPAController",
                "resource": "/voice/ready",
                "scope": "PUBLIC",
                "version": 1
            },
            {
                "group": "FrontDoor",
                "handler": "FrontDoorSelfService",
                "resource": "deregister",
                "scope": "PUBLIC",
                "version": 1
            },
            {
                "group": "FrontDoor",
                "handler": "FrontDoorSelfService",
                "resource": "register",
                "scope": "PUBLIC",
                "version": 1
            }
        ]}, indent=4)
        jsonMsg['body'] = json.loads(data)
        return jsonMsg

    def _system_capabilities(self, jsonMsg):
        self.logger.info("_system_capabilities")
        data = json.dumps({"group": [
            {
                "apiGroup": "Bluetooth",
                "endpoints": [
                    {
                        "endpoint": "/bluetooth/le/setupActivate"
                    },
                    {
                        "endpoint": "/bluetooth/le/setupDeactivate"
                    },
                    {
                        "endpoint": "/bluetooth/le/setupStatus"
                    },
                    {
                        "endpoint": "/bluetooth/sink/connect"
                    },
                    {
                        "endpoint": "/bluetooth/sink/connectionStatus"
                    },
                    {
                        "endpoint": "/bluetooth/sink/disconnect"
                    },
                    {
                        "endpoint": "/bluetooth/sink/list"
                    },
                    {
                        "endpoint": "/bluetooth/sink/macAddr"
                    },
                    {
                        "endpoint": "/bluetooth/sink/pairable"
                    },
                    {
                        "endpoint": "/bluetooth/sink/remove"
                    },
                    {
                        "endpoint": "/bluetooth/sink/status"
                    }
                ],
                "version": 1
            },
            {
                "apiGroup": "CAPS",
                "endpoints": [
                    {
                        "endpoint": "/addZoneSlave"
                    },
                    {
                        "endpoint": "/audio/defaultVolume"
                    },
                    {
                        "endpoint": "/audio/volume"
                    },
                    {
                        "endpoint": "/audio/volume/decrement"
                    },
                    {
                        "endpoint": "/audio/volume/increment"
                    },
                    {
                        "endpoint": "/audio/volumeMax"
                    },
                    {
                        "endpoint": "/audio/volumeMin"
                    },
                    {
                        "endpoint": "/audio/zone"
                    },
                    {
                        "endpoint": "/content/nowPlaying"
                    },
                    {
                        "endpoint": "/content/nowPlaying/favorite"
                    },
                    {
                        "endpoint": "/content/nowPlaying/rating"
                    },
                    {
                        "endpoint": "/content/nowPlaying/repeat"
                    },
                    {
                        "endpoint": "/content/nowPlaying/shuffle"
                    },
                    {
                        "endpoint": "/content/playbackRequest"
                    },
                    {
                        "endpoint": "/content/selectLastSource"
                    },
                    {
                        "endpoint": "/content/selectLastStreamingSource"
                    },
                    {
                        "endpoint": "/content/transportControl"
                    },
                    {
                        "endpoint": "/getZone"
                    },
                    {
                        "endpoint": "/removeZoneSlave"
                    },
                    {
                        "endpoint": "/setZone"
                    },
                    {
                        "endpoint": "/startDiscoveryAdvertisement"
                    },
                    {
                        "endpoint": "/system/sources"
                    }
                ],
                "version": 1
            },
            {
                "apiGroup": "FrontDoor",
                "endpoints": [
                    {
                        "endpoint": "/internal/capabilities"
                    },
                    {
                        "endpoint": "/network/ping"
                    },
                    {
                        "endpoint": "/system/capabilities"
                    },
                    {
                        "endpoint": "deregister"
                    },
                    {
                        "endpoint": "register"
                    }
                ],
                "version": 1
            },
            {
                "apiGroup": "FrontDoor",
                "endpoints": [
                    {
                        "endpoint": "/deregister"
                    },
                    {
                        "endpoint": "/internal/capabilities"
                    },
                    {
                        "endpoint": "/network/ping"
                    },
                    {
                        "endpoint": "/register"
                    },
                    {
                        "endpoint": "/system/capabilities"
                    }
                ],
                "version": 2
            },
            {
                "apiGroup": "Lightbar",
                "endpoints": [
                    {
                        "endpoint": "/ui/lightbar"
                    }
                ],
                "version": 1
            },
            {
                "apiGroup": "Passport",
                "endpoints": [
                    {
                        "endpoint": "/cloudSync"
                    }
                ],
                "version": 1
            },
            {
                "apiGroup": "ProductActivation",
                "endpoints": [
                    {
                        "endpoint": "/system/activated"
                    },
                    {
                        "endpoint": "/system/authentication"
                    },
                    {
                        "endpoint": "/system/challenge"
                    }
                ],
                "version": 1
            },
            {
                "apiGroup": "ProductController",
                "endpoints": [
                    {
                        "endpoint": "/audio/bass"
                    },
                    {
                        "endpoint": "/audio/treble"
                    },
                    {
                        "endpoint": "/clock"
                    },
                    {
                        "endpoint": "/system/buttonEvent"
                    },
                    {
                        "endpoint": "/system/configuration/status"
                    },
                    {
                        "endpoint": "/system/info"
                    },
                    {
                        "endpoint": "/system/language"
                    },
                    {
                        "endpoint": "/system/power/control"
                    },
                    {
                        "endpoint": "/system/power/timeouts"
                    },
                    {
                        "endpoint": "/system/productSettings"
                    },
                    {
                        "endpoint": "/system/reset"
                    },
                    {
                        "endpoint": "/system/setup"
                    },
                    {
                        "endpoint": "/system/state"
                    },
                    {
                        "endpoint": "/system/update/start"
                    },
                    {
                        "endpoint": "/ui/Display"
                    },
                    {
                        "endpoint": "/ui/alive"
                    },
                    {
                        "endpoint": "/ui/display"
                    }
                ],
                "version": 1
            },
            {
                "apiGroup": "SASS",
                "endpoints": [
                    {
                        "endpoint": "/sass/debug"
                    },
                    {
                        "endpoint": "/sass/error"
                    },
                    {
                        "endpoint": "/sass/frontingRequest"
                    },
                    {
                        "endpoint": "/sass/playRequest"
                    },
                    {
                        "endpoint": "/sass/sassToggle"
                    },
                    {
                        "endpoint": "/sass/stopAll"
                    },
                    {
                        "endpoint": "/sass/streamStatus"
                    }
                ],
                "version": 1
            },
            {
                "apiGroup": "Unknown",
                "endpoints": [
                    {
                        "endpoint": "/demo"
                    },
                    {
                        "endpoint": "/demo/chimes"
                    },
                    {
                        "endpoint": "/demo/keyConfig"
                    },
                    {
                        "endpoint": "/network/status"
                    },
                    {
                        "endpoint": "/network/wifi/ap"
                    },
                    {
                        "endpoint": "/network/wifi/profile"
                    },
                    {
                        "endpoint": "/network/wifi/siteScan"
                    },
                    {
                        "endpoint": "/network/wifi/status"
                    },
                    {
                        "endpoint": "/systemeventservice/register"
                    },
                    {
                        "endpoint": "/voice/listen"
                    },
                    {
                        "endpoint": "/voice/mic"
                    },
                    {
                        "endpoint": "/voice/status"
                    }
                ],
                "version": 1
            },
            {
                "apiGroup": "Update",
                "endpoints": [
                    {
                        "endpoint": "/system/update/status"
                    }
                ],
                "version": 1
            }
        ]}, indent=4)
        jsonMsg['body'] = json.loads(data)
        return jsonMsg

    def _bluetooth_le_setupStatus(self, jsonMsg):
        self.logger.info("_bluetooth_le_setupStatus")
        if jsonMsg['header']['method'] == 'GET':
            data = json.dumps({
                "state": "INACTIVE"}, indent=4)
            jsonMsg['body'] = json.loads(data)
        else:
            jsonMsg['header']['status'] = 500
            jsonMsg['error'] = json.loads(self.__error_only_get())
        return jsonMsg

    def _bluetooth_sink_macAddr(self, jsonMsg):
        self.logger.info("_bluetooth_sink_macAddr")
        if jsonMsg['header']['method'] == 'GET':
            data = json.dumps({
                "mac": "AA:BB:CC:DD:EE:FF"}, indent=4)
            jsonMsg['body'] = json.loads(data)
        else:
            jsonMsg['header']['status'] = 500
            jsonMsg['error'] = json.loads(self.__error_only_get())
        return jsonMsg

    def _cloudSync(self, jsonMsg):
        self.logger.info("_cloudSync")

    def _demo(self, jsonMsg):
        self.logger.info("_demo")
        if jsonMsg['header']['method'] == 'GET':
            data = json.dumps({"demoMode" : "ON"}, indent=4)
            jsonMsg['body'] = json.loads(data)
        else:
            jsonMsg['header']['status'] = 500
            jsonMsg['error'] = json.loads(self.__error_only_get())
        return jsonMsg

    def _demo_keyConfig(self, jsonMsg):
        self.logger.info("_demo_keyConfig")
        if jsonMsg['header']['method'] == 'GET':
            data = json.dumps({"keyTable":[{"origin": 0,
                                       "keyEvent": 1,
                                       "keyList": [4],
                                       "timeOutList": [0],
                                       "action": 1001,
                                       "comment": "Console: MFB release between 0-1750 ms ---> play-pause"}]}, indent=4) 
            jsonMsg['body'] = json.loads(data)
        elif jsonMsg['header']['method'] == 'PUT':
            data = json.dumps({"keyTable":[{"origin": 0,
                                       "keyEvent": 1,
                                       "keyList": [4],
                                       "timeOutList": [0],
                                       "action": 1001,
                                       "comment": "Console: MFB release between 0-1750 ms ---> play-pause"}]}, indent=4)
            jsonMsg['body'] = json.loads(data)
        elif jsonMsg['header']['method'] == 'DELETE':
            data = json.dumps({"keyTable":[{"origin": 0,
                                       "keyEvent": 1,
                                       "keyList": [4],
                                       "timeOutList": [0],
                                       "action": 1001,
                                       "comment": "Console: MFB release between 0-1750 ms ---> play-pause"}]}, indent=4)
            jsonMsg['body'] = json.loads(data)
        else:
            jsonMsg['header']['status'] = 500
            jsonMsg['error'] = json.loads(self.__error_only_get())
        return jsonMsg

    def _network_ping(self, jsonMsg):
            self.logger.info("_network_ping")
            if jsonMsg['header']['method'] == 'GET':
                data = json.dumps({"pong" : 'true'}, indent=4)
                jsonMsg['body'] = json.loads(data)
            else:
                jsonMsg['header']['status'] = 500
                jsonMsg['error'] = json.loads(self.__error_only_get())
            return jsonMsg

    def _network_status(self, jsonMsg):
        self.logger.info("_network_status")
        if jsonMsg['header']['method'] == 'GET':
            data = json.dumps({
                "interfaces": [
                    {
                        "ipInfo": {
                            "ipAddress": "192.168.1.0",
                            "subnetMask": "255.255.255.192"
                        },
                        "macAddress": "ABCDEFGHIJ01",
                        "name": "wlan0",
                        "state": "UP",
                        "type": "WIRELESS"
                    }
                ],
                "isPrimaryUp": 'true',
                "primary": "WIRELESS",
                "primaryIpAddress": "192.168.1.1"
            }, indent=4)
            jsonMsg['body'] = json.loads(data)
        else:
            jsonMsg['header']['status'] = 500
            jsonMsg['error'] = json.loads(self.__error_only_get())
        return jsonMsg

    def _network_wifi_status(self, jsonMsg):
        self.logger.info("_network_wifi_status")
        if jsonMsg['header']['method'] == 'GET':
            data = json.dumps({
                "frequencyKhz": "5180000",
                "signalDbm": "-43",
                "ssid": "B-PRODUCT",
                "state": "WIFI_STATION_CONNECTED"}, indent=4)
            jsonMsg['body'] = json.loads(data)
        else:
            jsonMsg['header']['status'] = 500
            jsonMsg['error'] = json.loads(self.__error_only_get())
        return jsonMsg        

    def _network_wifi_profile(self, jsonMsg):
        self.logger.info("_network_wifi_profile")
        if jsonMsg['header']['method'] == 'POST':
            profile = jsonMsg["body"]
            if not profile:
                jsonMsg['header']['status'] = 400
                jsonMsg['error'] = json.loads(self.__error_missing_payload())
        else:
            data = json.dumps(
                {"profiles": [
                    {
                        "security": "WPA_OR_WPA2",
                        "ssid": "B-PRODUCT"
                    }]}, indent=4)
            jsonMsg['body'] = json.loads(data)
        return jsonMsg

    def _network_wifi_siteScan(self, jsonMsg):
        self.logger.info("_network_wifi_siteScan")
        if jsonMsg['header']['method'] == 'GET':
            jsonMsg['header']['status'] = 400
            jsonMsg['error'] = json.loads(self.__error_missing_payload())
        else:
            data = json.dumps(self.wifiData)
            jsonMsg['body'] = json.loads(data)
        return jsonMsg

    def _remote(self, jsonMsg):
        self.logger.info("_remote")
        if jsonMsg['header']['method'] == 'GET':
            data = jsonMsg.dumps({"pairingState" : "PSTATE_INIT",
                                  "remoteMacAddr" : "no example specified",
                                  "remoteName" : "no example specified",
                                  "remoteVersion" : "no example specified"}, indent=4)
            jsonMsg['body'] = json.loads(data)
        elif jsonMsg['header']['method'] == 'PUT':
            data = jsonMsg.dumps({"pair" : 'true',
                                  "timeout" : 120}, indent=4)
            jsonMsg['body'] = json.loads(data)
        else:
            jsonMsg['header']['status'] = 500
            jsonMsg['error'] = json.loads(self.__error_only_get())
                        
    def set_wifi_data(self, data):
        self.wifiData = data

    def _system_activationData(self, jsonMsg):
        self.logger.info("_system_activationData")
        if jsonMsg['header']['method'] == 'GET':
            data = json.dumps({
                "header": {
	                "device": "",
	                "resource": "/system/activationData",
	                "method": "GET",
	                "msgtype": "RESPONSE",
	                "reqID": 0,
	                "version": 1.000000,
	                "status": 500
                },
                "error": {
	                "GUID": "1",
	                "code": 0,
	                "message": "HandleFrontDoorRequest - Send failed - Request was not in GetRegistryWithPayload",
	                "subcode": 1005 }}, indent=4) 
            jsonMsg['body'] = json.loads(data)
        elif jsonMsg['header']['method'] == 'POST':
            data = json.dumps({
	                        "header": {
		                        "device": "1",
		                        "resource": "/system/activationData",
		                        "method": "POST",
		                        "msgtype": "REQUEST",
		                        "reqID": 43,
		                        "version": 1.000000
	                        },
	                        "body": {
		                        "swVersion": "5.0.8-0+13729d0",
		                        "productType": "eddie",
		                        "productMarketingName": "Bose Home Speaker 500"}}, indent=4) 
            jsonMsg['header']['method'] = 'NOTIFY'
            jsonMsg['header']['resource'] = '/system/activationData'
            del jsonMsg['header']['msgtype']
            jsonMsg["body"] = json.loads(data)
            self.logger.info("The notification to the client is: %s", json.dumps(jsonMsg, indent=4))
        else:
            jsonMsg['header']['status'] = 500
            jsonMsg['error'] = json.loads(self.__error_only_get())
        return jsonMsg
    

    def _system_info(self, jsonMsg):
        self.logger.info("_system_info")
        if jsonMsg['header']['method'] == 'GET':
            data = json.dumps({
              "countryCode" : "US",
              "defaultName" : "Bose Home Speaker 500",
              "guid" : "26e9d45e-cb4e-4deb-8e6b-b68d66cfddbc",
              "name" : "Living Room",
              "productColor" : 0,
              "productId" : 16422,
              "productName" : "Bose Home Speaker 500",
              "productType" : "eddie",
              "regionCode" : "US",
              "serialNumber" : "078338980220110AE",
              "softwareVersion" : "1.5.16-3941+2048b03",
              "variantId" : 1}, indent=4)
            jsonMsg['body'] = json.loads(data)
        else:
            jsonMsg['header']['status'] = 500
            jsonMsg['error'] = json.loads(self.__error_only_get())
        return jsonMsg

    def _system_state(self, jsonMsg):
        self.logger.info("_system_state")
        if jsonMsg['header']['method'] == 'GET':
            data = json.dumps({"state" : "BOOTING"}, indent=4)
            jsonMsg['body'] = json.loads(data)
        else:
            jsonMsg['header']['status'] = 500
            jsonMsg['error'] = json.loads(self.__error_only_get())
        return jsonMsg

    def _system_update_status(self, jsonMsg):
        self.logger.info("_system_update_status")
        if jsonMsg['header']['method'] == 'GET':
            data = json.dumps({"availableVersion": "0.0.0",
                               "deadline": "1970-01-01T00:00:00.00Z",
                               "deferrable": 'true',
                               "percent": 0,
                               "status": "UP_TO_DATE"}, indent=4)
            jsonMsg['body'] = json.loads(data)
        else:
            jsonMsg['header']['status'] = 500
            jsonMsg['error'] = json.loads(self.__error_only_get())
        return jsonMsg

    def _system_update_start(self, jsonMsg):
        self.logger.info("_system_update_start")
        data = json.dumps({
            "availableVersion": "",
            "deadline": "",
            "deferrable": 'false',
            "localUpdate": 'false',
            "percent": "0",
            "status": "CHECKING_FOR_UPDATE"
        }, indent=4)
        jsonMsg['body'] = json.loads(data)
        return jsonMsg

    def _system_setup(self, jsonMsg):
        self.logger.info("_system_setup")
        jsonMsg['body'] = {"networkConfigured": 'true', "isSetupCompleted": 'false'}
        return jsonMsg

    def _system_activated(self, jsonMsg):
        self.logger.info("_system_activated")
        jsonMsg['body'] = {"status": "NOT_ACTIVATED"}
        return jsonMsg

    def _system_challenge(self, jsonMsg):
        self.logger.info("_system_challenge")
        jsonMsg['body'] = {
          "challenge" : "1513630208",
          "guid" : "26e9d45e-cb4e-4deb-8e6b-b68d66cfddbc",
          "signature" : "I1khamtYXUpwLz10bkgxTT9ffmtuQzBMS3kzVFhUVlRnPC04SyFdTGJQKHV6eE9TOj0="
            }
        return jsonMsg

    def _ui_lightbar(self, jsonMsg):
        self.logger.info("_ui_lightbar")
        if jsonMsg['header']['method'] == 'GET':
            data = json.dumps({
              "currentValue" : {
                "repeat" : 'false',
                "transition" : "no example specified",
                "value" : "no example specified"
              },
              "nextValue" : {
                "repeat" : 'false',
                "transition" : "no example specified",
                "value" : "no example specified"
              },
              "properties" : {
                "supportedTransistions" : [ "no example specified" ],
                "supportedValues" : [ "no example specified" ]
              }
            }, indent=4)
            jsonMsg['body'] = json.loads(data)
        else:
            jsonMsg['header']['status'] = 500
            jsonMsg['error'] = json.loads(self.__error_only_get())
        return jsonMsg
    
    def _device_configure(self, jsonMsg):
        self.logger.info("_device_configure")
        if jsonMsg['header']['method'] == 'PUT':
            data = json.dumps({
                "config": {
                    "activationKey": "ACTIVATION_KEY_GAME",
                    "friendlyName": "FRIENDLY_NAME_HDTV_TUNER",
                   "routingInfo": {
                        "availableInputs": [
                           "DEVICE_INPUT_HDMI1",
                           "DEVICE_INPUT_HDMI2",
                           "DEVICE_INPUT_HDMI3",
                           "DEVICE_INPUT_HDMI4"
                        ],
                        "input": "DEVICE_INPUT_UNKNOWN",
                        "parentId": "TV"
                    }
                },
                "id": "SLOT_0",
                "status": [
                    {
                        "configType": "ADDITIONAL_CONFIG_ROUTINGINFO",
                        "isCompleted": 'false',
                        "isRequired": 'false'
                    },
                    {
                        "configType": "ADDITIONAL_CONFIG_FRIENDLYNAME",
                        "isCompleted": 'true',
                        "isRequired": 'false'
                    },
                    {
                        "configType": "ADDITIONAL_CONFIG_ACTIVATIONKEY",
                        "isCompleted": 'true',
                        "isRequired": 'true'
                    }
                ]
            }, indent=4)
            jsonMsg['body'] = json.loads(data)
        return jsonMsg
     
    def _voice_status(self, jsonMsg):
        self.logger.info("_voice_status")
        if jsonMsg['header']['method'] == 'GET':
            data = json.dumps({
                 	"header": {
                 		"device": "",
                 		"resource": "/voice/status",
                 		"method": "GET",
                 		"msgtype": "RESPONSE",
                 		"reqID": 0,
                 		"version": 1.000000,
                 		"status": 200
                 	},
                 	"body": {
                 		"status": "IDLE"
                 	}
                 }, indent=4)
            jsonMsg['body'] = json.loads(data)
        else:
            jsonMsg['header']['status'] = 500
            jsonMsg['error'] = json.loads(self.__error_only_get())
        return jsonMsg

    def __error_only_get(self):
        data = json.dumps({
            "GUID": "1",
            "code": "1",
            "message": "HandleFrontDoorRequest - Send failed - Request was not in either PostRegistry, or PostEmptyResponseRegistry",
            "subcode": "1005"})
        return data

    def __error_missing_payload(self):
        data = json.dumps({
            "GUID": "1",
            "code": "1",
            "message": "HandleFrontDoorRequest - Send failed - Request is missing payload",
            "subcode": "1005"
        }, indent=4)
        return data

if __name__ == '__main__':
    mockFront = MockFrontDoorBase()
    data = json.dumps({
        'header': {
            "device": "",
            "resource": "/system/setup",
            "method": "GET",
            "msgtype": "RESPONSE",
            "reqID": 0,
            "version": 1,
            "status": 200,
            "token": "las9kdfjaslkjdbhgsdkKbldkfbvnl?adkfjnvlk"
        }}, indent=4)
    data = json.loads(data)
    mockFront.parser(data)

