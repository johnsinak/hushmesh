from loguru import logger
from random import random, randint
from networkx import watts_strogatz_graph
from networkx.classes.graph import Graph
import matplotlib.pyplot as plt
from tqdm import tqdm
import datetime

from user import User
from message import Message
import data_holder


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
        for step in tqdm(range(self.duration)):
            self._step_forward(step)
        logger.info("simulation done. Plotting plots")

        self._plot()
        logger.info("plotting done. GG")

    def _initialize(self) -> None:
        for i in range(self.number_of_users):
            user_location = (randint(0, self.world_dimension[0]) - 1, randint(0, self.world_dimension[1] - 1))
            # Map to help with the exchange
            self.user_map[user_location[0]][user_location[1]].append(i)
            if random() < self.adversary_ratio:
                self.users[i] = self._spawn_user(i, user_location, self.world_dimension, is_adversary=True)
                data_holder.adversary_count += 1
            else:
                self.users[i] = self._spawn_user(i, user_location, self.world_dimension)

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

    def _step_forward(self, step) -> None:
        self._exchange_messages(step)
        self._generate_messages(step)
        self._users_act(step)
        self._users_move()
    
    def _exchange_messages(self, step) -> None:
        for x in range(self.world_dimension[0]):
            for y in range(self.world_dimension[1]):
                location = (x,y)
                self._exchange_messages_in_location(location, step)

    def _exchange_messages_in_location(self, location, step):
        aggregate_messages = {}
        user_ids_in_location = self.user_map[location[0]][location[1]]
        for id in user_ids_in_location:
            user = self.users[id]
            for message in user.message_storage:
                if message.ttl <= 0: continue
                if message.id not in aggregate_messages:
                    aggregate_messages[message.id] = message
                else:
                    old_mesasge = aggregate_messages[message.id]
                    for voter_id in message.votes.keys():
                        if voter_id not in old_mesasge.votes:
                            old_mesasge.votes[voter_id] = message.votes[voter_id]
                            data_holder.votes_exchanged_steps[step] += 1

        for id in user_ids_in_location:
            self.users[id].add_messages(list(aggregate_messages.values()), step)
    
    def _generate_messages(self, step) -> None:
        for i in range(self.number_of_users):
            self.users[i].generate_message(step)

    def _users_act(self, step) -> None:
        for id in range(self.number_of_users):
            if random() < self.user_act_probability:
                self.users[id].act(step)

    def _users_move(self) -> None:
        for i in range(self.number_of_users):
            old_location = self.users[i].location
            self.users[i].move(self.move_range)
            new_location = self.users[i].location
            if not (old_location[0] == new_location[0] and old_location[1] == new_location[1]):
                self.user_map[old_location[0]][old_location[1]].remove(i)
                self.user_map[new_location[0]][new_location[1]].append(i)

    def _plot(self) -> None:
        now = datetime.datetime.now()
        formatted_datetime = now.strftime("%Y-%m-%d_%H-%M-%S")
        contactlist_sizes = []
        message_storage_sizes = []
        for user_id in self.users:
            contactlist_sizes.append(len(self.users[user_id].contacts))
            message_storage_sizes.append(len(self.users[user_id].message_storage))
            
        # print()
        with open(f'results/results_{formatted_datetime}.txt', 'w') as f:
            txt_write_to_file = ''
            txt_write_to_file += f'===== test information =====\nusers: {self.number_of_users}   adversaries: {data_holder.adversary_count}\n'
            txt_write_to_file += f'total owts created: {data_holder.total_owt_created}    total owts responded to: {data_holder.total_owts_responded_to}\n'
            txt_write_to_file += f'total number of messages sent (mis or not): {Message.ID_COUNTER - data_holder.total_owt_created}\n'
            txt_write_to_file += f'average number of messages per step: {sum(data_holder.messages_exchanged_steps)/len(data_holder.messages_exchanged_steps)}\n'
            txt_write_to_file += f'average number of votes per step: {sum(data_holder.votes_exchanged_steps)/len(data_holder.votes_exchanged_steps)}\n'
            txt_write_to_file += f'average contact list sizes: {sum(contactlist_sizes)/len(contactlist_sizes)}\n'
            txt_write_to_file += f'average message storage sizes: {sum(message_storage_sizes)/len(message_storage_sizes)}\n'

            txt_write_to_file += f'===== average message propagation times (in steps) =====\n'
            txt_write_to_file += f'highest percentile reached: {data_holder.highest_percentile_reached_for_message}\n'
            if len(data_holder.message_propagation_times_80_percentile) == 0:
                txt_write_to_file += 'no message reached 80th. This is bad!\n'
            else:
                txt_write_to_file += f'80th: {sum(data_holder.message_propagation_times_80_percentile)/ len(data_holder.message_propagation_times_80_percentile)}     '
            if len(data_holder.message_propagation_times_90_percentile) == 0:
                txt_write_to_file += 'no message reached 90th. This is bad!\n'
            else:
                txt_write_to_file += f'90th: {sum(data_holder.message_propagation_times_90_percentile)/ len(data_holder.message_propagation_times_90_percentile)}     '
            if len(data_holder.message_propagation_times_full) == 0:
                txt_write_to_file += 'no message reached 100%. makes sense.\n'
            else:
                txt_write_to_file += f'full: {sum(data_holder.message_propagation_times_full)/ len(data_holder.message_propagation_times_full)}'
            txt_write_to_file += '\n'

            txt_write_to_file += '========= misinformation data =========\n'
            txt_write_to_file += f'total misinformation messages spread: {sum(data_holder.misinformation_count)}\n'
            txt_write_to_file += f'total upvotes on misinformation messages: {sum(data_holder.upvoted_misinformation_count)}\n'
            txt_write_to_file += f'total downvotes on misinformation messages: {sum(data_holder.downvoted_misinformation_count)}'

            print(txt_write_to_file)
            f.write(txt_write_to_file)
            
            # message_locations = []
            # user_locations = []
            # for user in self.users:
            #     user_locations.append(self.users[user].location)
            #     for message in self.users[user].message_storage:
            #         if message.id == 1:
            #             message_locations.append(self.users[user].location)
            
            # x_coords1, y_coords1 = zip(*message_locations)
            # x_coords2, y_coords2 = zip(*user_locations)

            # # Create a figure and axis
            # fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7))

            # # Plot the first set of points
            # ax1.scatter(x_coords1, y_coords1, color='blue')
            # ax1.set_xlim(0, 7)
            # ax1.set_ylim(0, 7)
            # ax1.set_xticks(range(8))
            # ax1.set_yticks(range(8))
            # ax1.grid(True)
            # ax1.set_xlabel('X-axis')
            # ax1.set_ylabel('Y-axis')
            # ax1.set_title('Scatter Plot 1')

            # # Plot the second set of points
            # ax2.scatter(x_coords2, y_coords2, color='red')
            # ax2.set_xlim(0, 7)
            # ax2.set_ylim(0, 7)
            # ax2.set_xticks(range(8))
            # ax2.set_yticks(range(8))
            # ax2.grid(True)
            # ax2.set_xlabel('X-axis')
            # ax2.set_ylabel('Y-axis')
            # ax2.set_title('Scatter Plot 2')

            # # Adjust layout to prevent overlap
            # plt.tight_layout()
            # plt.show()
            # # Set the limits of the plot to create a 7x7 grid
            

        with open(f'bulks/bulk_data_result_{formatted_datetime}.txt', 'w') as f:
            f.write(','.join(list(map(str, data_holder.misinformation_count))))
            f.write('\n')

            f.write(','.join(list(map(str, data_holder.upvoted_misinformation_count))))
            f.write('\n')

            f.write(','.join(list(map(str, data_holder.downvoted_misinformation_count))))
            f.write('\n')

            f.write(','.join(list(map(str, data_holder.messages_exchanged_steps))))
            f.write('\n')

            f.write(','.join(list(map(str, data_holder.votes_exchanged_steps))))
            f.write('\n')

            f.write(','.join(list(map(str, data_holder.message_propagation_times_80_percentile))))
            f.write('\n')

            f.write(','.join(list(map(str, data_holder.message_propagation_times_90_percentile))))
            f.write('\n')

            f.write(','.join(list(map(str, data_holder.message_propagation_times_full))))
            f.write('\n')




