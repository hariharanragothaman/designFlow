"""
This is a helper file that uses functions from FrontDoorAPIBase.py
to return values of interest.
"""

import json
import time

from tenacity import retry, stop_after_delay

from ..LoggerUtils.CastleLogger import get_logger


def wait_for(func, *args, **kwargs):
    """
    Keep calling a function until successful or has reached timeout.

    timeout kwarg: will determine how long to wait for, if not present will wait for default period of 30 seconds
    before exiting if call is not successful
    delay kwarg: will delay execution upon successful function call. This can be useful when playing something
    and you want to let play for a period before returning

    :param func: function or lambda expression that will perform a check that should return a boolean value
    :param args: Optional arguments
    :param kwargs: Keyword arguments
    :return: whether call was successful
    """
    timeout = kwargs.get("timeout", 30)
    delay_after_success = kwargs.get("delay", 0)
    sleep_interval = kwargs.get("sleep_interval", 1)
    timeout += time.time()

    while time.time() < timeout:
        try:
            if func(*args):
                if delay_after_success is not None:
                    # This allows delay after successful completion
                    time.sleep(delay_after_success)
                return True
        except (AttributeError, KeyError):
            # Ignore these and retry
            pass
        time.sleep(sleep_interval)
    return False


class FrontDoorUtilities(object):
    """Collection of methods that access FrontDoor either using frontdoorutil / FrontDoorClient """
    def __init__(self, front_door, logger=None):
        self.front_door = front_door
        self.logger = logger or get_logger(__name__)

    def wait_for_power_state(self, power, timeout=60):
        """
        Wait until power state reaches the given value,

        :param power: "ON", "OFF"
        :param timeout: how long in seconds before timing out
        :return: True if reached given state
        """
        success = wait_for(lambda b: self.get_power_control() == power, power, timeout=timeout)
        if not success:
            self.logger.warning("Expected power state %s never reached; current state: %s",
                                power, self.get_power_control())
        return success

    def wait_for_play_state(self, state, timeout=60, delay=0):
        """
        Checks the speaker now playing state until it matches the state
        :param timeout: How long to wait in seconds
        :param state: "play", "stop", pr "pause" (pause and stop are interchangable)
        :param delay: Number of seconds to wait after the play state is correct before returning
        :return: boolean
        """
        success = wait_for(lambda b: self.get_playstate().lower() == state.lower(), state, timeout=timeout, delay=delay)
        if not success:
            self.logger.warning("Timed out waiting for play state to reach %s, current state is: %s",
                                state, self.get_playstate())
        return success

    def wait_for_source(self, sourcename, timeout=30, delay=0):
        """
        Checks the source display name until it matches the source requested or timeout
        :param timeout: How long to wait in seconds
        :param sourcename: "ALEXA", "iHeart", "Deezer", "TuneIn", "Amazon", "Pandora"
        :param delay: Number of seconds to wait after the play state is correct before returning
        :return: boolean
        """
        success = wait_for(lambda b:
                           self._get_now_playing_data("source", "sourceDisplayName").lower() == sourcename.lower(),
                           sourcename, delay=delay, timeout=timeout)
        if not success:
            self.logger.warning("Timed out waiting for source to be %s", sourcename)
        return success

    def wait_for_track_change(self, original_track, timeout=30, delay=0):
        """
        Wait up to specified timeout for track to change

        :param original_track: Whether
        :param timeout: How long to wait in seconds
        :param delay:
        :return: True if track has changed within specified timeout
        """
        success = wait_for(lambda b: self.get_track() != original_track, original_track, delay=delay, timeout=timeout)

        if not success:
            self.logger.warning("Failed to change track")
        return success

    def wait_for_zone_disbanded(self, timeout=30):
        """
        Keep getting zone info until zone has been disbanded or timeout is reached
        :param timeout: How long to wait in seconds
        :return: True if zone disbanded; False otherwise
        """
        master = "master"
        success = wait_for(lambda b: master not in self.front_door.getZone()["body"], master, timeout=timeout)

        if not success:
            self.logger.warning("Zone wasn't disbanded within specified time %d", timeout)
        return success

    def _get_now_playing_data(self, *keys):
        now_playing = self.front_door.getNowPlaying()
        try:
            now_playing = now_playing["body"]
            for key in keys:
                now_playing = now_playing[key]
            return now_playing
        except KeyError as err:
            self.logger.error("KeyError: key: %s response: %s", err.message, now_playing)

    def get_track(self):
        """
        :return: Name of current track
        """
        return self._get_now_playing_data("track", "contentItem", "name")

    def get_all_track_content(self):
        """
        :return: track contentItem as dict
        """
        return self._get_now_playing_data("track", "contentItem")

    def get_now_playing_metatdata(self):
        """
        :return: metadata as dict
        """
        return self._get_now_playing_data("metadata")

    def get_album(self):
        """
        :return: name of album of current track
        """
        return self._get_now_playing_data("metadata", "album")

    def get_artist(self):
        """
        :return: name of artist of current track
        """
        return self._get_now_playing_data("metadata", "artist")

    def get_playstate(self):
        """
        :return: play state status
        """
        return self._get_now_playing_data("state", "status")

    def is_currently_playing(self):
        """
        :return: True if currently playing; False if not
        """
        play_state = self.get_playstate()
        return play_state is not None and play_state.lower() == "play"

    def get_source(self):
        """
        :return: contentItem source
        """
        return self._get_now_playing_data("container", "contentItem", "source")

    def get_msp_source(self):
        """
        :return: source display name
        """
        return self._get_now_playing_data("source", "sourceDisplayName")

    def get_language(self):
        """
        :return: language code
        """
        return self.front_door.getLanguage()

    def get_volume(self):
        """
        :return: return volume value
        """
        response = self.front_door.getVolume()
        return response["body"]["value"]

    def get_mute_state(self):
        """
        :return: mute state
        """
        response = self.front_door.getVolume()
        return response["body"]["muted"]

    def get_power_control(self):
        """
        :return: power control state
        """
        try:
            response = self.front_door.getSystemPowerControl()
            return response["body"]["power"]
        except ValueError:
            self.logger.error("Unable to retrieve power control settings, please retry")
            return None

    @retry(stop=stop_after_delay(20))
    def set_volume(self, volume):
        """
        Set volume to a specific integral value
        :param volume: int of volume
        :return:
        """
        data = json.dumps({"value": volume})
        response = self.front_door.sendVolume(data)
        return response

    def set_power_on(self):
        """
        Power On device
        :return:
        """
        data = json.dumps({"power": "ON"})
        response = self.front_door.setSystemPowerControl(data)
        return response

    def set_power_off(self):
        """
        Power off device
        :return:
        """
        data = json.dumps({"power": "OFF"})
        response = self.front_door.setSystemPowerControl(data)
        return response

    def get_current_play_time(self):
        """
        Get time into track info
        :return: timeIntoTrack value
        """
        return self._get_now_playing_data("state", "timeIntoTrack")

    def sendTransportControl(self, state):
        """
        send transport control (play, pause, skipNext, skipPrevious, etc)
        :param state: play, pause, skipNext, skipPrevious
        :return:
        """
        self.front_door.sendTransportControl(json.dumps({"state": state}))

    def get_account(self, source_name):
        """
        source_name: DEEZER, AMAZON, PANDORA
        :param source_name: source name
        :return: sourceAccountName
        """
        response = self.front_door.getSources()
        for source in response["body"]["sources"]:
            if source["sourceName"] == source_name:
                return source["sourceAccountName"]

    def play_deezer_on_demand(self,
                              album_location="8493391",
                              album_name="Wonders",
                              track_location="84309795",
                              track_name="Summer Jam"):
        """
        Plays a deezer track
        if track info is omitted, it will play the default track
        :param album_location: Deezer location for the containing album
        :param album_name: Name of the containing album
        :param track_location: Deezer location of the track
        :param track_name: Name of the track
        :return:
        """
        account = self.get_account("DEEZER")
        if not account:
            self.logger.error("No Deezer account found on system")
            return

        data = json.dumps({"source": "DEEZER",
                           "sourceAccount": account,
                           "preset": {"type": "tracklisturl",
                                      "location": "/v1/playback/containerType/album/containerId/" + album_location,
                                      "name": album_name,
                                      "presetable": "true",
                                      "containerArt": ""},
                           "playback": {"type": "tracklisturl",
                                        "location": "/v1/playback/containerType/album/containerId/"
                                                    + album_location + "/track/" + track_location,
                                        "name": track_name,
                                        "presetable": "true"}}, indent=4)

        self.logger.info("The data going to be sent is %s", data)
        return self.front_door.sendPlaybackRequest(data)

    def play_iheartradio(self,
                    name="106.7 Lite fm",
                    location= "/playback/containerType/live/containerId/1477/containerName/106.7 Lite fm"):

        """ Plays an iheartradio station"""
        account = self.get_account("IHEART")
        data = json.dumps({"source": 'IHEART',
                           "sourceAccount": account,
                           "preset": {"type": "stationurl",
                                      "location": location,
                                      "name": name,
                                      "presetable": "true"},
                           "playback": {"type": "stationurl",
                                        "location": location,
                                        "name": name,
                                        "presetable": "true",}}, indent=4)
        self.logger.info("The data going to be sent is %s", data)
        self.front_door.sendPlaybackRequest(data)


    def play_spotify(self,
                    name="Daily Mix 1",
                    location= "/playback/container/c3BvdGlmeTpwbGF5bGlzdDozN2k5ZFFaRjFFMzl4eTl5d3lNY20x"):

        """ Plays Daily Mix 1 Playlist on Spotify"""
        account = self.get_account("SPOTIFY")
        data = json.dumps({"source": 'SPOTIFY',
                           "sourceAccount": account,
                           "preset": {"type": "tracklisturl",
                                      "location": location,
                                      "name": name,
                                      "presetable": "true"},
                           "playback": {"type": "stationurl",
                                        "location": location,
                                        "name": name,
                                        "presetable": "true",}}, indent=4)
        self.logger.info("The data going to be sent is %s", data)
        self.front_door.sendPlaybackRequest(data)


    def play_tunein(self,
                    name="100.7 WZLX",
                    location="/playback/station/s28589",
                    containerArt="http://cdn-radiotime-logos.tunein.com/s28589q.png"):
        """ Plays a Tune-In station """
        data = json.dumps({"source": 'TUNEIN',
                           "sourceAccount": "",
                           "preset": {"type": "stationurl",
                                      "location": location,
                                      "name": name,
                                      "presetable": "true",
                                      "containerArt": containerArt},
                           "playback": {"type": "stationurl",
                                        "location": location,
                                        "name": name,
                                        "presetable": "true",
                                        "containerArt": containerArt}}, indent=4)
        self.logger.info("The data going to be sent is %s", data)
        self.front_door.sendPlaybackRequest(data)

    def play_amazon(self,
                    location="cHJpbWUvc3RhdGlvbnMvQTEwMlVLQzcxSTVEVTgvI3BsYXlhYmxl/trackIndex/0",
                    name="Classic Hits"):
        """
        Plays an Amazon station
        :param location:
        :return:
        """
        account = self.get_account("AMAZON")
        if not account:
            self.logger.error("No Amazon account found on system")
            return
        data = json.dumps({"source": "AMAZON",
                           "sourceAccount": account,
                           "preset": {"type": "tracklisturl",
                                      "location": "/v1/playback/type/playable/url/" + location,
                                      "name": name,
                                      "presetable": "true", "containerArt": ""},
                           "playback": {"type": "tracklisturl",
                                        "location": "/v1/playback/type/playable/url/" + location,
                                        "presetable": "true"}}, indent=4)

        self.logger.info("The data going to be sent is %s", data)
        self.front_door.sendPlaybackRequest(data)

    def play_pandora(self, name="The Beatles Radio", location="/v1/playback/token/3828911929411831692"):
        """
        Plays a pandora station

        :param name:
        :param location:
        :return:
        """
        account = self.get_account("PANDORA")
        data = json.dumps({"source": "PANDORA",
                           "sourceAccount": account,
                           "preset": {"type": "tracklisturl",
                                      "location": location,
                                      "name": name,
                                      "presetable": "true"},
                           "playback": {"type": "tracklisturl",
                                        "location": location,
                                        "name": name,
                                        "presetable": "true"}}, indent=4)

        self.logger.info("The data going to be sent is %s", data)

        self.front_door.sendPlaybackRequest(data)

    def set_favorite(self, favorite):
        """
        Set favorite true/false
        :param favorite: should be 'true' (for favorite) or 'false'
        :return:
        """
        if favorite:
            state = "true"
        else:
            state = "false"
        data = json.dumps({"state": state})
        response = self.front_door.set_favorites(data)
        self.logger.info("Set Favorite Response %s", response)

    def get_art_url(self):
        """
        Returns the art text url
        return: String album name
        """
        return self._get_now_playing_data("container", "contentItem", "containerArt")

    def get_total_play_time(self):
        """
        :return: Total play_time
        """
        return self._get_now_playing_data("metadata", "duration")

    def get_change_report_data(self):
        """ collects from the speaker all of the data needed to verify the change report event
        removed: "trackId": "get_trackid", "artistId": "get_artistid", "albumId": "get_albumid",
        "positionMilliseconds": "get_current_play_time","""
        collect = {"state": "_get_state",
                   "supportedOperations": "_get_supported_operations",
                   "playbackSource": "_playbackSource",
                   "trackName": "get_track",
                   "artist": "get_artist",
                   "album": "get_album",
                   "coverUrls": "get_art_url",
                   "mediaProvider": "get_source",
                   "media_type": "get_track",
                   "durationInMilliseconds": "get_total_play_time",
                   "shuffle": "_get_shuffle",
                   "repeat": "_get_repeat",
                   "favorite": "_get_favorite",
                   "positionMilliseconds": "get_current_play_time"}
        data = {}

        for item in collect:
            data[item] = getattr(self, collect[item])()

        # change the seconds to milliseconds
        try:
            data["positionMilliseconds"] = int(data["positionMilliseconds"]) * 1000
        except KeyError:
            data["positionMilliseconds"] = ""

        try:
            data["durationInMilliseconds"] = int(data["durationInMilliseconds"]) * 1000
        except KeyError:
            data["durationInMilliseconds"] = ""

        return data

    def _get_state(self):
        playstate = self._get_now_playing_data("state", "status")
        if "play" in playstate:
            return "PLAYING"
        elif "pause" in playstate:
            return "PAUSED"
        elif "stop" in playstate:
            return "STOPPED"
        elif "buffer" in playstate:
            return "BUFFERING"
        else:
            return playstate

    def _playbackSource(self):
        return self._get_now_playing_data("source", "sourceDisplayName")

    def _get_supported_operations(self):
        operations = ["Play"]
        now_playing = self._get_now_playing()
        if now_playing["body"]["container"]["capabilities"]["skipNextSupported"]:
            operations.append("Next")
        if now_playing["body"]["container"]["capabilities"]["skipPreviousSupported"]:
            operations.append("Previous")

        # todo: find a better way to do this
        source = now_playing["body"]["source"]["sourceDisplayName"]
        stop_sources = ["TUNEIN", "SIRIUSXM", "IHEART"]  # iheart can go either way...
        pause_sources = ["DEEZER", "PANDORA", "AMAZON", "SPOTIFY", "INTERNET_RADIO", "LOCAL_MUSIC", "STORED_MUSIC",
                         "STANDBY"]
        if source in stop_sources:
            operations.append("Stop")
        if source in pause_sources:
            operations.append("Pause")
        return operations

    def _get_now_playing(self):
        return self.front_door.getNowPlaying()

    def _get_shuffle(self):
        return self._get_now_playing_data("state", "shuffle")

    def _get_repeat(self):
        return self._get_now_playing_data("state", "repeat")

    def _get_favorite(self):
        favorite = self._get_now_playing_data("track", "favorite")

        if favorite == "no":
            return "NOT_RATED"
        else:
            return "FAVORITED"

    def get_system_state(self):
        """
        :return: system state
        """
        system_state = self.front_door.getSystemState()
        try:
            system_state = system_state["body"]["state"]
            return system_state
        except KeyError as err:
            self.logger.error("KeyError: key: %s response: %s", err.message, system_state)

    def get_info(self):
        """
        :return: system info
        """
        info = self.front_door.getInfo()
        return info



