class IcExcepcion(Exception):
    def __init__(self, message: str, code: int = 500):
        self.message = message
        self.code = code