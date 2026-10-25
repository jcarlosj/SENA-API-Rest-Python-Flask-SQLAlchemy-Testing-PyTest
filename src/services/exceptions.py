class AppError(Exception):
    # Excepción base del sistema
    def __init__(self, message, code=None, details=None):
        super().__init__(message)
        self.message = message
        self.code = code
        self.details = details or {}

class ValidationError(AppError):
    def __init__(self, message, code='VALIDATION_ERROR', details=None):
        super().__init__(message, code, details)

class ConflictError(AppError):
    def __init__(self, message, code='CONFLICT', details=None):
        super().__init__(message, code, details)

class DatabaseError(AppError):
    def __init__(self, message, code='DB_ERROR', details=None):
        super().__init__(message, code, details)

class NotFoundError(AppError):
    def __init__(self, message, code='NOT_FOUND', details=None):
        super().__init__(message, code, details)
