from random import random, randint

from settings import *
from message import Message

class User:
    def __init__(self, id, location, world_dimension, is_adversary=False) -> None:
        self.id = id
        self.is_adversary = is_adversary
        self.contacts = []
        self.message_storage = []
        self.world_dimension = world_dimension
        self.location = location
    
    def extend_contacts(self, contact_list: list) -> None:
        self.contacts.extend(contact_list)

    def generate_message(self):
        if self.is_adversary:
            self.generate_adversary_message()
        elif random() < USER_MESSAGE_CREATION_RATE:
            self.generate_normal_message()

    def generate_adversary_message(self):
        self.message_storage.append(Message(self.id, is_misinformation=True))

    def generate_normal_message(self):
        self.message_storage.append(Message(self.id, is_misinformation=False))
    
    def move(self, move_range):
        # Random move value within move_range
        move_value = (randint(move_range[0][0], move_range[0][1]), randint(move_range[1][0], move_range[1][1]))
        print(f'move val: {move_value}')
        # This line bounds the new location to the boundries of the map
        self.location = (max(min(self.location[0] + move_value[0], self.world_dimension[0]), 0), max(min(self.location[1] + move_value[1], self.world_dimension[1]), 0))

    def act(self):
        if self.is_adversary:
            self._adversary_act()
        else:
            self._benign_act()
    
    def _adversary_act(self):
        # TODO:
        pass

    def _benign_act(self):
        # TODO: 
        pass
