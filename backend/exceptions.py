class UserNotFoundError(Exception):
    pass

class InvalidPasswordError(Exception):
    pass

class SessionExpiredError(Exception):
    pass

class SessionRevokedError(Exception):
    pass

class UserIDNotFound(Exception):
    pass