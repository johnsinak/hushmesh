from settings import *


class Message:
    ID_COUNTER = 0

    def __init__(self, author:int, step:int, is_misinformation:bool, is_owt=False, owt_recipient=-1) -> None:
        self.id = Message.ID_COUNTER
        Message.ID_COUNTER += 1
        self.author = author
        self.seen_by = {self.author: True}
        self.percentile_80 = False
        self.percentile_90 = False
        self.percentile_full = False
        self.created_at = step
        self.votes = {} # True for upvotes and False for downvotes
        self.ttl = MIN_TTL
        self.is_owt = is_owt
        self.owt_recipient = owt_recipient
        self.is_misinformation = is_misinformation
    
    def decrease_ttl(self):
        self.ttl -= 1

