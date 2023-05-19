import random

import matplotlib.pyplot as plt
import numpy as np
from potential_world import calc_potential_field
from potential_pathfinder import get_path

from lightning7_ssl.vis.world_plotter import PotentialWorldPlotter

FIELD_LEN = 90
FIELD_WIDTH = 60
POT_RES = 1
APG = 2.5  # attractive potential gain
RPG = 100.0  # repulsive potential gain


def main():
    goal = [random.uniform(0, FIELD_WIDTH), random.uniform(0, FIELD_LEN)]
    start = [random.uniform(0, FIELD_WIDTH), random.uniform(0, FIELD_LEN)]

    obstacles = [[random.uniform(0, FIELD_LEN), random.uniform(0, FIELD_WIDTH)] for _ in range(10)]
    oy = [x[0] for x in obstacles]
    ox = [y[1] for y in obstacles]
    goal = [random.sample(range(FIELD_LEN), 1)[0], random.sample(range(FIELD_WIDTH), 1)[0]]
    robot_radius = 0.5
    s = 1

    pmap = calc_potential_field(goal[1], goal[0], ox, oy, POT_RES, robot_radius, FIELD_LEN, FIELD_WIDTH, s)
    PotWorld = PotentialWorldPlotter(APG, RPG, FIELD_LEN, FIELD_WIDTH, pmap)

    path = get_path(pmap, start, goal)
    waypoints = [[segment.x_index, segment.y_index] for segment in path]
    velocities = np.diff(waypoints, axis=0)
    print(velocities)

    PotWorld.darw_heatmap(starting_point=start, goal=goal)
    PotWorld.plot_path(path)  # type: ignore
    plt.show()


if __name__ == "__main__":
    main()
