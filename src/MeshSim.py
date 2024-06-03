from loguru import logger
from random import random, randint
from networkx import watts_strogatz_graph
from networkx.classes.graph import Graph
import matplotlib.pyplot as plt
import networkx

from user import User


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
        user_act_probability: float
    ) -> None:
        self.duration = duration
        self.number_of_users = number_of_users
        self.world_dimension = world_dimension
        self.move_range = move_range
        self.message_exchange_range = message_exchange_range
        self.adversary_ratio = adversary_ratio
        self.ws_delta = ws_delta
        self.ws_beta = ws_beta
        self.user_act_probability = user_act_probability
        self.users = {}
        self.user_map = [[list() for _ in range(world_dimension[1])] for _ in range(world_dimension[0])]

    def run(self) -> None:
        logger.info("initializing...")
        self._initialize()

        logger.info("starting simualtion")
        for step in range(self.duration):
            self._step_forward()
        logger.info("simulation done. Plotting plots")

        self._plot()

    def _initialize(self) -> None:
        for i in range(self.number_of_users):
            user_location = (randint(0, self.world_dimension[0]) - 1, randint(0, self.world_dimension[1] - 1))
            # Map to help with the exchange
            self.user_map[user_location[0]][user_location[1]].append(i)
            if random() < self.adversary_ratio:
                self.users[i] = self._spawn_user(i, user_location, is_adversary=True)
            else:
                self.users[i] = self._spawn_user(i, user_location)

        graph = self._create_social_graph()
        self._update_users_based_on_graph(graph)

    def _spawn_user(self, id: int, user_location: tuple, world_dimension:tuple, is_adversary=False) -> User:
        return User(id, user_location, world_dimension, is_adversary)

    def _create_social_graph(self) -> Graph:
        return watts_strogatz_graph(self.number_of_users, self.ws_delta, self.ws_beta)

    def _update_users_based_on_graph(self, graph: Graph):
        for i in range(self.number_of_users):
            contacts = list(graph[i].keys())
            self.users[i].extend_contacts(contacts)

    def _step_forward(self) -> None:
        self._exchange_messages()
        self._generate_messages()
        self._users_act()
        self._users_move()
    
    def _exchange_messages(self) -> None:
        for x in range(self.world_dimension[0]):
            for y in range(self.world_dimension[1]):
                location = (x,y)
                self._exchange_messages_in_location(location)

    def _exchange_messages_in_location(self, location):
        aggregate_messages = {}
        user_ids_in_location = self.user_map[location[0], location[1]]
        for id in user_ids_in_location:
            user = self.users[id]
            for message in user.message_storage:
                if not aggregate_messages.get(message.id, None):
                    aggregate_messages[message.id] = message
                else:
                    old_mesasge = aggregate_messages[message.id]
                    for voter_id in message.votes.keys():
                        old_mesasge.votes[voter_id] = message.votes[voter_id]
        
        for id in user_ids_in_location:
            self.users[id].message_storage = list(aggregate_messages.values())
    
    def _generate_messages(self) -> None:
        for i in range(self.number_of_users):
            self.users[i].generate_message()

    def _users_act(self) -> None:
        for id in range(self.number_of_users):
            if random() < self.user_act_probability:
                self.users[id].act()

    def _users_move(self) -> None:
        for i in range(self.number_of_users):
            old_location = self.users[i].location
            self.users[i].move(self.move_range)
            new_location = self.users[i].location
            if not (old_location[0] == new_location[0] and old_location[1] == new_location[1]):
                self.user_map[old_location[0]][old_location[1]].remove(i)
                self.user_map[new_location[0]][new_location[1]].append(i)

    def _plot(self) -> None:
        # TODO
        pass
