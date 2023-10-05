

class UserExeption(Exception):
    def __init__(self, name: str, status_code: int):
        self.name = name
        self.status_code = status_code