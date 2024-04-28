from ui.state_handler import StateHandler
from logs.logs import setup_logging
from ui.state import State
from db.models import Base
from db.db import engine


def main():
    setup_logging()
    Base.metadata.create_all(engine)

    state_handler = StateHandler()

    state_lookup = {
        State.AUTH: state_handler.auth_page,
        State.LOGIN: state_handler.login,
        State.REGISTER: state_handler.register,
        State.MENU: state_handler.menu,
        State.JOIN_SERVER: state_handler.join_server,
    }

    state = State.AUTH

    while state != State.QUIT:
        state = state_lookup[state]()

    print("Goodbye!")
    state_handler.close_all()


if __name__ == "__main__":
    main()
