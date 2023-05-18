import numpy as np


"""
    Computes the potential field given the goal and obstacles.
"""

APG = 2.5  # attractive potential gain
RPG = 100.0  # repulsive potential gain
AREA_WIDTH = 2.0  # repulsive area width


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


def calc_potential_field(gx, gy, ox, oy, reso, rr, lth, w, s):
    # calc each potential
    pmap = [[0.0 for _ in range(lth)] for _ in range(w)]

    for ix in range(w):
        x = ix * reso

        for iy in range(lth):
            y = iy * reso
            ug = calc_attractive_potential(x, y, gx, gy)
            uo = calc_repulsive_potential(x, y, ox, oy, rr, s)
            uf = ug + uo
            pmap[ix][iy] = uf

    return pmap
