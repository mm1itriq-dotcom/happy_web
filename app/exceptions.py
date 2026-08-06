from flask import jsonify

class HappyWebError(Exception):
    """Base class for all custom Happy Web exceptions."""
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['error'] = self.message
        return rv

class ValidationError(HappyWebError):
    """Raised when user input fails validation (e.g., bad password format)."""
    def __init__(self, message):
        super().__init__(message, status_code=400)

class AuthenticationError(HappyWebError):
    """Raised when authentication fails (e.g., wrong password, bad token)."""
    def __init__(self, message):
        super().__init__(message, status_code=401)

class ResourceExistsError(HappyWebError):
    """Raised when trying to create a resource that already exists (e.g., duplicate email)."""
    def __init__(self, message):
        super().__init__(message, status_code=409)


def register_error_handlers(app):
    """Registers error handlers on the Flask app."""

    @app.errorhandler(HappyWebError)
    def handle_happy_web_error(error):
        # We don't necessarily need to log user-level errors like "bad password" to the error log,
        # but we can if we want. For now, we just return the JSON cleanly.
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response

    @app.errorhandler(Exception)
    def handle_unexpected_error(error):
        # Log unexpected 500 errors to the terminal (Flask logger)
        app.logger.error(f"Unexpected Error: {str(error)}", exc_info=True)
        return jsonify({"error": "An unexpected server error occurred."}), 500
