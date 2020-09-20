"""
Notification class for mock frontdoor
"""
import json
from .mockfrontDoor import MockFrontDoor

from ....LoggerUtils.CastleLogger import get_logger
LOGGER = get_logger(__name__)

class FrontDoorNotify(MockFrontDoor):
    """
    Defining callbacks for notifications
    """

    def volumeCallback(self, jsonMsg):
        """
        :param: jsonMsg, that includes header / Type of Request
        broadcasts message to all clients in localhost
        """
        LOGGER.info("_audio_volume")
        _volume = 30
        if jsonMsg['header']["method"] == 'GET':
            data = json.dumps({"value": _volume}, indent=4)
            jsonMsg['body'] = json.loads(data)

        elif jsonMsg['header']["method"] == 'PUT':
            _volume = jsonMsg["body"]["value"]
            data = json.dumps({"defaultOn": "30", \
                              "min": "0", \
                              "muted": "false", \
                              "max": "100", \
                              "value": _volume, \
                              "thresholdVolume": { \
                                  "max": "70", \
                                  "min": "30"}}, indent=4)

            jsonMsg['header']['method'] = 'NOTIFY'
            del jsonMsg['header']['msgtype']
            jsonMsg["body"] = json.loads(data)
            LOGGER.info("The notification to be broadcasted is: %s", json.dumps(jsonMsg, indent=4))
            self.broadcast(jsonMsg)

    def incrementvolumeCallback(self, jsonMsg):
        """
        :param: jsonMsg, that includes header / Type of Request
        broadcasts message to all clients in localhost
        """
        LOGGER.info("_audio_volume_increment")
        if jsonMsg['header']["method"] == 'PUT':
            volume = jsonMsg["body"]["delta"]
            data = json.dumps({"delta": volume}, indent=4)
            jsonMsg['header']['method'] = 'NOTIFY'
            del jsonMsg['header']['msgtype']
            jsonMsg["body"] = json.loads(data)
            LOGGER.info("The notification to be broadcasted is: %s", json.dumps(jsonMsg, indent=4))
            self.broadcast(jsonMsg)
        else:
            self.logger.info("No other request type supported at this moment")

    def nowPlayingCallback(self, jsonMsg):
        """
        :param: jsonMsg, that includes header / Type of Request
        broadcasts message to all clients in localhost
        """
        LOGGER.info("_content_nowPlaying")
        data  = {
            'collectData' : True,
            'container' : {
                'capabilities' : {
                    'favoriteSupported' : True,
                    'ratingsSupported' : True,
                    'repeatSupported' : True,
                    'resumeSupported' : True,
                    'shuffleSupported' : True,
                    'skipNextSupported' : True,
                    'skipPreviousSupported' : True
                    },
                'contentItem' : {
                    'location' : "tracklisturl",
                    'name' : "",
                    'presetable' : False,
                    'source' : "ALEXA",
                    'sourceAccount' : "alexa_occam@bose.com",
                    'containerArt': "https://m.media-amazon.com/images/I/91eh6ApLnzL._UL600_.jpg"
                    }
                },
            'metadata' : {
                'album' : "Hotel California (Remastered)",
                'artist' : "Eagles",
                'trackName' : "Hotel California (Eagles 2013 Remaster)"
                },
            'state' : {
                'canSkipPrevious' : False,
                'repeat' : "OFF",
                'shuffle' : "OFF",
                'status' : "PLAY",
                },
            'track' : {
                'contentItem' : {
                    'containerArt' : "https://m.media-amazon.com/images/I/91eh6ApLnzL._UL600_.jpg",
                    'presetable' : False,
                    'name' : "Hotel California (Eagles 2013 Remaster)",
                    'source' : "ALEXA",
                    'sourceAccount' : "alexa_occam@bose.com"
                    },
                'favorite' : "YES",
                'rating' : "UP",
                'type' : "AD"
                }
            }
  
        jsonMsg['header']['method'] = 'NOTIFY'
        del jsonMsg['header']['msgtype']
        jsonMsg["body"] = json.loads(data)
        LOGGER.info("The notification to be broadcasted is: %s", json.dumps(jsonMsg, indent=4))
        self.broadcast(jsonMsg)

