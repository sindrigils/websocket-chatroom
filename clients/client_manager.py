from dotenv import load_dotenv

from os import environ
import threading
import logging

from clients.client import ChatClient

load_dotenv()
HOST = environ.get("HOST")

logger = logging.getLogger(__name__)


class ClientManager:
    def __init__(self):
        self.clients = {}

    def join_server(self, client_name: str, server_name: str, port: int):
        disconnect_event = threading.Event()

        client = ChatClient(HOST, port, disconnect_event, client_name)

        receive_thread = threading.Thread(target=client.receive)
        receive_thread.start()

        send_thread = threading.Thread(target=client.write)
        send_thread.start()

        self.clients[client_name] = {
            "client": client,
            "server_name": server_name,
            "port": port,
            "receive_thread": receive_thread,
            "send_thread": send_thread,
            "disconnect_event": disconnect_event,
        }

    def disconnect_client(self, client_name: str):
        client_info = self.clients[client_name]
        client = client_info["client"]

        client.cleanup()

        client_info["receive_thread"].join()
        client_info["send_thread"].join()

        print(f"Client '{client_name}' disconnected.")

    def wait_until_client_disconnects(self, client_name: str):
        if client_name in self.clients:
            client_info = self.clients[client_name]

            disconnect_event = client_info["disconnect_event"]

            disconnect_event.wait()
            self.disconnect_client(client_name)

    def close_all(self):
        for name in self.clients.keys():
            self.disconnect_client(name)
        self.clients = {}
