class EmailAlreadyExistsError(Exception):
    pass


class EmailNotFoundError(Exception):
    pass


class IncorrectPasswordError(Exception):
    pass


class InvalidTokenError(Exception):
    pass


class ExpiredTokenError(Exception):
    pass