from settings import *


class Message:
    ID_COUNTER = 0

    def __init__(self, author:str, is_misinformation:bool) -> None:
        self.id = Message.ID_COUNTER
        Message.ID_COUNTER += 1
        self.author = author
        self.votes = {}
        self.ttl = MIN_TTL
        self.is_misinformation = is_misinformation

