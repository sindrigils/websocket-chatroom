from enum import Enum


class State(Enum):
    AUTH = 1
    LOGIN = 2
    REGISTER = 3
    MENU = 4
    JOIN_SERVER = 5
    QUIT = 99
