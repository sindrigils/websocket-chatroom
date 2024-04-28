from colorama import Fore, Style

import threading
import socket

from utils.common import DISCONNECT_MESSAGE, FORMAT


class ChatServer:
    def __init__(self, host: str, port: int, name: str) -> None:
        self.name = name

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen()
        self.clients = []
        self.nicknames = []

    def broadcast(self, message: str, sender: socket.socket = None):
        for client in self.clients:
            if client == sender:
                message = message.decode(FORMAT)
                message_split = message.split(":", 1)
                message = (
                    f"{Fore.RED}{message_split[0]}{Style.RESET_ALL}" + message_split[-1]
                ).encode(FORMAT)

            client.send(message)

    def handle_client(self, client: socket.socket):
        while True:
            try:
                message = client.recv(1024)
                if message.decode(FORMAT).upper() == DISCONNECT_MESSAGE:
                    self.close_client(client)
                    break

                self.broadcast(message, client)
            except:
                break

    def receive(self):
        while True:
            try:
                client, address = self.server.accept()
                print(f"{Fore.GREEN}Connected with {str(address)}{Style.RESET_ALL}")

                nickname = client.recv(1024).decode(FORMAT)
                self.nicknames.append(nickname)
                self.clients.append(client)

                self.broadcast(
                    f"{Fore.BLUE}{nickname} joined the chat!\n{Style.RESET_ALL}".encode(
                        FORMAT
                    ),
                )
                client.send("Connected to the server!".encode(FORMAT))

                thread = threading.Thread(target=self.handle_client, args=(client,))
                thread.start()

            except ConnectionAbortedError or OSError:
                break

    def close(self):
        self.server.close()

        for client in self.clients:
            client.close()

    def close_client(self, client: socket.socket):
        index = self.clients.index(client)
        self.clients.remove(client)
        client.close()

        nickname = self.nicknames[index]
        self.broadcast(
            f"{Fore.BLUE}{nickname} left the chat!{Style.RESET_ALL}".encode(FORMAT)
        )
        self.nicknames.remove(nickname)


if __name__ == "__main__":
    pass
