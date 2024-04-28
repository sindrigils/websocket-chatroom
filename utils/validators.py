def validate_username(username: str) -> bool:
    return (
        bool(username)
        and len(username) > 3
        and any(char.isalpha() for char in username)
    )


def validate_password(password: str) -> bool:
    return len(password) > 3


if __name__ == "__main__":
    pass