@retry(stop=stop_after_delay(20))
def validate_devices_playing_same_content(devices, expected_play_status, expected_source=None):
    """
    Common validation for multi-device validation that same content is playing on all speakers
    at the same time. If expected_source is provided verify that current source is matches specified value
    otherwise simply verify that all devices are playing from same source.

    Note: Metadata includes album, artist, trackName and duration.

    :param devices: list of Device objects
    :param expected_play_status: status as str ("PLAY", "PAUSED", etc)
    :param expected_source: expected source of play content (optional)
    :return: None
    """
    track_info = None

    for device in devices:
        currently_playing = device.front_door.getNowPlaying()
        assert currently_playing["body"]["state"]["status"].lower() == expected_play_status.lower()
        assert currently_playing["body"]["metadata"] is not None, "Failed to retrieve now playing track info"
        assert currently_playing["body"]["source"] is not None, "Failed to retrieve source from now playing"

        if track_info is None:
            track_info = currently_playing["body"]["metadata"]
            if expected_source is None:
                expected_source = currently_playing["body"]["source"]["sourceDisplayName"]
        else:
            assert currently_playing["body"]["metadata"] == track_info, "Different music is playing on each device"
            assert currently_playing["body"]["source"]["sourceDisplayName"] == expected_source, \
                "Different sources are playing on each device; actual {actual}, expected {expected}"\
                .format(actual=currently_playing["body"]["source"]["sourceDisplayName"], expected=expected_source)


