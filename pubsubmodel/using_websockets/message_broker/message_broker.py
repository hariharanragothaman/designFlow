#!/usr/bin/env python
import threading
import json
from .websocketServer import WebsocketServer
from .mockFrontDoorBase import MockFrontDoorBase
from threading import Thread
from CastleLogger import get_logger

class MockFrontDoor(MockFrontDoorBase):
    def __init__(self, host='127.0.0.1', port=8084, logger=None):
        self.clienConnectedEvent = threading.Event()
        self.logger = logger or get_logger(__name__)
        self.server = WebsocketServer(port, host)
        self.server.set_fn_new_client(self._new_client)
        self.server.set_fn_client_left(self._client_left)
        self.server.set_fn_message_received(self._message_received)
        self._cb = None
        self._callbackMap = {}
        self.run_thread = None
        self.__resources = {}
        self.__resource_change_event = threading.Event()
        # Called for every client connecting (after handshake)

    def run(self):
        def runloop(*args):
            """
            Calls the run_forever() method of the WebSocket.
            :param args: Arguments to the WebSocket Client run_forever() method
            :return: None
            """
            self.server.run_forever()
        self.run_thread = Thread(target=runloop)
        self.run_thread.start()

    def is_running(self):
        if self.run_thread:
            return self.run_thread.isAlive()
        else:
            return False

    def add_callback(self, resource, cbFunction):
        """
        Add callback to a map that will be called if a given resource is found
        :param resource: ex. /register, /bluetooth/sink/status, etc.
        :param cbFunction: callBack function
        :return:
        """
        self._callbackMap[resource] = cbFunction

    def close(self):
        """
        Close the socket connection and stop thread
        :return:
        """
        self.server.shutdown()
        self.server.server_close()
        if self.run_thread: self.run_thread.join(10)

    def _new_client(self, client, server):
        """
        :param client: client object
        :param server: server object
        """
        self.clienConnectedEvent.set()
        self.logger.info("New client connected and was given id %d" % client['id'])
        self.server.send_message(client, json.dumps(self.readyMsg))

    # Called for every client disconnecting
    def _client_left(self, client, server):
        """
        :param client: client object based on clientID
        :param server: WebSocket server object
        """
        self.__remove_all_resources_for_Client(client)
        self.logger.info("Client(%d) disconnected" % client['id'])

    # Called when a client sends a message
    def _message_received(self, client, server, message):
        """
        :param client:  client object based on clientID
        :param server:  WebSocket server object
        :param message: JSON message
        """
        self.logger.info("Client(%d) said: %s" % (client['id'], message))
        try:
            json_message = json.loads(message)
            resource = str(json_message['header']['resource'])
            """
            When mock frontDoor receives a message from a client that it
            wants to register, and handle the resource
            """
            if resource == '/register':
                self.__add_resource(str(json_message['body']['resource']), client)
                register_message = json_message
                register_message['header']['msgtype'] = "RESPONSE"
                register_message['header']['status'] = 200
                server.send_message(client, json.dumps(register_message))

                return
            """
            When mock frontDoor receives a message and we decide
            to look for it in the callback-map
            """
            val = self._callbackMap.get(resource)
            if val:
                val(json_message)
                return

            """
            When mock frontDoor receives a notification,
            we silent dismiss it for now.
            """
            if json_message['header']['method'] == 'NOTIFY':
                self.logger.info("Received Notify message...")
                self.broadcast(message)
                return
            """
            When mock frontDoor receives a message, that has to be handled, 
            by one of it's clients, it forwards the request
            """
            if resource in self.__resources:
                msg_type = str(json_message['header']['msgtype'])
                self.logger.info("The message type is: %s", msg_type)
                if msg_type == "REQUEST":
                    server.send_message(self.__resources[resource], json.dumps(json_message))
                    return
                elif msg_type == "RESPONSE":
                    self.logger.info("The message is: %s", json.dumps(json_message))
                    if '/test/client' in self.__resources:
                        server.send_message(self.__resources['/test/client'], json.dumps(json_message))
                else:
                    self.logger.info("Neither request, not Response, hence dismissing it.")
            """
            When none of the above conditions are satisified, 
            it looks for a default call-back in mockFrontDoorBase
            """
            output = self.parser(json_message)
            output = json.dumps(output, indent=4)
        except ValueError:
            self.logger.info("Decoding JSON has failed")
        self._send_response(client, server, output)

    def broadcast(self, message):
        """
        Send a message to all client on localhost
        """
        self.logger.info("Sending notifications to all clients")
        self.server.send_message_to_all(message)

    def _send_response(self, client, server, message):
        """
        Sends a message to a specific registered client
        :param client:  client object; based on clientID
        :param server:  WebSocket Server object
        :param message: message to be sent
        """
        server.send_message(client, message)

    def send_message(self, msg):
        resource = str(msg['header']['resource'])
        client = self.__resources.get(resource)
        if client is None:
            raise RuntimeError("Resource Not Found")

        self.server.send_message(client, json.dumps(msg))

    def list_resources(self):
        return list(self.__resources.keys())

    def __add_resource(self, resource, client):
        self.logger.info("Add Resource %s" % resource)
        self.__resources[resource] = client
        self.__resource_change_event.set()
        self.__resource_change_event.clear()

    def __remove_resource(self, resource):
        del self.__resources[resource]
        self.__resource_change_event.set()
        self.__resource_change_event.clear()

    def __remove_all_resources_for_Client(self, client):
        key_to_remove = []
        for key, value in list(self.__resources.items()):
            if value == client:
                key_to_remove.append(key)
        for key in key_to_remove:
            del self.__resources[key]
        if len(key_to_remove) > 0:
            self.__resource_change_event.set()
            self.__resource_change_event.clear()

    def wait_for_client_resource(self, resource, timeout_s):
        key = resource
        step_time = 0.1  # 100ms
        cumulative_time = 0
        if key in self.__resources:
            return True
        while cumulative_time < timeout_s:
            self.__resource_change_event.wait(step_time)
            if key in self.__resources:
                return True
            cumulative_time += step_time
        return False


if __name__ == '__main__':
    mockFront = MockFrontDoor(port=8082)
    mockFront.run()
