from MeshSim import MeshSim
from settings import *

if __name__ == "__main__":
    sim = MeshSim(T, N, WORLD_DIMENSION, MOVE_RANGE, MESSAGE_EXCHANGE_RANGE)
    sim.run()