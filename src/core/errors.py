class NotFoundErr(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class ConflictErr(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class InvalidValueErr(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class AuthErr(Exception):
    def __init__(self, message: str = "Authentication error"):
        self.message = message
        super().__init__(self.message)


class InvalidTokenErr(Exception):
    def __init__(self, message: str = "Invalid token"):
        self.message = message
        super().__init__(self.message)


class PermissionErr(Exception):
    def __init__(self, message: str = "Permission denied"):
        self.message = message
        super().__init__(self.message)
