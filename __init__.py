class HikBaseException(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status = status_code
