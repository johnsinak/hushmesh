from loguru import logger
from random import random
from networkx import watts_strogatz_graph
from networkx.classes.graph import Graph

from Adversary import Adversary
from User import User


class MeshSim:
    def __init__(
        self,
        duration: int,
        number_of_users: int,
        world_dimension: tuple,
        move_range: tuple,
        message_exchange_range: tuple,
        adversary_ratio: float,
        ws_delta: int,
        ws_beta: float,
    ) -> None:
        self.duration = duration
        self.number_of_users = number_of_users
        self.world_dimension = world_dimension
        self.move_range = move_range
        self.message_exchange_range = message_exchange_range
        self.adversary_ratio = adversary_ratio
        self.ws_delta = ws_delta
        self.ws_beta = ws_beta
        self.users = {}

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
                self.users[i] = self._spawnAdversary(i)
            else:
                self.users[i] = self._spawnUser(i)

        graph = self._createSocialGraph()
        self._updateUsersBasedOnGraph(graph)

    def _spawnAdversary(self, id) -> User:
        return User(id, is_adversary=True)

    def _createSocialGraph(self) -> Graph:
        return watts_strogatz_graph(self.number_of_users, self.ws_delta, self.ws_beta)

    def _updateUsersBasedOnGraph(self, graph: Graph):
        # TODO: complete here based on prints in temp
        pass

    def _spawnUser(self, id) -> User:
        return User(id)

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
