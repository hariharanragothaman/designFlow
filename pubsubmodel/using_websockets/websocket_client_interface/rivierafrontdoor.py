"""
rivierafrontdoor.py

Access the Castle Product FrontDoor through a Riviera Connection
"""

import json
import logging

from .FrontDoorAPIBase import FrontDoorAPIBase
from ..LoggerUtils.CastleLogger import get_logger
from ..exception import BoseRequiredArgNotFoundError

FRONTDOORUTIL = "/opt/Bose/bin/frontdoorutil"


class FrontDoorUtil(FrontDoorAPIBase):
    """
    Inheritance from the FrontDoorAPIBase and uses the ADB internal command
    frontdoorutil to send FrontDoor commands.
    """

    def __init__(self, riviera, logger=None):
        """
        Initialize connection with riviera

        :param riviera: RivieraUtils Instance
        :param logger: Python Logging logger object
        """
        self.riviera = riviera
        self.logger = logger or get_logger(name=self.__class__.__name__, level=logging.DEBUG)

    def send(self, request_type, api, data="", wait_for_response=True):  # pylint: disable=unused-argument
        """
        Send data to the API, return response

        :param request_type: The RESTful method
        :param api: The API endpoint
        :param data: String JSON formatted data to apply to the message
        :param wait_for_response: unused inheritance of FrontDoorAPI
        :return: A string response, that is json-formatted
        """
        self.logger.info("Executing frontdoor riviera command")

        if request_type not in ["GET", "PUT", "POST"]:
            raise BoseRequiredArgNotFoundError("Request Type ({}) not allowed. Must be {}".format(
                request_type, ["GET", "PUT", "POST"]))

        # Convert data to json format
        if data and isinstance(data, str):
            # Strip any spaces
            data = data.strip()
            data = json.dumps(json.loads(data))
        elif data and isinstance(data, dict):
            data = json.loads(data)

        # Quote the data appropriately
        if data:
            data = '\'{}\''.format(data)
            # data = data.replace('"', '\\"')
            self.logger.debug("Data to send: %s", data)

        # Build command
        command = FrontDoorUtil._build_command(request_type, api, data)

        # Execute command on riviera device
        self.logger.debug("Message to send: %s", repr(command))
        response = self.riviera.communication.executeCommand(command)

        # Return response
        return response

    @staticmethod
    def _build_command(request_type, api, data=""):
        """
        Build the command to execute

        :param request_type: The RESTful method
        :param api: The API endpoint
        :param data: String JSON formatted data to apply to the message
        :return: command to execute
        """
        command = [FRONTDOORUTIL, '-c', request_type, api]
        if data:
            command.append(data)
        command = " ".join(command)
        return command
