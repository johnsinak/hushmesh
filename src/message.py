from settings import *
import data_holder

class Message:
    ID_COUNTER = 0

    def __init__(self, author:int, step:int, is_misinformation:bool, is_owt=False, owt_recipient=-1) -> None:
        self.id = Message.ID_COUNTER
        Message.ID_COUNTER += 1
        self.author = author
        self.seen_by = {self.author: True}
        data_holder.message_seen_counter[self.id] = set()
        data_holder.message_seen_counter[self.id].add(self.author)
        self.percentile_80 = False
        self.percentile_90 = False
        self.percentile_full = False
        self.created_at = step
        self.received_at = -1
        self.votes = {} # True for upvotes and False for downvotes
        self.ttl = MIN_TTL
        self.is_owt = is_owt
        self.owt_recipient = owt_recipient
        self.is_misinformation = is_misinformation
    
    def decrease_ttl(self):
        self.ttl -= 1

