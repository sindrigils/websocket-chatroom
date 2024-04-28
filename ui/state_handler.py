import bcrypt

from getpass import getpass
import logging

from utils.validators import validate_password, validate_username
from servers.server_manager import ChatServerManager
from clients.client_manager import ClientManager
from sqlalchemy.orm import sessionmaker
from db.models import Client, Server
from ui.state import State
from db.db import engine

logger = logging.getLogger(__name__)


class StateHandler:
    def __init__(self):
        self.client_name = None
        self.server_manager = ChatServerManager()
        self.client_manager = ClientManager()

    def close_all(self):
        self.server_manager.close_all()
        self.client_manager.close_all()

    def auth_page(self):
        print(f"Welcome to ChatRoom!\n" f"1) Login\n" "2) Register\n" f"q) Quit\n")

        while (choice := input("> ")) not in ["1", "2", "q"]:
            print("Invalid option, please try again!")
            print()

        if choice == "1":
            return State.LOGIN

        if choice == "2":
            return State.REGISTER

        if choice == "q":
            return State.QUIT

    def login(self):
        Session = sessionmaker(bind=engine)
        session = Session()

        while True:
            username = input("username (q to quit): ")

            if username == "q":
                break

            password = getpass("password: ")

            user = session.query(Client).filter_by(username=username).first()

            if user:
                if bcrypt.checkpw(password.encode(), user.password.encode()):
                    self.client_name = username
                    print("Login successful!")
                    session.close()
                    return State.MENU

                else:
                    print("Invalid password.")
            else:
                print("User not found.")

        session.close()
        return State.AUTH

    def register(self):
        Session = sessionmaker(bind=engine)
        session = Session()

        while True:

            username = input("username: ")
            while not validate_username(username):
                print("Invalid username")
                username = input("username: ")

            password = getpass("password: ")
            while not validate_password(password):
                print("Invalid password")
                password = getpass("password: ")

            user_exists = session.query(Client).filter_by(username=username).first()
            if user_exists:
                print(
                    f"Username '{username}' is already taken. Please choose a different username."
                )
            else:
                break

        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        new_user = Client(username=username, password=hashed_password.decode())

        session.add(new_user)
        session.commit()

        print("User registered successfully!")
        print()
        session.close()

        self.client_name = username
        return State.MENU

    def menu(self):
        print(
            f"\n"
            f"1) Join server\n"
            f"2) Create server\n"
            f"3) View own servers\n"
            f"q) Quit\n"
        )

        choice = input("> ")

        if choice == "1":
            return State.JOIN_SERVER

        if choice == "2":
            name = input("Sever name: ")
            self.server_manager.create_server(name, self.client_name)
            return State.MENU

        if choice == "3":
            self.server_manager.list_all_owned_servers()
            return State.MENU

        if choice == "q":
            return State.QUIT

    def join_server(self):
        Session = sessionmaker(engine)
        session = Session()

        self.server_manager.list_all_servers()

        server_name = input("Enter server name to join (q to quit): ")
        while not (session.query(Server).filter_by(name=server_name).first()):
            if server_name == "q":
                print()
                session.close()
                return State.MENU

            print("Invalid server name ")
            server_name = input("Enter server name to join (q to quit): ")

        print()

        session.close()
        port = self.server_manager.get_server_port(server_name)
        self.client_manager.join_server(self.client_name, server_name, port)
        self.client_manager.wait_until_client_disconnects(self.client_name)

        return State.MENU
