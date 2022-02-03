import pickle
import socket
import time
from datetime import datetime
from ChatPayload import ChatPayload
import select
import sys
from _thread import *




def timer():
    app_time = time.time()
    while True:
        new_time = time.time()
        if new_time - app_time > 120:
            print(f"[{datetime.now()}] Server On")
            app_time = new_time


class Chat:
    def __init__(self, ip_address: str, port: int):
        # Setting variables
        self._ip_address = ip_address
        self._port = port
        self._list_of_clients = []
        self._connection = None

        print(f"[{datetime.now()}] Starting Server on {self._ip_address}")
        self._server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        print(f"[{datetime.now()}] Binding IP and Port")
        self._server.bind((ip_address, port))

        print(f"[{datetime.now()}] Listening on port: {self._port}")
        self._server.listen(100)
        print(f"[{datetime.now()}] Server Started")

    """Using the below function, we broadcast the message to all
    clients who's object is not the same as the one sending
    the message """

    def _broadcast(self, message, connection):
        for clients in self._list_of_clients:
            if clients != connection:
                try:
                    clients.send(message)
                except:
                    clients.close()

                    # if the link is broken, we remove the client
                    self._remove(clients)

    def _client_thread(self, connection, addr):
        # sends a message to the client whose user object is conn
        msg = ChatPayload()
        msg.text_payload = "Bem Vindo ao Chat"
        print(msg)
        connection.send(pickle.dumps(msg))

        while True:
            try:
                message = connection.recv(2048)
                if message:

                    """prints the message and address of the
                    user who just sent the message on the server
                    terminal"""
                    print("<" + addr[0] + "> " + message)

                    # Calls broadcast function to send message to all
                    message_to_send = "<" + addr[0] + "> " + message
                    self._broadcast(message_to_send, connection)

                else:
                    """message may have no content if the connection
                    is broken, in this case we remove the connection"""
                    self._remove(connection)
            except:
                continue

    """The following function simply removes the object
    from the list that was created at the beginning of
    the program"""

    def _remove(self, connection):
        if connection in self._list_of_clients:
            self._list_of_clients.remove(connection)

    def loop(self):
        print(f"[{datetime.now()}] Server On")
        start_new_thread(timer, ())
        while True:
            """Accepts a connection request and stores two parameters,
                conn which is a socket object for that user, and addr
                which contains the IP address of the client that just
                connected"""
            self._connection, address = self._server.accept()

            """Maintains a list of clients for ease of broadcasting
            a message to all available people in the chatroom"""
            self._list_of_clients.append(self._connection)

            # prints the address of the user that just connected
            print(f"[{datetime.now()}] {address[0]} connection has been established")

            # creates and individual thread for every user
            # that connects
            start_new_thread(self._client_thread, (self._connection, address))

    def __del__(self):
        self._connection.close()
        print(f"[{datetime.now()}] Connection Closed")
        self._server.close()
        print(f"[{datetime.now()}] Server Closed")
