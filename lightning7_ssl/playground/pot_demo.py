import matplotlib.pyplot as plt
import random
from potential_world import calc_potential_field
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

    PotWorld.darw_heatmap()
    PotWorld.draw_3d()
    plt.show()


if __name__ == "__main__":
    main()
