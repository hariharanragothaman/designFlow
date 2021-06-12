"""
Utility to send WebSocket requests through FrontDoor
"""
import argparse
import datetime
import json
import ssl
import _thread
import threading
import time
import websocket

from .FrontDoorAPIBase import FrontDoorAPIBase
from ..LoggerUtils.CastleLogger import get_logger
from ..NetworkUtils.Telnet import TelnetSession
from ..OAuthUtils.OAuthUtils import UserAccount

APIKEY = "67616C617061676F732D6E6F6E2D70726F642D746972616D6973752D746573742D73637269707473"
RESPONSE_TIMEOUT = "Response Timeout"

class FrontDoorAPI(FrontDoorAPIBase):
    """
    Class to communicate with target device via WebSocket connection
    """

    def __init__(self, ip, port=8082, env='integration', logger=None, access_token=None, email=None, password=None):
        """
        Instantiates a connection to the device's Front Door via a WebSocket.
        May use a JWT (access_token) or Email/Password combintation to instantiate.

        JWT (access_token) should be valid if used.

        Email/Password combination must be an active account.

        :param ip: IP Address of the Device connection
        :param port: Port that will connect to the Front Door on the device
        :param env: User Environment
        :param logger: Python Logging logger object
        :param access_token: Java Web Token (jwt) string
        :param email: Email Address for connection account
        :param password: Password associated with email address
        """
        self.logger = logger or get_logger(__name__)

        self._endpointmap = {}
        self._jsonIn = []
        self._isOpen = False
        self._msgCb = None

        self._web_socket_timeout = 150
        self._request_id = 0

        self._last_notification = ""

        self.gigya_url = 'https://ingress-platform.live-aws-useast1.bose.io/dev/svc-id-gen-pub/{}/id-user-accounts-core/userAccounts/'

        self._open_event = threading.Event()
        self._close_event = threading.Event()

        self._ip_address = ip
        self._port = port
        self.logger.info("The port currently in use is: %s", self._port)
        self.logger.info("The IP address of the target is: %s", self._ip_address)

        # Define our environment and connection URL
        self._env = env
        self.gigya_url = self.gigya_url.format(self._env)

        self._access_token = access_token

        if access_token and email and password:
            raise ValueError("Please use either access_token or email/password.")

        # If we are in [local], we don't care about the token
        # If we are given a token, we use the token
        # If we are given an email/password, we generate a token
        if self._ip_address not in ['127.0.0.1', 'localhost'] and self._access_token is None:
            if email is None or password is None:
                raise ValueError('email/password must be set if not local connection or supplying JWT.')
            self._email = email
            self._password = password
            self.generate_token()

        self.open()

    def check_before_open(self):
        """
        Actually checks if FrontDoor process has started listening on PORT:8082
        Q: Is this dependent on misc factors?
           The product takes some time download the server.crt from the cloud
           to start servicing the port.
           server.crt is in /mnt/nv/product-persistence
        """
        _cert_timeout = 5 * 60
        _fd_flag = False
        start_time = time.time()
        telnet_conn = None
        while time.time() < _cert_timeout + start_time:
            try:
                telnet_conn = TelnetSession(self._ip_address, 23)

                # Ignore this check on production unit
                # If there is Error 111 while openeing connection then
                # it is assumed to be a production unit.
                if telnet_conn.connection_error and \
                   "[Errno 111] Connection refused" in telnet_conn.connection_error:
                    self.logger.info("It seems to be a production unit, bypassing FrontDoor process check")
                    return True

                telnet_conn.write("netstat -tlnp | grep " + str(self._port))
                response = telnet_conn.read()
                response = response.split('tcp', 1)[-1]
                if response and 'FrontDoor' in response:
                    _fd_flag = True
                    break
            except RuntimeError:
                continue
        if telnet_conn:
            del telnet_conn
        if _fd_flag:
            self.logger.info("FrontDoor is starting to serve on port 8082")
            return True
        return False

    def generate_token(self):
        """
        This generates a 'token' to be injected into the header.
        """
        self.logger.info("Creating an User-Account for generating tokens")

        user_account = UserAccount(url=self.gigya_url, logger=self.logger)
        response = user_account.authenticate_user_account(self._email, self._password)

        self._access_token = response["access_token"]
        self.logger.info("The access token is: %s", self._access_token)


    def add_endpoint(self, endpoint, callbackFunc):
        """
        endpoint map for callback functions - used for notifications
        :param endpoint: resource
        :param callbackFunc: function
        """
        self._endpointmap[endpoint] = callbackFunc

    def open(self, open_socket_time_out=30):
        """
        Opens a WebSocket connection
        Note: There is a sub-protocol, that needs to be passed known as 'Gabbo' protocol
        :param open_socket_time_out: How long to wait, in s, for opening the connection to take
        :return: None
        """
        self._open_event.clear()
        self._close_event.clear()
        self.logger.debug("Opening Web Socket connection to the device with IP: %s", self._ip_address)
        self._jsonIn[:] = []

        _clientName = datetime.datetime.now().isoformat()
        if self._ip_address not in ['127.0.0.1', 'localhost']:
            tflag = self.check_before_open()
            self.logger.info("The value of tflag: %s", tflag)
            if not tflag:
                raise websocket.WebSocketTimeoutException("FrontDoor not Listening on port 8082")
            if int(self._port) == 8082:
                self.fd_url = "wss://" + self._ip_address + ":" + str(self._port) + "/?product=EddieTest" + _clientName
                self.logger.info("The websocket url is: {}".format(self.fd_url))
                self._wss = websocket.WebSocketApp(self.fd_url,
                                                   subprotocols=['eco2'],
                                                   on_message=self._onMessage,
                                                   on_error=self._onError,
                                                   on_close=self._onClose)

            if int(self._port) == 8086:
                self.fd_url = "ws://" + self._ip_address + ":" + str(self._port) + "/?product=EddieTest" + _clientName
                self.logger.info("The websocket url is: {}".format(self.fd_url))
                self._wss = websocket.WebSocketApp(self.fd_url,
                                                   subprotocols=['eco2'],
                                                   on_message=self._onMessage,
                                                   on_error=self._onError,
                                                   on_close=self._onClose)
        else:
            self._wss = websocket.WebSocketApp("ws://127.0.0.1:" + str(self._port),
                                               on_message=self._onMessage,
                                               on_error=self._onError,
                                               on_close=self._onClose)
        self.json_in_event = threading.Event()
        self.json_in_event.clear()
        self._wss.on_open = self._onOpen
        self._run()

        open_socket_start_time = time.time()
        self.logger.debug("Waiting for WebSocket connection to be established.")
        while not self._wss.sock:
            if (time.time() - open_socket_start_time) > open_socket_time_out:
                raise websocket.WebSocketTimeoutException('Failed to acquire a socket after {}s'
                                                          .format(open_socket_time_out))

        self.logger.debug("Connecting to WebSocket Object: %s", self._wss.sock)

        connected_start_time = time.time()
        while not self._wss.sock.connected:
            if (time.time() - connected_start_time) > self._web_socket_timeout:
                # It's taking too long, better close the connection
                self.logger.error("WebSocket Timeout - No Route to host")
                self._wss.close()
                break

        if not self._open_event.wait(10):
            raise websocket.WebSocketTimeoutException("Failed to received Websocket Open event")

        total_open_time = time.time() - open_socket_start_time

        self.logger.debug("Total time for connection to WebSocket: {:.3f}".format(total_open_time))
        self.logger.info("Is the WebSocket connection established? %s", self._wss.sock.connected)

    def _run(self):
        """
        Creates thread and runs to open WebSocket
        """
        def runloop(*args):
            """
            Calls the run_forever() method of the WebSocket.

            :param args: Arguments to the WebSocket Client run_forever() method
            :return: None
            """
            if int(self._port) == 8082:
                self._wss.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
            else:
                self._wss.run_forever()
        _thread.start_new_thread(runloop, ())

    def close(self):
        """
        Closes the WebSocket connection
        """
        self.logger.info("Closing WebSocket Connection")

        self._wss.close()
        self._isOpen = False
        if not self._close_event.wait(10) and self._wss.sock.connected:
            raise websocket.WebSocketTimeoutException("Failed to received Websocket Close event")

    def _onOpen(self):
        """
        The on_open callback for the WebSocketApp

        :param ws: The WebSocketApp object returned by WebSocketApp.on_open
        :return: None
        """
        self.logger.debug("WebSocket Connection Open")
        self._isOpen = True
        self._open_event.set()

    def _onClose(self):
        """
        The on_close callback for the WebSocketApp

        :param ws: The WebSocketApp object returned by WebSocketApp.on_close
        :return: None
        """
        self.logger.debug("WebSocket Connection Closed")

        self._wss.close()
        self._isOpen = False
        self._close_event.set()

    def isOpen(self):
        """
        Returns the status of the WebSocket is open.

        :return: Boolean of _isOpen
        """
        return self._isOpen

    def _onError(self, error):
        """
        The on_error callback for the WebSocketApp

        :param ws: The WebSocketApp object returned by WebSocketApp.on_error
        :param error: The string error message reported by the WebSocketApp
        :return: None
        """
        self.logger.debug("Web Socket Error Received: %s", error)
        self.close()

    def capture(self, cb=lambda msg, msgId: False):
        """
        Gets the response from the system that matches the Request ID of the current message

        :param cb:
        :return: String response information
        """
        start_time = time.time()
        while True:
            self._msgCb = cb
            response_id = self._request_id

            # To find the response where request ID matches with the expected ID
            for response in self._jsonIn:
                # Loading the JSON response into a python dictionary
                json_object = json.loads(response)

                # This dumps a python dict to a JSON object
                json_response = json.dumps(json_object, sort_keys=True, indent=4)

                if json_object["header"]["reqID"] == response_id:
                    self._jsonIn.remove(response)
                    return json_response

            if (time.time() - start_time) > self._web_socket_timeout:
                # It's taking too long, better close the connection
                self.logger.error("WebSocket Timeout during capture. Took longer than %s", self._web_socket_timeout)
                self._wss.close()
                return RESPONSE_TIMEOUT

    def _onMessage(self, message):
        """
        This function detects if the message is a notification and adds it to the last_notification

        :param ws: The WebSocketApp object returned by WebSocketApp.on_message
        :param message: UTF-8 string from the server parsed by WebSocketApp.on_message
        :return: None
        """
        jsonMsg = json.loads(message)
        val = self._endpointmap.get(jsonMsg['header']['resource'])
        if val:
            val(jsonMsg)
        if '"method":"NOTIFY"' in message:
            self._last_notification = json.loads(message)
            self.logger.debug("Last Notification received:" + json.dumps(self._last_notification, indent=4, sort_keys=True))
        else:
            self._jsonIn.append(message)
            if self._msgCb(message, len(self._jsonIn) - 1):
                self.json_in_event.set()

    def send(self, request_type, api, data="", version = 1, wait_for_response=True):
        """
        Sends data to the FrontDoor API WebSocket

        :param request_type: HTTP Request Type: e.g. GET, POST, PUT
        :param api: The string API on the WebSocket
        :param data: The dictionary body that will be sent
        :return: String response after sending encapsulated message
        """
        self._response = ""
        if not self._isOpen:
            self.open()

        self.logger.debug("Getting status of the WebSocket connection")
        self.logger.debug("WebSocket is Open: %s", self.isOpen())
        self.logger.debug("Sending %s to %s", request_type, api)

        # Encapsulating the JSON, with request type; header etc, into the message
        self.logger.debug("Enveloping data: %s", data)

        env_message = self.envelope_message(request_type, api, data, self._request_id, version)
        self.logger.debug("Enveloped Message to be sent: \n%s", env_message)

        try:
            self._wss.send(str(env_message))
        except websocket.WebSocketConnectionClosedException as exception:
            self._isOpen = False
            self.logger.error("Exception in send() - %s", str(exception))
            return "WebSocket not connected"

        # Gets the response
        self.logger.debug("Getting the response for: %s", api)
        if wait_for_response:
            self._response = self.capture()

        # Printing the response
        self.logger.debug("The returned response is:\n%s", self._response)

        # Increment the counter for the next time
        self._request_id += 1

        # Reset Counter if we get a lot of requests
        if self._request_id > 9999:
            self._request_id = 0

        return self._response

    def envelope_message(self, request_type, api, data, request_id, version = 1):
        """
        Generates proper message format for the FrontDoor WebSocket

        :param request_type: HTTP Request Type: e.g. GET, POST, PUT
        :param api: The string API on the WebSocket
        :param data: The dictionary body that will be sent
        :param request_id: Internal integer to this class that is
            incremented on send
        :return: The string JSON message
        """
        if request_type == "NOTIFY":
            _header = {"header":{
                "resource": api,
                "version": version,
                "device": "GUID",
                "method": request_type,
                "reqID": request_id}}
        else:
            _header = {"header": {
                "resource": api,
                "version": version,
                "token": self._access_token,
                "method": request_type,
                "msgtype": "REQUEST",
                "device": "GUID",
                "reqID": request_id}}

        self.logger.debug("The header Json string: %s", _header)
        self.logger.debug("The data received in JSON string is: \n%s", data)

        if request_type.lower() == "get":
            _message = json.dumps(_header, indent=4)

        elif request_type.lower() == "post" or "put":
            # Converting the header and into a Python Dict
            _header["body"] = json.loads(data)

            # Constructing the message to be sent
            _header = json.dumps(_header, indent=4)
            _message = _header
        else:
            _message = "Non-supported type"

        self.logger.debug("The value of the message is: %s", _message)
        return _message

    def last_notification(self):
        """
        Returns the last_notification handled.

        :return: the Last Notification on the WebSocket
        """
        return self._last_notification


def main(arguments):
    """
    Simple check that the FrontDoor API will get the languages on the system.

    :param arguments: ArgParser based arguments
    :return: None
    """
    front_door = FrontDoorAPI(arguments.ip_address, access_token=arguments.token)
    front_door.getLanguage()

    if front_door:
        front_door.close()

def parse_arguments():
    """"
    Parses command line arguments to the __main__ function.

    :return: Namespace parsed command line arguments.
    """
    parser = argparse.ArgumentParser(
        description="Uses the FrontDoor API against the target IP Address to get the languages.")
    parser.add_argument('--ip-address', action='store', type=str, required=True,
                        help='The IP Address of the target.')
    parser.add_argument('--token', action='store', type=str,
                        help='The JWT used for the connection.')

    return parser.parse_args()


if __name__ == "__main__":
    main(parse_arguments())