def validate_play_status_multiple_devices(devices, expected_play_status):
    """
    Verify that each of the supplied devices is in expected play status (PLAY, PAUSED, STOP)

    :param devices: list of Device objects
    :param expected_play_status: expected status as str
    :return: None
    """
    for device in devices:
        assert device.frontdoor_utils.wait_for_play_state(expected_play_status)


def validate_track_change_multiple_devices(devices, original_track):
    """
    Verify that the track has changed on each device. Helpful when giving directive that should change track
    on a multi-device setup
    :param devices:  list of Device objects
    :param original_track: Track that should change (str)
    :return:
    """
    for device in devices:
        assert device.frontdoor_utils.wait_for_track_change(original_track=original_track), \
            "Track didn't change for device {}".format(device.device_name)


def validate_zone_info(devices, zone_info):
    """
    Common assertion to validate that zone information is created for a group of devices. It's unknown which device in
    a media group will be designated the master, so this simply verifies the master is one of the listed devices
    provided. This should only called when a group is formed, such as when a directive is given to play
    something while targeting the space

    :param devices: list of Device objects
    :param zone_info: Zone info as dict (as retrieved from front_door)
    :return: None
    """
    assert "master" in zone_info["body"], "Master not defined for provided zone"
    assert "members" in zone_info["body"], "Members list is empty for given zone"

    assert len(zone_info["body"]["members"]) == len(devices) - 1, \
        "Zone Info {} has incorrect number of members".format(str(zone_info))

    master_in_group = False

    for device in devices:
        if device.device_ip == zone_info["body"]["master"]["ip"]:
            master_in_group = True
            assert zone_info["body"]["master"]["guid"] == device.product_guid
        else:
            member_in_group = False
            for member in zone_info["body"]["members"]:
                if device.device_ip == member["ip"]:
                    assert member["guid"] == device.product_guid
                    member_in_group = True
                    break
            assert member_in_group, "Device {} was not present in zone members".format(device.device_name)

    assert master_in_group, "Master doesn't match device defined in media group"
