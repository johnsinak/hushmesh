from loguru import logger
from random import random

from Adversary import Adversary
from User import User


class MeshSim:
    def __init__(self, duration: int, number_of_users: int, world_dimension: tuple, move_range: tuple, message_exchange_range: tuple, adversary_ratio: float) -> None:
        self.duration = duration
        self.number_of_users = number_of_users
        self.world_dimension = world_dimension
        self.move_range = move_range
        self.message_exchange_range = message_exchange_range
        self.adversary_ratio = adversary_ratio
        self.users = []

    def run(self) -> None:
        logger.info("initializing...")
        self._initialize()

        logger.info("starting simualtion")
        for step in range(self.duration):
            self._stepForward()
        logger.info("simulation done. Plotting plots")

        self._plot()

    
    def _initialize(self) -> None:
        for i in range(self.number_of_users):
            if random() < self.adversary_ratio:
                self.users.append(self._spawnAdversary())
            else: 
                self.users.append(self._spawnUser())
        
        # TODO: create social graph

    def _spawnAdversary(self) -> Adversary:
        return Adversary()
    
    def _spawnUser(self) -> User:
        return User()

    def _stepForward(self) -> None:
        self._exchangeMessages()
        self._generateMessages()
        self._usersAct()
        self._usersMove()

    def _generateMessages(self) -> None:
        # TODO
        pass

    def _exchangeMessages(self) -> None:
        # TODO
        pass

    def _usersAct(self) -> None:
        # TODO
        pass

    def _usersMove(self) -> None:
        # TODO
        pass

    def _plot(self) -> None:
        # TODO
        pass