"""
FrontDoorAPIBase.py
Utility to send WebSocket requests through FrontDoor
"""

# Disable pylint's no-member error
# pylint: disable=no-member

import json


class FrontDoorAPIBase(object):
    """
    Class that defines getters and setters for API's defined
    """
    def send_api(self, api, method="", _data=""):
        """
        Parameters: api   : API to Send
                _data : JSON data to send for POST API
        """
        self.logger.debug("Sending API: %s", api)
        if _data == "":
            return self.send("GET", api)
        else:
            if method == "":
                return self.send("POST", api, _data)
            else:
                return self.send(method, api, _data)

    # Individual Get & Set functions for each implemented API

    # 1. Handler - Product Eddie
    def getLanguage(self):
        """
        Returns the Language
        :return:  language_list [dict]  FrontDoor response json
        """
        self.logger.debug("Getting the language")
        language_list = self.send("GET", '/system/language')
        language_list = json.loads(language_list)
        return language_list["body"]["code"]

    def getState(self):
        """
        Returns product State
        :return:  state [dict]  FrontDoor response json
        """
        state = self.send("GET", '/system/state')
        state = json.loads(state)
        return state["body"]["state"]

    def getconfigurationStatus(self):
        """
        Returns configuration Status
        :return:  configStatus["body"]["status"]["account"]
                  configStatus["body"]["status"]["language"]
                  configStatus["body"]["status"]["network"] FrontDoor response json
        """
        configStatus = self.send("GET", '/system/configuration/status')
        configStatus = json.loads(configStatus)
        return configStatus["body"]["status"]["account"], \
               configStatus["body"]["status"]["language"], \
               configStatus["body"]["status"]["network"]

    def getInfo(self):
        """
        Returns Product Info
        :return:  info [dict]  FrontDoor response json
        """
        self.logger.debug("Getting the Info from the Product")
        info = self.send("GET", '/system/info')
        info = json.loads(info)
        return info

    def getDemoMode(self):
        """
        Returns demo flag state
        :return:  demoMode [dict]  FrontDoor response json
        """
        demoMode = self.send("GET", '/demo')
        demoMode = json.loads(demoMode)
        return demoMode["body"]["demoMode"]

    def setDemo(self, data):
        """
        Sets the demo Mode
        param: data: {"demoMode": " True/ False"}
        :return:  demoMode [dict]  FrontDoor response json
        """
        demoMode = self.send("PUT", '/demo', data)
        demoMode = json.loads(demoMode)
        return demoMode["body"]["demoMode"]

    def setDemoKeyConfig(self, data):
        """
        Sets the demo keyConfig
        param: data:
        :return:  keyConfig [dict]  FrontDoor response json
        """
        keyConfig = self.send("PUT", '/demo/keyConfig', data)
        keyConfig = json.loads(keyConfig)
        return keyConfig

    def getDemoKeyConfig(self):
        """
        Returns demo keyConfig
        :return:  keyConfig [dict]  FrontDoor response json
        """
        keyConfig = self.send("GET", '/demo/keyConfig')
        keyConfig = json.loads(keyConfig)
        return keyConfig

    def deleteDemoKeyConfig(self):
        """
        Deletes demo keyConfig ## right now payload is required
        :return:  keyConfig [dict]  FrontDoor response json
        """
        keyConfig = self.send("DELETE", '/demo/keyConfig', '{}')
        keyConfig = json.loads(keyConfig)
        return keyConfig

    def setDemoChimes(self, data):
        """ Sets demo chimes """
        demoChimes = self.send("PUT", '/demo/chimes', data)
        demoChimes = json.loads(demoChimes)
        return demoChimes

    def getDemoChimes(self):
        """ Returns demo chimes """
        demoChimes = self.send("GET", '/demo/chimes')
        demoChimes = json.loads(demoChimes)
        return demoChimes

    # 2. Handler - CAPS
    def getSources(self):
        """
        Returns the Source List
        :return:  sourceList [dict]  FrontDoor response json
        """
        self.logger.debug("Getting the Sources List")
        sourceList = self.send("GET", '/system/sources')
        sourceList = json.loads(sourceList)
        return sourceList

    def setSources(self, data):
        """
        Sets the Source List
        :return: sourceList [dict] FrontDoor response json
        """
        self.logger.debug("Setting the Sources List")
        sourceList = self.send("PUT", '/system/sources', data)
        sourceList = json.loads(sourceList)
        return sourceList

    def configureDevice(self, data):
        """
        Configures the source device mapping with HDMI Input Port Number.
        :return: device_config [dict] FrontDoor response json
        """
        self.logger.debug("Setting the Sources List")
        device_config = self.send("PUT", '/device/configure', data)
        device_config = json.loads(device_config)
        return device_config

    def getCapsIntializationStatus(self):
        """
        Checks for CAPS Initialization
        :return:  capsStatus [dict]  FrontDoor response json
        """
        self.logger.debug("Getting the CAPS status")
        capsStatus = self.send("GET", '/system/capsInitializationStatus')
        capsStatus = json.loads(capsStatus)
        return capsStatus["body"]["CapsInitialized"]

    def getNowPlaying(self):
        """
        Returns nowPlaying Information
        :return:  nowplaying [dict]  FrontDoor response json
        """
        self.logger.debug("Getting the nowPlaying information")
        nowplaying = self.send("GET", '/content/nowPlaying')
        nowplaying = json.loads(nowplaying)
        return nowplaying

    def sendPlaybackRequest(self, data):
        """
        Sends playbackRequest msg
        param: data:
        :return:  playbackRequest [dict]  FrontDoor response json
        """
        self.logger.debug("Send playback request")
        playbackRequest = self.send("POST", '/content/playbackRequest', data)
        playbackRequest = json.loads(playbackRequest)
        return playbackRequest

    def sendPlaybackRepeat(self, data):
        """
        Sends playback repeat msg
        param: data: {"repeat" : "ONE" "ALL" "OFF"}
        :return:  nowPlaying [dict]  FrontDoor response json
        """
        self.logger.debug("Send playback repeat")
        nowPlaying = self.send("POST", '/content/nowPlaying/repeat', data)
        nowPlaying = json.loads(nowPlaying)
        return nowPlaying

    def sendPlaybackRating(self, data):
        """
        Sends playback rating msg
        param: data: {"rating" : "UP" "DOWN" "UNRATED"}
        :return:  nowPlaying [dict]  FrontDoor response json
        """
        self.logger.debug("Send playback rating")
        nowPlaying = self.send("POST", '/content/nowPlaying/rating', data)
        nowPlaying = json.loads(nowPlaying)
        return nowPlaying

    def getPlaybackRating(self):
        """
        Returns the response to nowPlaying/rating
        :return:  nowPlaying [dict]  FrontDoor response json
        """
        self.logger.debug("Get playback rating")
        nowPlaying = self.send("GET", '/content/nowPlaying/rating')
        nowPlaying = json.loads(nowPlaying)
        return nowPlaying

    def sendPlaybackShuffle(self, data):
        """
        Sends playback shuffle msg
        param: data: {"shuffle" : "ON" "OFF"}
        :return:  nowPlaying [dict]  FrontDoor response json
        """
        self.logger.debug("Send playback shuffle")
        shuffleResponse = self.send("POST", '/content/nowPlaying/shuffle', data)
        shuffleResponse = json.loads(shuffleResponse)
        return shuffleResponse

    def getPlaybackShuffle(self):
        """
        Returns the response to nowPlaying/shuffle
        :return:  nowPlaying [dict]  FrontDoor response json
        """
        self.logger.debug("Get playback shuffle")
        shuffleResponse = self.send("GET", '/content/nowPlaying/shuffle')
        shuffleResponse = json.loads(shuffleResponse)
        return shuffleResponse

    def stopPlaybackRequest(self):
        """
        Sends /stopPlayback; deactivates the source
        :return:  stopPlaybackResponse [dict]  FrontDoor response json
        """
        self.logger.debug("Stop/Deactivate the source")
        data = '{"position" : 0, "state" : "STOP"}'
        stopPlaybackResponse = self.send("PUT", '/content/transportControl', data)
        stopPlaybackResponse = json.loads(stopPlaybackResponse)
        return stopPlaybackResponse

    def sendTransportControl(self, data):
        """
        Sends transportControl operations
        param:data: {"position" : 0, "state" : "skip"}
        :return:  transportControl [dict]  FrontDoor response json
        """
        self.logger.debug("Set transportcontrol")
        transportControl = self.send("PUT", '/content/transportControl', data)
        transportControl = json.loads(transportControl)
        return transportControl

    def getVolume(self):
        """
        Returns the response to /volume
        :return:  volume [dict]  FrontDoor response json
        """
        self.logger.debug("Getting the current volume")
        volume = self.send("GET", '/audio/volume')
        volume = json.loads(volume)
        return volume

    def sendVolume(self, data):
        """
        Sets the Volume level
        param: data: {"volume": 10}
        :return:  volume [dict]  FrontDoor response json
        """
        self.logger.debug("Sending Volume Level")
        volume = self.send("PUT", '/audio/volume', data)
        volume = json.loads(volume)
        return volume["body"]["value"]

    def sendMinVolume(self, data):
        """
        Sets the minimum threshold volume
        :return:  minVolume [dict]  FrontDoor response json
        """
        self.logger.debug("Setting the minimum Volume")
        minVolume = self.send("POST", '/audio/volumeMin', data)
        minVolume = json.loads(minVolume)
        return minVolume

    def sendMaxVolume(self, data):
        """
        Sets the maximum threshold volume
        :return:  maxVolume [dict]  FrontDoor response json
        """
        self.logger.debug("Setting the Maximum Volume")
        maxVolume = self.send("POST", '/audio/volumeMax', data)
        maxVolume = json.loads(maxVolume)
        return maxVolume

    def sendAbsoluteMinVolume(self, data):
        """
        Sets the minimum volume
        User cannot set volume below this
        param: data: {"volume": 10}
        :return:  minVolume [dict]  FrontDoor response json
        """
        self.logger.debug("Setting the minimum Volume")
        minVolume = self.send("POST", '/audio/volume', data)
        minVolume = json.loads(minVolume)
        return minVolume

    def sendAbsoluteMaxVolume(self, data):
        """
        Sets the absolute maximum volume
        User cannot set volume above this
        param: data: {"volume": 10}
        :return:  maxVolume [dict]  FrontDoor response json
        """
        self.logger.debug("Setting the Maximum Volume")
        maxVolume = self.send("POST", '/audio/volume', data)
        maxVolume = json.loads(maxVolume)
        return maxVolume

    def sendDefaultVolume(self, data):
        """
        Sets the Default volume
        param: data
        :return:  defaultVolume [dict]  FrontDoor response json
        """
        self.logger.debug("Setting the default Volume")
        defaultVolume = self.send("POST", '/audio/defaultVolume', data)
        defaultVolume = json.loads(defaultVolume)
        return defaultVolume["body"]["defaultOn"]

    def getDefaultVolume(self):
        """
        Returns the default Volume
        :return:  defaultVolume [dict]  FrontDoor response json
        """
        self.logger.debug("Setting the default Volume")
        defaultVolume = self.send("GET", '/audio/defaultVolume')
        defaultVolume = json.loads(defaultVolume)
        return defaultVolume["body"]["defaultOn"]

    def sendIncrementVolume(self, data):
        """
        Increments the Volume by given level
        param: data: {"delta" : 0}
        :return:  incrementVolume [dict]  FrontDoor response json
        """
        self.logger.debug("Incrementing Volume")
        incrementVolume = self.send("PUT", '/audio/volume/increment', data)
        incrementVolume = json.loads(incrementVolume)
        return incrementVolume

    def sendDecrementVolume(self, data):
        """
        Decrements the Volume by given level
        param: data: {"delta" : 0}
        :return:  decrementVolume [dict]  FrontDoor response json
        """
        self.logger.debug("Decrementing Volume")
        decrementVolume = self.send("PUT", '/audio/volume/decrement', data)
        decrementVolume = json.loads(decrementVolume)
        return decrementVolume

    def addZone(self, data):
        """
        Create New Zone
        param: data:
        :return:  zoneDetails [dict]  FrontDoor response json
        """
        self.logger.debug("Add Zone Request")
        zoneDetails = self.send("POST", '/audio/zone', data)
        zoneDetails = json.loads(zoneDetails)
        return zoneDetails

    def addSlaveInZone(self, data):
        """
        Add new slave in Zone
        param:"data:
        :return:  zoneSlaveDetails [dict]  FrontDoor response json
        """
        self.logger.debug("Add slave in Zone Request")
        zoneSlaveDetails = self.send("PUT", '/audio/zone', data)
        zoneSlaveDetails = json.loads(zoneSlaveDetails)
        return zoneSlaveDetails

    def deleteZone(self, data):
        """
        Delete Zone
        param: data:
        :return:  zoneDetails [dict]  FrontDoor response json
        """
        self.logger.debug("Delete Zone Request")
        zoneDetails = self.send("DELETE", '/audio/zone', data)
        zoneDetails = json.loads(zoneDetails)
        return zoneDetails

    def getZone(self):
        """
        Get Zone Info
        :return:  zoneDetails [dict]  FrontDoor response json
        """
        self.logger.debug("Get Zone Request")
        zoneDetails = self.send("GET", '/audio/zone')
        zoneDetails = json.loads(zoneDetails)
        return zoneDetails

    def get_favoritesValue(self):
        """
        Get favorites
        :return:  fvalue [dict]  FrontDoor response json
        """
        fvalue = self.send("GET", '/content/nowPlaying/favorite')
        fvalue = json.loads(fvalue)
        return fvalue

    def set_favorites(self, data):
        """
        Set Favorites
        param:data:
        :return:  fvalue [dict]  FrontDoor response json
        """
        fvalue = self.send("POST", '/content/nowPlaying/favorite', data)
        fvalue = json.loads(fvalue)
        return fvalue

    # 3. Handler - NetworkService
    def ping(self):
        """
        Sending Ping
        :return:  pong [dict]  FrontDoor response json
        """
        pong = self.send("GET", '/network/ping')
        pong = json.loads(pong)
        return pong["body"]["pong"]

    def getWifiProfile(self):
        """
        Get the Wi-Fi profiles added to the device
        :return:  wifiProfiles [dict]  FrontDoor response json
        """
        wifiProfiles = self.send("GET", '/network/wifi/profile')
        wifiProfiles = json.loads(wifiProfiles)
        return wifiProfiles

    def addWifiProfile(self, data):
        """
        Add Wi-Fi profile to the device
        param:data:
        :return:  addWifiProfileResponse [dict]  FrontDoor response json
        """
        addWifiProfileResponse = self.send("POST", '/network/wifi/profile', data)
        addWifiProfileResponse = json.loads(addWifiProfileResponse)
        return addWifiProfileResponse

    def getNetworkStatus(self):
        """
        Get Network Status
        :return:  networkStatus [dict]  FrontDoor response json
        """
        networkStatus = self.send("GET", '/network/status')
        networkStatus = json.loads(networkStatus)
        return networkStatus

    def sendSiteScan(self, data, wait_for_response=True):
        """
        Get site-scan results
        param:data:
        :return:  siteSurvey [dict]  FrontDoor response json
        """
        siteSurvey = self.send("POST", '/network/wifi/siteScan', data, wait_for_response)
        siteSurvey = json.loads(siteSurvey)
        return siteSurvey

    def getAPModeStatus(self):
        """
        Get AP mode status on the device
        :return:  apStatus [dict]  FrontDoor response json
        """
        apStatus = self.send("GET", '/network/wifi/ap')
        apStatus = json.loads(apStatus)
        return apStatus

    def setAPMode(self, data):
        """
        Set AP Mode on the device
        param:data:
        :return:  apMode [dict]  FrontDoor response json
        """
        apMode = self.send("POST", '/network/wifi/ap', data)
        apMode = json.loads(apMode)
        return apMode

    def getNetworkWiFiStatus(self):
        """
        Get network WiFi Status
        :return:  wifiStatus [dict]  FrontDoor response json
        """
        wifiStatus = self.send("GET", '/network/wifi/status')
        wifiStatus = json.loads(wifiStatus)
        return wifiStatus

    def setOperationMode(self, data):
        """
        Set Network operation Mode on the device
        param:data:
        :return:  OperationalMode [dict]  FrontDoor response json
        """
        opearationMode = self.send("PUT", '/network/operationMode', data)
        opearationMode = json.loads(opearationMode)
        return opearationMode

    def getOperationMode(self):
        """
        Get Network operation Mode on the device
        :return:  OperationalMode [dict]  FrontDoor response jsonSSSSS
        """
        opearationMode = self.send("GET", '/network/operationMode')
        opearationMode = json.loads(opearationMode)
        return opearationMode

    def performDriverScan(self):
        """
        Perform wifi driver level scan on the device
        :return:  Success [empty response], scan data is stored in /tmp/wifi-mgr-ndc.json file in json format
        """
        driverScan = self.send("POST", '/network/wifi/driverScan')
        driverScan = json.loads(driverScan)
        return driverScan

    # 4. Handler - FrontDoor
    def getCapabilities(self):
        """
        Getting the List of API's for this build
        :return:  apis [dict]  FrontDoor response json
        """
        apis = self.send("GET", '/system/capabilities')
        apis = json.loads(apis)
        return apis

    # 5. Handler - LightBarController
    def getActiveAnimation(self):
        """
        Get current active animation
        :return:  lightbar_status [dict]  FrontDoor response json
        """
        lightbar_status = self.send("GET", '/ui/lightbar')
        lightbar_status = json.loads(lightbar_status)
        return lightbar_status["body"]

    def playLightBarAnimation(self, data):
        """"
        Request Lightbar to play animation
        param:data:
        :return:  lightbar_status [dict]  FrontDoor response json
        """
        lightbar_status = self.send("PUT", '/ui/lightbar', data)
        lightbar_status = json.loads(lightbar_status)
        return lightbar_status

    def stopActiveAnimation(self, data):
        """
        Stopping the current active animation
        param:data:
        :return:  lightbar_status [dict]  FrontDoor response json
        """
        lightbar_status = self.send("DELETE", '/ui/lightbar', data)
        lightbar_status = json.loads(lightbar_status)
        return lightbar_status["body"]

    #    Handler - FrontDoor BLE
    def activateBLESetup(self, data):
        """
        Set BLE advertising status
        param:data
        :return:  bleSetupStatus [dict]  FrontDoor response json
        """
        bleSetupStatus = self.send("POST", '/bluetooth/le/setupActivate', data)
        bleSetupStatus = json.loads(bleSetupStatus)
        return bleSetupStatus

    def deactivateBLESetup(self):
        """
        Set BLE advertising status
        :return:  bleSetupStatus [dict]  FrontDoor response json
        """
        bleSetupStatus = self.send("POST", '/bluetooth/le/setupDeactivate', "{}")
        bleSetupStatus = json.loads(bleSetupStatus)
        return bleSetupStatus

    def getBLESetupStatus(self):
        """
        Get BLE advertising status
        :return:  bleStatus [dict]  FrontDoor response json
        """
        bleStatus = self.send("GET", '/bluetooth/le/setupStatus')
        bleStatus = json.loads(bleStatus)
        return bleStatus["body"]["state"]

    def getMacAddr(self):
        """
        Get BT sink mac addr (same mac for BT Source)
        :return:  macAddr [dict]  FrontDoor response json
        """
        macAddr = self.send("GET", "/bluetooth/sink/macAddr")
        macAddr = json.loads(macAddr)
        return macAddr["body"]["mac"]

    # 6. Handler - FrontDoor BT Sink
    def sinkGoPairable(self):
        """
        Set BT Sink into pairable/connectable state
        :return:  pairableResponse [dict]  FrontDoor response json
        """
        pairableResponse = self.send("POST", "/bluetooth/sink/pairable", "{}")
        pairableResponse = json.loads(pairableResponse)
        return pairableResponse

    def sinkGoToConnecting(self):
        """ Set BT Sink into pairable/connectable state """
        connectableResponse = self.send("POST", "/bluetooth/sink/connect", "{\"mac\":\"\"}")
        connectableResponse = json.loads(connectableResponse)
        return connectableResponse

    def sinkRemoveConnectedDevices(self, data):
        """
        BT Sink remove connected device
        param: data { "mac":"ff:ff:ff:ff:ff:ff" }
        :return:  removeConnectedDevice [dict]  FrontDoor response json
        """
        removeConnectedDevice = self.send("POST", "/bluetooth/sink/remove", data)
        removeConnectedDevice = json.loads(removeConnectedDevice)
        return removeConnectedDevice

    def sinkClearAllConnectedDevices(self):
        """
        BT Sink clear connected devices list
        :return:  clearConnecteList [dict]  FrontDoor response json
        """
        clearConnecteList = self.send("POST", "/bluetooth/sink/remove", "{}")
        clearConnecteList = json.loads(clearConnecteList)
        return clearConnecteList

    def sinkGetConnectedDevicesList(self):
        """
        BT Sink get connected BT device list
        :return:  macAddressList [dict]  FrontDoor response json
        """
        getConnectedDeviceList = self.send("GET", "/bluetooth/sink/list")
        getConnectedDeviceList = json.loads(getConnectedDeviceList)
        macAddressList = []
        for device in getConnectedDeviceList["body"]["devices"]:
            macAddressList.append(device["mac"])
        return macAddressList

    def sinkGetAppStatus(self):
        """
        Get BT Sink app status
        :return:  sinkAppStatus [dict]  FrontDoor response json
        """
        sinkAppStatus = self.send("GET", "/bluetooth/sink/status")
        sinkAppStatus = json.loads(sinkAppStatus)
        return sinkAppStatus["body"]

    def sinkConnectToRemoteDevice(self, data):
        """
        BT Sink connect to remote device
        param:data: { "mac":"ff:ff:ff:ff:ff:ff" }
        :return:  sinkConnectRemoteDevice [dict]  FrontDoor response json
        """
        sinkConnectRemoteDevice = self.send("POST", "/bluetooth/sink/connect", data)
        sinkConnectRemoteDevice = json.loads(sinkConnectRemoteDevice)
        return sinkConnectRemoteDevice

    def sinkDisconnectFromRemoteDevice(self, data):
        """
        BT Sink disconnect from remote device
        param:data: { "mac":"ff:ff:ff:ff:ff:ff" }
        :return:  sinkDisconnect [dict]  FrontDoor response json
        """
        sinkDisconnect = self.send("POST", "/bluetooth/sink/disconnect", data)
        sinkDisconnect = json.loads(sinkDisconnect)
        return sinkDisconnect

    def sinkDelayReport(self, data):
        """
        BT Sink send delay report
        param:data: { "delay": int }
        :return:  sinkDelayReport [dict]  FrontDoor response json
        """
        sinkDelay = self.send("POST", "/bluetooth/sink/delayReporting", data)
        sinkDelay = json.loads(sinkDelay)
        return sinkDelay

    # 7. Handler - FrontDoor BT Source
    def sourcePairDevice(self, data):
        """
        BT Source pair to remote device
        param:data: { "mac":"ff:ff:ff:ff:ff:ff" }
        :return:  sourcePairDevice [dict]  FrontDoor response json
        """
        sourcePairDevice = self.send("POST", "/bluetooth/source/pair", data)
        sourcePairDevice = json.loads(sourcePairDevice)
        return sourcePairDevice

    def sourceConnectToRemoteDevice(self, data):
        """
        BT Source connect to remote device
        param:data: { "mac":"ff:ff:ff:ff:ff:ff" }
        :return:  sourceConnect [dict]  FrontDoor response json
        """
        sourceConnect = self.send("POST", "/bluetooth/source/connect", data)
        sourceConnect = json.loads(sourceConnect)
        return sourceConnect

    def sourceDisconnectFromRemoteDevice(self, data):
        """
        BT Source disconnect from remote device
        param:data: { "mac":"ff:ff:ff:ff:ff:ff" }
        :return:  sourceDisconnect [dict]  FrontDoor response json
        """
        sourceDisconnect = self.send("POST", "/bluetooth/source/disconnect", data)
        sourceDisconnect = json.loads(sourceDisconnect)
        return sourceDisconnect

    def sourceVolumeToRemoteDevice(self, data):
        """
        BT Source change volume
        param:data: {"volume":"10"}
        :return:  sourceVolume [dict]  FrontDoor response json
        """
        sourceVolume = self.send("POST", "/bluetooth/source/volume", data)
        sourceVolume = json.loads(sourceVolume)
        return sourceVolume

    def sourceGetConnectedRemoteDevices(self):
        """
        BT Source get connected device
        :return:  connected_device [dict]  FrontDoor response json
        """
        connected_device = self.send("GET", "/bluetooth/source/connect")
        connected_device = json.loads(connected_device)
        return connected_device["body"]

    def sourceRemoveConnectedDevices(self, data):
        """
        BT Source remove connected device
        param:data: { "mac":"ff:ff:ff:ff:ff:ff" }
        :return:  removeConnectedDevice [dict]  FrontDoor response json
        """
        removeConnectedDevice = self.send("POST", "/bluetooth/source/remove", data)
        removeConnectedDevice = json.loads(removeConnectedDevice)
        return removeConnectedDevice

    def sourceClearAllConnectedDevices(self):
        """
        BT Source clear connected devices list
        :return:  clearConnecteList [dict]  FrontDoor response json
        """
        clearConnecteList = self.send("POST", "/bluetooth/source/remove", "{}")
        clearConnecteList = json.loads(clearConnecteList)
        return clearConnecteList

    def sourceGetConnectedDevicesList(self):
        """
        BT Source get connected BT device list
        :return:  macAddressList [dict]  FrontDoor response json
        """
        getConnectedDeviceList = self.send("GET", "/bluetooth/source/list")
        getConnectedDeviceList = json.loads(getConnectedDeviceList)
        macAddressList = []
        for device in getConnectedDeviceList["body"]["devices"]:
            macAddressList.append(device["mac"])
        return macAddressList

    def sourceScanForDevices(self):
        """
        BT Source scan for devices
        :return:  scan [dict]  FrontDoor response json
        """
        scan = self.send("POST", "/bluetooth/source/scan", "{}")
        scan = json.loads(scan)
        return scan
   
    def sourceStopScan(self):
        """
        BT Source Stopscan
        :return:  Stopscan [dict]  FrontDoor response json
        """
        stopScan = self.send("POST", "/bluetooth/source/stopScan", "{}")
        stopScan = json.loads(stopScan)
        return stopScan

    def sourcePlayStatus(self, data):
        """
        BT Source send AVRCP PlayStatus (This is Private API)
        status: "STATUS_PLAYING", "STATUS_PAUSED", "STATUS_STOPPED"
        param:data: {"status": "STATUS_PAUSED", "position":0, "duration":0, allowNowPlaying":"true"},
        :return:  playStatus [dict]  FrontDoor response json
        """
        playStatus = self.send("POST", "/bluetooth/source/playStatus", data)
        playStatus = json.loads(playStatus)
        return playStatus

    def stackSetDeviceMode(self, data):
        """
        BT Stack set the device mode
        Current options: "NONE", "CONNECTABLE", "DISCOVERABLE_PAIRABLE_CONNECTABLE"
        param: data: { "mode":"NONE" }
        :return: stackSetDeviceMode [dict]  FrontDoor response json
        """
        setDeviceMode = self.send("POST", "/bluetooth/deviceMode", data)
        setDeviceMode = json.loads(setDeviceMode)
        return setDeviceMode

    def stackGetDeviceMode(self):
        """
        BT Stack set the device mode
        :return: stackGetDeviceMode [dict]  FrontDoor response json
        """
        getDeviceMode = self.send("GET", "/bluetooth/deviceMode")
        getDeviceMode = json.loads(getDeviceMode)
        return getDeviceMode

    def stackRequestRole(self, data):
        """
        BT Stack get request role againts a particular device
        param: data: { "mac":"ff:ff:ff:ff:ff:ff" }
        :return: stackRequestRole [dict]  FrontDoor response json
        """
        setRequestRole = self.send("POST", "/bluetooth/role", data)
        setRequestRole = json.loads(setRequestRole)
        return setRequestRole

    def stackResponseRole(self):
        """
        BT Stack get response role againts a particular device
        :return: stackResponseRole [dict]  FrontDoor response json
        """
        setResponseRole = self.send("GET", "/bluetooth/role")
        setResponseRole = json.loads(setResponseRole)
        return setResponseRole

    def stackGetMacAddr(self):
        """
        Get BT Stack mac address
        :return:  macAddr [string]
        """
        macAddr = self.send("GET", "/bluetooth/macAddr")
        macAddr = json.loads(macAddr)
        return macAddr["body"]["mac"]

    # 8. Handler - Passport
    def cloudSync(self, data):
        """
        Sends /cloudSync - Syncs 'ALL'
        param:data:
        :return:  sync [dict]  FrontDoor response json
        """
        sync = self.send("PUT", "/cloudSync", data)
        sync = json.loads(sync)
        return sync

    # 9. Handler - ProductController
    def getAdaptiq(self):
        """
        Returns Adaptiq Information
        :return:  adaptiq [dict]  FrontDoor response json
        """
        self.logger.debug("Getting the Adaptiq information")
        adaptiq = self.send("GET", '/adaptiq')
        adaptiq = json.loads(adaptiq)
        return adaptiq

    def sendAdaptiqRequest(self, data):
        """
        Sends Adaptiq msg
        param: data
        :return:  adaptiqRequest [dict]  FrontDoor response json
        """
        self.logger.debug("Send Adaptiq request")
        adaptiqRequest = self.send("PUT", '/adaptiq', data)
        adaptiqRequest = json.loads(adaptiqRequest)
        return adaptiqRequest

    def getPower(self):
        """
        Returns power Information
        :return:  power [dict]  FrontDoor response json
        """
        self.logger.debug("Getting the power information")
        power = self.send("GET", '/system/power/control')
        power = json.loads(power)
        return power

    def setPower(self, data):
        """
        Set the power state
        :param data: {"power": "ON" "OFF" "TOGGLE"}
        :return:
        """
        response_json = self.send('POST', '/system/power/control', data=data)
        response_dict = json.loads(response_json)
        return response_dict

    # 10. Handler - Accessories
    def getAccessories(self):
        """
        Sends a GET to '/accessories'
        :return:  response_dict [dict]  FrontDoor response json
        """
        response_json = self.send('GET', '/accessories')
        response_dict = json.loads(response_json)
        return response_dict

    def setPairingTrue(self):
        """
        Initiate pairing through FrontdoorAPI "/accessories", and get Riviera's response
        :return:  pairing [bool] pairing mode after payload is sent
        """
        enter_pairing_dict = {"pairing": True}
        payload_json = json.dumps(enter_pairing_dict)
        response_json = self.send('PUT', '/accessories', data=payload_json)
        response_dict = json.loads(response_json)
        pairing = response_dict["body"]["pairing"]
        return pairing

    def setPairingFalse(self):
        """
        Stop pairing through FrontdoorAPI "/accessories", and get Riviera's response
        :return:  pairing [bool] pairing mode after payload is sent
        """
        stop_pairing_dict = {"pairing": False}
        payload_json = json.dumps(stop_pairing_dict)
        response_json = self.send('PUT', '/accessories', data=payload_json)
        response_dict = json.loads(response_json)
        pairing = response_dict["body"]["pairing"]
        return pairing

    def disbandAccessories(self):
        """
        Send "disbandAccessories" to FrontdoorAPI "/accessories", and get Riviera's response
        :return:  response_dict [dict]  FrontDoor response json
        """
        disbandAccessories = {"disbandAccessories": True}
        payload_json = json.dumps(disbandAccessories)
        response_json = self.send('PUT', '/accessories', data=payload_json)
        response_dict = json.loads(response_json)
        return response_dict

    # 11. Software Update Service
    def getSoftwareUpdateStatus(self):
        """
        Sends a GET to '/system/update/status'
        :return: repsonse_dict [dict] FrontDoor response json
        """
        response_json = self.send('GET', '/system/update/status')
        response_dict = json.loads(response_json)
        return response_dict

    def sendSystemUpdateStartRequest(self, delay=0):
        """
        Sends a PUT to '/system/update/start (ProductController)'
'
        :return: repsonse_dict [dict] FrontDoor response json
        """
        delay_info = {"delay": delay}
        payload_json = json.dumps(delay_info)
        response_json = self.send('PUT', '/system/update/start', data=payload_json)
        response_dict = json.loads(response_json)
        return response_dict

    # 12. System Settings
    def getBassLevel(self):
        """
        Returns the Bass Level
        :return:  basslevel_dict [dict]  FrontDoor response json
        """
        self.logger.debug("Getting the current Bass Level")
        basslevel_dict = self.send("GET", '/audio/bass')
        basslevel_dict = json.loads(basslevel_dict)
        return basslevel_dict

    def setBassLevel(self, data):
        """
        Sets the Bass level
        Param: data:{"value" : 0}
        :return:  basslevel_dict [dict]  FrontDoor response json
        """
        self.logger.debug("Sending Bass Level")
        basslevel_dict = self.send("PUT", '/audio/bass', data)
        basslevel_dict = json.loads(basslevel_dict)
        return basslevel_dict

    def getTreble(self):
        """
        Returns the Treble Level
        :return:  treble_dict [dict]  FrontDoor response json
        """
        self.logger.debug("Getting the current Treble")
        treble_dict = self.send("GET", '/audio/treble')
        treble_dict = json.loads(treble_dict)
        return treble_dict

    def setTreble(self, data):
        """
        Sets the Treble Level
        Param: data: {"value" : 0}
        :return:  treble_dict [dict]  FrontDoor response json
        """
        self.logger.debug("Sending Treble")
        treble_dict = self.send("PUT", '/audio/treble', data)
        treble_dict = json.loads(treble_dict)
        return treble_dict

    def getCenter(self):
        """
        Returns the Center Level
        :return:  center_dict [dict]  FrontDoor response json
        """
        self.logger.debug("Getting the current Center")
        center_dict = self.send("GET", '/audio/center')
        center_dict = json.loads(center_dict)
        return center_dict

    def setCenter(self, data):
        """
        Sets the Center Level
        Param: data: {"value" : 0}
        :return:  center_dict [dict]  FrontDoor response json
        """
        self.logger.debug("Sending Center")
        center_dict = self.send("PUT", '/audio/center', data)
        center_dict = json.loads(center_dict)
        return center_dict

    def getSurround(self):
        """
        Returns the Surround Level
        :return:  surrounds_dict [dict]  FrontDoor response json
        """
        self.logger.debug("Getting the current Surrounds")
        surrounds_dict = self.send("GET", '/audio/surround')
        surrounds_dict = json.loads(surrounds_dict)
        return surrounds_dict

    def setSurround(self, data):
        """
        Sets the Surround Level
        Param: data:{"value" : 0}
        :return:  surrounds_dict [dict]  FrontDoor response json
        """
        self.logger.debug("Sending Surrounds")
        surrounds_dict = self.send("PUT", '/audio/surround', data)
        surrounds_dict = json.loads(surrounds_dict)
        return surrounds_dict

    def getAudioMode(self):
        """
        Returns the Audio Mode
        :return:  audiomode_dict [dict]  FrontDoor response json
        """
        self.logger.debug("Getting the current AudioMode")
        audiomode_dict = self.send("GET", '/audio/mode')
        audiomode_dict = json.loads(audiomode_dict)
        return audiomode_dict

    def setAudioMode(self, data):
        """
        Sets the Audio Mode
        Param: data:{"value" :"night"}
        :return:  audiomode_dict [dict]  FrontDoor response json
        """
        self.logger.debug("Setting AudioMode")
        audiomode_dict = self.send("PUT", '/audio/mode', data)
        audiomode_dict = json.loads(audiomode_dict)
        return audiomode_dict

    def getMountOrientation(self):
        """
        Returns the mount orientation
        :return: mountorientation_dict [dict] FrontDoor response json
        """
        self.logger.debug("Getting the current mount orientation")
        mountorientation_dict = self.send("GET", "/audio/mountOrientation")
        mountorientation_dict = json.loads(mountorientation_dict)
        return mountorientation_dict

    def setMountOrientation(self, data):
        """
        Returns the mount orientation
        :return: mountorientation_dict [dict] FrontDoor response json
        """
        self.logger.debug("Setting the current mount orientation. {}".format(data))
        mountorientation_dict = self.send("PUT", "/audio/mountOrientation", data)
        mountorientation_dict = json.loads(mountorientation_dict)
        return mountorientation_dict

    def getAVsync(self):
        """
        Returns the A/V sync
        :return:  avsync_dict [dict]  FrontDoor response json
        """
        self.logger.debug("Getting the current AVsync")
        avsync_dict = self.send("GET", '/audio/avSync')
        avsync_dict = json.loads(avsync_dict)
        return avsync_dict

    def setAVsync(self, data):
        """
        Sets the A/V sync
        Param: data: {"value" :0}
        :return:  avsync_dict [dict]  FrontDoor response json
        """
        self.logger.debug("Sending AVsync")
        avsync_dict = self.send("PUT", '/audio/avSync', data)
        avsync_dict = json.loads(avsync_dict)
        return avsync_dict

    def getContentType(self):
        """
        Returns the Content Type
        :return:  contentType_dict [dict]  FrontDoor response json
        """
        self.logger.debug("Getting the current Content Type")
        contentType_dict = self.send("GET", '/audio/contentType')
        contentType_dict = json.loads(contentType_dict)
        return contentType_dict

    def setContentType(self, data):
        """
        Sets the Content Type
        Param: data: {"value" :0}
        :return:  contentType_dict [dict]  FrontDoor response json
        """
        self.logger.debug("Sending Content Type")
        contentType_dict = self.send("PUT", '/audio/contentType', data)
        contentType_dict = json.loads(contentType_dict)
        return contentType_dict

    def getDualMonoSelect(self):
        """
        Returns the Dual Mono Select
        :return:  dualMonoSelect_dict [dict]  FrontDoor response json
        """
        self.logger.debug("Getting the current Dual Mono Select")
        dualMonoSelect_dict = self.send("GET", '/audio/dualMonoSelect')
        dualMonoSelect_dict = json.loads(dualMonoSelect_dict)
        return dualMonoSelect_dict

    def setDualMonoSelect(self, data):
        """
        Sets the Dual Mono Select
        Param: data: {"value" :0}
        :return:  dualMonoSelect_dict [dict]  FrontDoor response json
        """
        self.logger.debug("Sending Dual Mono Select")
        dualMonoSelect_dict = self.send("PUT", '/audio/dualMonoSelect', data)
        dualMonoSelect_dict = json.loads(dualMonoSelect_dict)
        return dualMonoSelect_dict

    def getEqSelect(self):
        """
        Returns the Eq Select
        :return:  eqSelect_dict [dict]  FrontDoor response json
        """
        self.logger.debug("Getting the current Eq Select")
        eqSelect_dict = self.send("GET", '/audio/eqSelect')
        eqSelect_dict = json.loads(eqSelect_dict)
        return eqSelect_dict

    def setEqSelect(self, data):
        """
        Sets the Eq Select
        Param: data: {"value" :0}
        :return:  eqSelect_dict [dict]  FrontDoor response json
        """
        self.logger.debug("Sending Eq Select")
        eqSelect_dict = self.send("PUT", '/audio/eqSelect', data)
        eqSelect_dict = json.loads(eqSelect_dict)
        return eqSelect_dict

    def getGainOffset(self):
        """
        Returns the Gain Offset
        :return:  gainOffset_dict [dict]  FrontDoor response json
        """
        self.logger.debug("Getting the current Gain Offset")
        gainOffset_dict = self.send("GET", '/audio/gainOffset')
        gainOffset_dict = json.loads(gainOffset_dict)
        return gainOffset_dict

    def setGainOffset(self, data):
        """
        Sets the Gain Offset
        Param: data: {"value" :0}
        :return:  gainOffset_dict [dict]  FrontDoor response json
        """
        self.logger.debug("Sending Gain Offset")
        gainOffset_dict = self.send("PUT", '/audio/gainOffset', data)
        gainOffset_dict = json.loads(gainOffset_dict)
        return gainOffset_dict

    def getSubwooferGain(self):
        """
        Returns the Subwoofer Gain
        :return:  subwooferGain_dict [dict]  FrontDoor response json
        """
        self.logger.debug("Getting the current Subwoofer Gain")
        subwooferGain_dict = self.send("GET", '/audio/subwooferGain')
        subwooferGain_dict = json.loads(subwooferGain_dict)
        return subwooferGain_dict

    def setSubwooferGain(self, data):
        """
        Sets the Subwoofer Gain
        Param: data: {"value" :0}
        :return:  subwooferGain_dict [dict]  FrontDoor response json
        """
        self.logger.debug("Sending Subwoofer Gain")
        subwooferGain_dict = self.send("PUT", '/audio/subwooferGain', data)
        subwooferGain_dict = json.loads(subwooferGain_dict)
        return subwooferGain_dict

    def getSubwooferPolarity(self):
        """
        Returns the Subwoofer Polarity
        :return:  subwooferPolarity_dict [dict]  FrontDoor response json
        """
        self.logger.debug("Getting the current Subwoofer Polarity")
        subwooferPolarity_dict = self.send("GET", '/audio/subwooferPolarity')
        subwooferPolarity_dict = json.loads(subwooferPolarity_dict)
        return subwooferPolarity_dict

    def setSubwooferPolarity(self, data):
        """
        Sets the Subwoofer Polarity
        Param: data: {"value" :0}
        :return:  subwooferPolarity_dict [dict]  FrontDoor response json
        """
        self.logger.debug("Sending Subwoofer Polarity")
        subwooferPolarity_dict = self.send("PUT", '/audio/subwooferPolarity', data)
        subwooferPolarity_dict = json.loads(subwooferPolarity_dict)
        return subwooferPolarity_dict

    def getSurroundDelay(self):
        """
        Returns the Surround Delay
        :return:  surroundDelay_dict [dict]  FrontDoor response json
        """
        self.logger.debug("Getting the current Surround Delay")
        surroundDelay_dict = self.send("GET", '/audio/surroundDelay')
        surroundDelay_dict = json.loads(surroundDelay_dict)
        return surroundDelay_dict

    def setSurroundDelay(self, data):
        """
        Sets the Surround Delay
        Param: data: {"value" :0}
        :return:  surroundDelay_dict [dict]  FrontDoor response json
        """
        self.logger.debug("Sending Surround Delay")
        surroundDelay_dict = self.send("PUT", '/audio/surroundDelay', data)
        surroundDelay_dict = json.loads(surroundDelay_dict)
        return surroundDelay_dict

    def getAudioFormat(self):
        """
        Returns the Audio Format
        :return: audio_format_dict [dict] FrontDoor response json
        """
        self.logger.debug("Getting the current Audio Format")
        audioFormat_dict = self.send("GET", '/audio/format')
        audioFormat_dict = json.loads(audioFormat_dict)
        return audioFormat_dict

    def getCec(self):
        """
        Returns the CEC
        :return:  cec_dict [dict]  FrontDoor response json
        """
        self.logger.debug("Getting the CEC")
        cec_dict = self.send("GET", '/cec')
        cec_dict = json.loads(cec_dict)
        return cec_dict

    def setCec(self, data):
        """
        Sets the CEC
        Param: data: {'mode': "Off"}
        :return:  cec_dict [dict]  FrontDoor response json
        """
        self.logger.debug("Sending CEC")
        cec_dict = self.send("PUT", '/cec', data)
        cec_dict = json.loads(cec_dict)
        return cec_dict

    def getAutoWake(self):
        """
        Returns the Auto-Wake status
        :return:  autowake_status [dict]  FrontDoor response json
        """
        self.logger.debug("Getting the Auto-Wake status")
        autowake_status = self.send("GET", '/system/power/mode/opticalAutoWake')
        autowake_status = json.loads(autowake_status)
        return autowake_status

    def setAutoWake(self, data):
        """
        Sets the Auto-Wake status
        Param: data: {"enabled":"false"}
        :return:  autowake_status [dict]  FrontDoor response json
        """
        self.logger.debug("Setting Auto-Wake status")
        autowake_status = self.send("PUT", '/system/power/mode/opticalAutoWake', data)
        autowake_status = json.loads(autowake_status)
        return autowake_status

    def factoryDefault(self):
        """
        Send FrontdoorAPI "/system/factorydefault" to factory defaults system, and get Riviera's response
        :return:  response_dict [dict]  FrontDoor response json
        """
        self.logger.debug("Factory defaulting system")
        data = {"restoreDefaults": True}
        payload_json = json.dumps(data)
        response_json = self.send('PUT', '/system/factorydefault', payload_json)
        response_dict = json.loads(response_json)
        return response_dict

    # 13. Handler - Kepler Remote

    def getRemoteStatus(self):
        """
        Gets the remote status of the console
        :return:response_dict =  {
        "macAddr": "0000000000000000",
        "name": "Bose GC Remote",
        "scanning": false,
        "version": "Version Unknown"
        """
        response_json = self.send('GET', '/remote')  # pylint: disable=no-member
        response_dict = json.loads(response_json)
        return response_dict

    def setRemotePairing(self, data):
        """
        Sets the console to discoverable or not discoverable for Kepler BLE remotes.
        :param data: data = {"pairing": true}
        :return: response_dict =  {
        "macAddr": "0000000000000000",
        "name": "Bose GC Remote",
        "scanning": true,
        "version": "Version Unknown"}
        """
        response_json = self.send('PUT', '/remote', data)  # pylint: disable=no-member
        response_dict = json.loads(response_json)
        return response_dict

    def getRemoteBrightness(self):
        """
        Returns a dictionary of the brightness and intensity properties of the remote
        :return: response_dict: {"brightness" : value, "intensity": value,
        "properties": {"availableBrightness": ["Day"], "availableIntensity": ["High"]}}
        """
        response_json = self.send('GET', '/remote/brightness')  # pylint: disable=no-member
        response_dict = json.loads(response_json)
        return response_dict

    def setRemoteBrightness(self, data):
        """
        Sets the remote brightness
        :param data: = {"brightness" : <brightness>,"intensity" : <intensity>}
        :param <brightness>: Enum: [High, Medium, Low]
        :param <intensity>: Enum: [Day, Night]

        :return: response_dict: {"brightness" : value, "intensity": value,
        "properties": {"availableBrightness": ["Day"], "availableIntensity": ["High"]}}
        """
        response_json = self.send('PUT', '/remote/brightness', data)  # pylint: disable=no-member
        response_dict = json.loads(response_json)
        return response_dict

    def getRemoteIntegration(self):
        """
        Returns the current state of the OSM
        :return:
        """
        response_json = self.send('GET', '/remote/integration')
        response_dict = json.loads(response_json)

        return response_dict

    def setRemoteIntegration(self, data):
        """
        Sends a PUT to /remote/integration to drive QuickSet
        :param
        data: {"action" : "ACTION_START",
        "deviceType": "DEVICE_TYPE_TV",
        "deviceBrand": "Sony"}
        or
        data: {"action" : "ACTION_USER_RESPONSE",
        "response" : "USER_RESPONSE_WORKED"}
        or
        data: {"action": "ACTION_SEND_KEY"}
        or
        data:{"action": "ACTION_CANCEL"}
        or
        data:{"action": "ACTION_COMPLETE"}
        Wiki: https://wiki.bose.com/display/A4V/QS+Front+Door+API+Definition
        :return:
        """
        response_json = self.send('PUT', '/remote/integration', data)
        response_dict = json.loads(response_json)

        return response_dict

    def getRemoteIntegrationBrandList(self, data):
        """
        Returns a list of brands based on device type and filter
        :param data:
        {"deviceType:" device,
        "filter": prefix}
        :return:
        """
        response_json = self.send('POST', '/remote/integration/brandList', data)
        response_dict = json.loads(response_json)

        return response_dict

    def setRemoteIntegrationDirectEntry(self, data):
        """
        Manually enters the device, brand, and model number to receive a ciCode
        :param data:
        {"deviceType": "DEVICE_TYPE_TV",
                       "brand": "Sony",
                       "model": "KDL-32W560A"}
        :return:
        """
        response_json = self.send('PUT', '/remote/integration/directEntry', data)
        response_dict = json.loads(response_json)

        return response_dict

    def getSystemPowerControl(self):
        """ Get System Power state """
        self.logger.info("Getting system power state")
        response_json = self.send("GET", "/system/power/control")
        response_dict = json.loads(response_json)
        return response_dict

    def setSystemPowerControl(self, data):
        """ Get System Power state """
        self.logger.info("Getting system power state")
        response_json = self.send("POST", "/system/power/control", data)
        response_dict = json.loads(response_json)
        return response_dict

    def getProductSettings(self):
        """ Get Product Settings """
        self.logger.info("Getting Product Settings")
        response_json = self.send("GET", "/system/productSettings")
        response_dict = json.loads(response_json)
        return response_dict

    def getSystemReset(self):
        """ Get System Reset API """
        self.logger.info("Getting System Reset information")
        response_json = self.send("GET", "/system/reset")
        response_dict = json.loads(response_json)
        return response_dict

    def setSystemReset(self, data):
        """ Set System Reset API """
        self.logger.info("Setting System Reset information")
        response_json = self.send("PUT", "/system/reset", data)
        response_dict = json.loads(response_json)
        return response_dict

    def getSystemState(self):
        """ Get System State """
        self.logger.info("Getting System State")
        response_json = self.send("GET", "/system/state")
        response_dict = json.loads(response_json)
        return response_dict

    def getSystemSetup(self):
        """ Get System Setup """
        self.logger.info("Getting System Setup information")
        response_json = self.send("GET", "/system/setup")
        response_dict = json.loads(response_json)
        return response_dict

    def setSystemSetup(self, data):
        """ Set System Setup """
        self.logger.info("Setting System Setup information")
        response_json = self.send("PUT", "/system/setup", data)
        response_dict = json.loads(response_json)
        return response_dict

    def getSystemPowerTimeouts(self):
        """ Get System Power Timeouts """
        self.logger.info("Getting System Power Timeouts ")
        response_json = self.send("GET", "/system/power/timeouts")
        response_dict = json.loads(response_json)
        return response_dict

    def setSystemPowerTimeouts(self, data):
        """ Set System Power Timeouts """
        self.logger.info("Setting System Power Timeouts ")
        response_json = self.send("PUT", "/system/power/timeouts", data)
        response_dict = json.loads(response_json)
        return response_dict

    def getInjectKey(self):
        """ Get Inject Key """
        self.logger.info("Getting Inject Key ")
        response_json = self.send("GET", "/injectKey")
        response_dict = json.loads(response_json)
        return response_dict

    def setInjectKey(self, data):
        """ Set Inject Key """
        self.logger.info("Setting Inject Key ")
        response_json = self.send("PUT", "/injectKey", data)
        response_dict = json.loads(response_json)
        return response_dict

    def setClock(self, data):
        """
        Set clock display On/Off LCD screen
        :return:  clockStatus [dict]  FrontDoor response json
        """
        clockDisplayStatus = self.send("PUT", '/clock', data)
        clockStatus = json.loads(clockDisplayStatus)
        return clockStatus

    def getClock(self):
        """
        Get clock display info
        :return:  clockStatus [dict]  FrontDoor response json
        """
        response_json = self.send("GET", "/clock")
        clockStatus = json.loads(response_json)
        return clockStatus

    def setVoiceSetupStart(self, data):
        """
        Set Voice Setup Start API
        :param data:
        {
        "vpaid" : "GVA"
        }
        :return: frondoor Response JSON
        """
        self.logger.info("Setting Voice Setup Start information")
        response_json = self.send("POST", "/voice/setup/start", data)
        response_dict = json.loads(response_json)
        return response_dict

    def subscribeNotification(self, data):
        """
        To Subscribe Frontdoor Notifications
        :param data: data = json.dumps({"notifications": [{"resource": "*", "version": 2.0}]})
        :return response_data : Json dict
        """
        self.logger.info("Getting Frontdoor notification")
        response_data = self.send("PUT", '/subscription', data)
        return response_data

    def getSystemPowerMacro(self):
        """
        Method to Get System Power Macro using /system/power/macro Frontdoor API.
        :return response_dict: Json dict
        """
        self.logger.info("Getting System Power Macro")
        response_json = self.send("GET", "/system/power/macro")
        response_dict = json.loads(response_json)
        return response_dict

    def getVFEVersion(self):
        """
        Returns the short and long version strings 
        :return response_dict: Json dict
        """
        self.logger.debug("Getting the VFE Version")
        response_json = self.send("GET", '/vfe/version')
        response_dict = json.loads(response_json)
        return response_dict

    def getSystemChallenge(self):
        """
        Returns system challenge response 
        :return response string
        """
        challenge_response = self.send("GET", "/system/challenge")
        self.logger.debug("System challenge response: %s ", challenge_response)
        challenge_response = json.loads(challenge_response)
        guid = challenge_response["body"]["guid"]
        challenge = challenge_response["body"]["challenge"]
        signature = challenge_response["body"]["signature"]
        self.logger.info("The guid is: %s", guid)
        self.logger.info("The challenge response is: %s", challenge)
        self.logger.info("The signature  is: %s", signature)
        response = '.'.join([str(guid), str(challenge), str(signature)])
        return response

    def getDeviceControllerTv(self):
        """
        Method to Get Device Controller TV using /device/assumed/TVs Frontdoor API.
        :return response_dict: Json dict
        """
        self.logger.info("Getting Device Controller TV")
        response_json = self.send("GET", "/device/assumed/TVs")
        response_dict = json.loads(response_json)
        return response_dict

    def sendDeviceControllerSetup(self, data):
        """
        Set Device Controller Setup
        :param data:
        {
            "controlType": "DEVICE_CONTROL_TYPE_IR",
            "deviceType": "DEVICE_TYPE_TV",
            "category": "DEVICE_TYPE_LIST_START",
            "irConfig": {
            "codeset": "T2051",
             "manufacturer": "Samsung"},
            "cecConfig": {
            "vendorId": 0,
            "logical": 0,
            "physical": 0,
            "displayName": "TV",
            "power": "CEC_DEVICE_POWER_UNKNOWN"}
        }
        :return: Response JSON
        """
        self.logger.info("Setting Device Controller Setup information")
        response_json = self.send("POST", "/device/setup", data)
        response_dict = json.loads(response_json)
        return response_dict

    def setMaxVolumeLimit(self, data):
        """
        Sets the max volume limit
        User cannot set volume above this
        API used '/audio/volume'
        Response from payload:
        {"header":{"device":"","resource":"/audio/volume","method":"PUT",
        "msgtype":"RESPONSE","reqID":1,"version":1.000000,"status":200},
        "body":{"defaultOn" : 30,"max" : 70,"min" : 30,"muted" : false,
        "properties" : {"maxLimit" : 40,"maxLimitOverride" : true,
        "minLimit" : 0,"startupVolume" : 20,"startupVolumeOverride" : true}
        ,"value" : 0}}
        param data: = {"maxLimit" : 50, "maxLimitOverride" : true}
        :return: maxLimit
        """
        status = False
        max_vol_limit = 0
        try:
            self.logger.debug("Setting the Max volume limit")
            max_limit = self.send("PUT", '/audio/volume', data)
            max_limit = json.loads(max_limit)
            max_vol_limit = int(max_limit["body"]["properties"]["maxLimit"])
            status = True
        except Exception as err_msg:
            self.logger.error("Couldn't parse max volume limit response: %s.", err_msg)
        return status, max_vol_limit

    def setMinVolumeLimit(self, data):
        """
        Sets the min volume limit
        User cannot set volume below this
        API used '/audio/volume'
        Response from payload:
        {"header":{"device":"","resource":"/audio/volume","method":"PUT",
        "msgtype":"RESPONSE","reqID":1,"version":1.000000,"status":200},
        "body":{"defaultOn" : 30,"max" : 70,"min" : 30,"muted" : false,
        "properties" : {"maxLimit" : 40,"maxLimitOverride" : true,
        "minLimit" : 0,"startupVolume" : 20,"startupVolumeOverride" : true}
        ,"value" : 0}}
        param data: = {"minLimit" : 35, "minLimitOverride" : true}
        :return: minLimit
        """
        status = False
        min_vol_limit = 0
        try:
            self.logger.debug("Setting the Min volume limit")
            min_limit = self.send("PUT", '/audio/volume', data)
            min_limit = json.loads(min_limit)
            min_vol_limit = int(min_limit["body"]["properties"]["minLimit"])
            status = True
        except Exception as err_msg:
            self.logger.error("Couldn't parse min volume limit response: %s.", err_msg)
        return status, min_vol_limit

    def setStartupVolume(self, data):
        """
        User sets the startup volume limit
        API used '/audio/volume'
        Response from payload:
        {"header":{"device":"","resource":"/audio/volume","method":"PUT",
        "msgtype":"RESPONSE","reqID":1,"version":1.000000,"status":200},
        "body":{"defaultOn" : 30,"max" : 70,"min" : 30,"muted" : false,
        "properties" : {"maxLimit" : 40,"maxLimitOverride" : true,
        "minLimit" : 0,"startupVolume" : 20,"startupVolumeOverride" : true}
        ,"value" : 0}}
        param data: = {"startupVolume" : 10, "startupVolumeOverride" : true}
        :return: startup_volume
        """
        status = False
        startup_vol_limit = 0
        try:
            self.logger.debug("Setting the Startup volume")
            startup_volume = self.send("PUT", '/audio/volume', data)
            startup_volume = json.loads(startup_volume)
            startup_vol_limit = int(startup_volume["body"]["properties"]["startupVolume"])
            status = True
        except Exception as err_msg:
            self.logger.error("Couldn't parse startup volume response: %s.", err_msg)
        return status, startup_vol_limit

    def getMaxVolumeLimit(self):
        """
        Returns maxLimit
        API used '/audio/volume'
        Response from payload:
        {"header":{"device":"","resource":"/audio/volume","method":"PUT",
        "msgtype":"RESPONSE","reqID":1,"version":1.000000,"status":200},
        "body":{"defaultOn" : 30,"max" : 70,"min" : 30,"muted" : false,
        "properties" : {"maxLimit" : 40,"maxLimitOverride" : true,
        "minLimit" : 0,"startupVolume" : 20,"startupVolumeOverride" : true}
        ,"value" : 0}}
        :return:  maxLimit
        """
        status = False
        max_vol_limit = 0
        try:
            self.logger.debug("Getting the max volume limit")
            max_limit = self.send("GET", '/audio/volume')
            max_limit = json.loads(max_limit)
            max_vol_limit = int(max_limit["body"]["properties"]["maxLimit"])
            status = True
        except Exception as err_msg:
            self.logger.error("Couldn't parse max volume limit response: %s.", err_msg)
        return status, max_vol_limit

    def getStartupVolume(self):
        """
        Returns the startupVolume
        API used '/audio/volume'
        Response from payload:
        {"header":{"device":"","resource":"/audio/volume","method":"PUT",
        "msgtype":"RESPONSE","reqID":1,"version":1.000000,"status":200},
        "body":{"defaultOn" : 30,"max" : 70,"min" : 30,"muted" : false,
        "properties" : {"maxLimit" : 40,"maxLimitOverride" : true,
        "minLimit" : 0,"startupVolume" : 20,"startupVolumeOverride" : true}
        ,"value" : 0}}
        :return:  startupVolume
        """
        status = False
        startup_vol_limit = 0
        try:
            self.logger.debug("Getting the Startup volume")
            startup_volume = self.send("GET", '/audio/volume')
            startup_volume = json.loads(startup_volume)
            startup_vol_limit = int(startup_volume["body"]["properties"]["startupVolume"])
            status = True
        except Exception as err_msg:
            self.logger.error("Couldn't parse startup volume response: %s.", err_msg)
        return status, startup_vol_limit

    def getMinVolumeLimit(self):
        """
        Returns min volume Limit
        API used '/audio/volume'
        Response from payload:
        {"header":{"device":"","resource":"/audio/volume","method":"PUT",
        "msgtype":"RESPONSE","reqID":1,"version":1.000000,"status":200},
        "body":{"defaultOn" : 30,"max" : 70,"min" : 30,"muted" : false,
        "properties" : {"maxLimit" : 40,"maxLimitOverride" : true,
        "minLimit" : 0,"startupVolume" : 20,"startupVolumeOverride" : true}
        ,"value" : 0}}
        :return:  minLimit
        """
        status = False
        min_vol_limit = 0
        try:
            self.logger.debug("Getting the min volume limit")
            min_limit = self.send("GET", '/audio/volume')
            min_limit = json.loads(min_limit)
            min_vol_limit = int(min_limit["body"]["properties"]["minLimit"])
            status = True
        except Exception as err_msg:
            self.logger.error("Couldn't parse min volume limit response: %s.", err_msg)
        return status, min_vol_limit
