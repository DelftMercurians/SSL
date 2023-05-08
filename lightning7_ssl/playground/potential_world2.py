import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider  # type: ignore
import random

FIELD_LEN = 90
FIELD_WIDTH = 60
POT_RES = 1

APG = 2.5  # attractive potential gain
RPG = 100.0  # repulsive potential gain
AREA_WIDTH = 2.0  # repulsive area width

goal = [random.uniform(0, FIELD_LEN), random.uniform(0, FIELD_LEN)]

show_animation = True


def calc_attractive_potential(x, y, gx, gy):
    return 0.5 * APG * np.hypot(x - gx, y - gy)


def calc_repulsive_potential(x, y, ox, oy, rr, s):
    # search nearest obstacle
    minid = -1
    dmin = float("inf")
    for i in range(len(ox)):
        d = np.hypot(x - ox[i], y - oy[i])
        if dmin >= d:
            dmin = d
            minid = i

    # calc repulsive potential
    dq = np.hypot(x - ox[minid], y - oy[minid])

    if dq <= rr+s:
        dq = 0.5

        return 0.5 * RPG * (1.0 / dq) ** 2
    else:
        return 0.0


def calc_potential_field(gx, gy, ox, oy, reso, rr, l, w, s):
    minx = min(ox) - AREA_WIDTH / 2.0
    miny = min(oy) - AREA_WIDTH / 2.0
    # maxx = max(ox) + AREA_WIDTH / 2.0
    # maxy = max(oy) + AREA_WIDTH / 2.0

    xw = w
    yw = l

    # calc each potential
    pmap = [[0.0 for i in range(yw)] for i in range(xw)]

    for ix in range(xw):
        x = ix * reso

        for iy in range(yw):
            y = iy * reso
            ug = calc_attractive_potential(x, y, gx, gy)
            uo = calc_repulsive_potential(x, y, ox, oy, rr, s)
            uf = ug + uo
            pmap[ix][iy] = uf

    return pmap, minx, miny


fig_heat, ax_heat = plt.subplots()


def draw_heatmap(data):
    data = np.array(data).T
    ax_heat.pcolor(data, vmax=100.0, cmap=plt.cm.Blues)  # type: ignore


def main():
    # start_pos = [random.uniform(0, FIELD_LEN), random.uniform(0, FIELD_WIDTH)]
    obstacles = [[random.uniform(0, FIELD_LEN), random.uniform(0, FIELD_WIDTH)] for _ in range(10)]
    oy = [x[0] for x in obstacles]
    ox = [y[1] for y in obstacles]
    goal = [random.sample(range(FIELD_LEN), 1)[0], random.sample(range(FIELD_WIDTH), 1)[0]]
    robot_radius = 0.5
    s = 1

    pmap, minx, miny = calc_potential_field(goal[1], goal[0], ox, oy, POT_RES, robot_radius, FIELD_LEN, FIELD_WIDTH, s)

    draw_heatmap(pmap)

    def heatmap_update(val):
        global RPG
        global APG
        RPG = rpg_slider.val
        APG = apg_slider.val
        pmap, minx, miny = calc_potential_field(goal[1], goal[0], ox, oy, POT_RES, robot_radius, FIELD_LEN, FIELD_WIDTH, s)
        draw_heatmap(pmap)
        fig_heat.canvas.draw_idle()

    axrpg = fig_heat.add_axes([0.25, 0.01, 0.65, 0.03])
    rpg_slider = Slider(
        ax=axrpg,
        label='RPG',
        valmin=0.0,
        valmax=500.0,
        valinit=100,
    )

    axapg = fig_heat.add_axes([0.25, 0.05, 0.65, 0.03])
    apg_slider = Slider(
        ax=axapg,
        label='APG',
        valmin=0.0,
        valmax=10.0,
        valinit=APG,
    )

    rpg_slider.on_changed(heatmap_update)
    apg_slider.on_changed(heatmap_update)
    # plt.scatter(goal[1], goal[0], s = 10, c = 'g')
    # plt.scatter(ox, oy, s = 10, c = 'r')
    X, Y = np.meshgrid(range(FIELD_LEN), range(FIELD_WIDTH))
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    ax.plot_wireframe(Y, X, np.clip(pmap, min(pmap), 100), color='blue')  # type: ignore

    def pot_update(val):
        global RPG
        global APG
        RPG = rpg_slider_3D.val
        APG = apg_slider_3D.val
        ax.clear()
        pmap, minx, miny = calc_potential_field(goal[1], goal[0], ox, oy, POT_RES, robot_radius, FIELD_LEN, FIELD_WIDTH, s)
        ax.plot_wireframe(Y, X, np.clip(pmap, min(pmap), 100), color='blue')  # type: ignore
        fig.canvas.draw_idle()

    axrpg_3D = fig.add_axes([0.25, 0.01, 0.65, 0.03])
    rpg_slider_3D = Slider(
        ax=axrpg_3D,
        label='RPG',
        valmin=0.0,
        valmax=500.0,
        valinit=100,
    )

    axapg_3D = fig.add_axes([0.25, 0.05, 0.65, 0.03])
    apg_slider_3D = Slider(
        ax=axapg_3D,
        label='APG',
        valmin=0.0,
        valmax=10.0,
        valinit=APG,
    )

    rpg_slider_3D.on_changed(pot_update)
    apg_slider_3D.on_changed(pot_update)

    plt.show()


if __name__ == '__main__':
    main()
