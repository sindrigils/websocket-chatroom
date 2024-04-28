from dotenv import load_dotenv

from os import environ
import threading
import socket

from sqlalchemy.orm import sessionmaker
from servers.server import ChatServer
from db.models import Server, Client
from db.db import engine


load_dotenv()
HOST = environ.get("HOST")


class ChatServerManager:
    def __init__(self):
        self.servers = {}
        self.port = 8765

    def get_next_port(self):
        port = self.port
        self.port += 1
        return port

    def create_server(self, name: str, client_name: str):

        port = self.get_next_port()
        chat_server = ChatServer(HOST, port, name)

        server_thread = threading.Thread(target=chat_server.receive)
        server_thread.start()

        self.servers[name] = {
            "server": chat_server,
            "thread": server_thread,
            "port": port,
        }

        Session = sessionmaker(engine)
        session = Session()

        client = session.query(Client).filter_by(username=client_name).first()
        server = Server(name=name, port=port, admin=client.id)

        session.add(server)
        session.commit()
        session.close()

        print(f"Server '{name}' created on port {port}.")

    def close_server(self, name: str):
        server: socket.socket = self.servers[name]

        server["server"].close()
        server["thread"].join()

        Session = sessionmaker(engine)
        session = Session()

        server_to_delete = session.query(Server).filter_by(name=name).first()
        session.delete(server_to_delete)
        session.commit()
        session.close()

    def list_all_servers(self):
        Session = sessionmaker(engine)
        session = Session()

        servers = session.query(Server).all()
        for idx, server in enumerate(servers):
            print(f"{idx+1}) {server.name}")

    def list_all_owned_servers(self):
        for idx, (name, server) in enumerate(self.servers.items(), start=1):
            print(f"{idx})")
            print(f"name: {name}")
            print(f"port: {server["port"]}")
            if idx != len(self.servers): print()

    def get_server_port(self, server_name):

        Session = sessionmaker(engine)
        session = Session()
        server = session.query(Server).filter_by(name=server_name).first()
        session.close()

        return server.port

    def close_all(self):
        for name in self.servers.keys():
            self.close_server(name)

        self.servers = {}


if __name__ == "__main__":
    pass
