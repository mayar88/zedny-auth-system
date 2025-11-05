class PermissionDenied(Exception):
    def __init__(self, message="Permission denied",role=None, action=None, resource=None):
        self.message = message
        self.role = role
        self.action = action
        self.resource = resource
        super().__init__(self.message)

class AuthenticationFailed(Exception):
    pass

class ResourceNotFound(Exception):
    pass

class InvalidOperation(Exception):
    pass

class DatabaseError(Exception):
    pass

class NotFoundException(Exception):
    pass
