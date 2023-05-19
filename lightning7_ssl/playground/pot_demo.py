import random

import matplotlib.pyplot as plt
import numpy as np
from potential_pathfinder import gradient_descent_3d
from potential_world import calc_potential_field
from potential_pathfinder2 import get_path

from lightning7_ssl.vis.world_plotter import PotentialWorldPlotter

FIELD_LEN = 90
FIELD_WIDTH = 60
POT_RES = 1
APG = 2.5  # attractive potential gain
RPG = 100.0  # repulsive potential gain

goal = [random.uniform(0, FIELD_LEN), random.uniform(0, FIELD_LEN)]


def main():
    obstacles = [[random.uniform(0, FIELD_LEN), random.uniform(0, FIELD_WIDTH)] for _ in range(10)]
    oy = [x[0] for x in obstacles]
    ox = [y[1] for y in obstacles]
    goal = [random.sample(range(FIELD_LEN), 1)[0], random.sample(range(FIELD_WIDTH), 1)[0]]
    robot_radius = 0.5
    s = 1

    pmap = calc_potential_field(goal[1], goal[0], ox, oy, POT_RES, robot_radius, FIELD_LEN, FIELD_WIDTH, s)
    PotWorld = PotentialWorldPlotter(APG, RPG, FIELD_LEN, FIELD_WIDTH, pmap)

    path = get_path(pmap, [1.0, 1.0], goal)
    print(path)

    PotWorld.darw_heatmap(starting_point=[1.0, 1.0], goal=goal)
    # plt.show()

    # map = np.asarray(pmap)
    # global_minimum = map.min()
    # indices = np.where(map == global_minimum)
    # print(f"Target: {global_minimum} @ {indices}")

    # step_size = 1
    # found_minimum = 9999

    # print(f"Optimal step size {step_size}")

    # while found_minimum != global_minimum:
    #     step_size += 1
    #     found_minimum, steps = gradient_descent_3d(map, 1, 1, steps=1000, step_size=step_size)

    # found_minimum, steps = gradient_descent_3d(map, 1, 1, steps=1000, step_size=step_size)
    # print(steps)
    # PotWorld.plot_path(steps)
    # plt.show()
    # print(f"Steps: {steps}")
    # PotWorld.draw_3d()
    # plt.show()


if __name__ == "__main__":
    main()
