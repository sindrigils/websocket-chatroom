import threading
import socket

from utils.common import FORMAT, DISCONNECT_MESSAGE


class ConnectionClosed(Exception):
    def __init__(self, message=""):
        super().__init__(message)


class ChatClient:
    def __init__(
        self, host: str, port: int, disconnect_event: threading.Event, name: str
    ) -> None:
        self.disconnect_event = disconnect_event
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, port))
        self.client.send(name.encode(FORMAT))
        self.name = name

    def receive(self):

        while True:
            try:
                message = self.client.recv(1024).decode(FORMAT)

                if not message:
                    print("Server closed the connection!")
                    raise ConnectionClosed()

                print("\u001B[s", end="")
                print("\u001B[A", end="")
                print("\u001B[999D", end="")
                print("\u001B[S", end="")
                print("\u001B[L", end="")
                print(message, end="")
                print("\u001B[u", end="")
                print("\u001b[K", end="")

            except Exception:
                self.cleanup()
                break

    def write(self):
        while True:
            try:
                user_input = input("")

                if user_input.upper() == DISCONNECT_MESSAGE:
                    self.client.send(user_input.encode(FORMAT))
                    print("You have disconnected!")
                    raise ConnectionClosed()

                message = f"{self.name}: {user_input}\n"
                self.client.send(message.encode(FORMAT))

            except Exception:
                self.cleanup()
                break

    def cleanup(self):
        self.disconnect_event.set()
        self.client.close()


if __name__ == "__main__":
    pass
