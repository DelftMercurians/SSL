import numpy as np
from numpy.lib.stride_tricks import as_strided
from dataclasses import dataclass


@dataclass
class descent_step:
    """Class for storing each step taken in gradient descent"""

    value: float
    x_index: float
    y_index: float


def sliding_window(pmap, window_size):
    """Construct a sliding window view of the pmap"""
    pmap = np.asarray(pmap)
    window_size = int(window_size)
    if pmap.ndim != 2:
        raise ValueError("need 2-D input")
    if not (window_size > 0):
        raise ValueError("need a positive window size")
    shape = (pmap.shape[0] - window_size + 1, pmap.shape[1] - window_size + 1, window_size, window_size)
    if shape[0] <= 0:
        shape = (1, shape[1], pmap.shape[0], shape[3])
    if shape[1] <= 0:
        shape = (shape[0], 1, shape[2], pmap.shape[1])
    strides = (pmap.shape[1] * pmap.itemsize, pmap.itemsize, pmap.shape[1] * pmap.itemsize, pmap.itemsize)

    return as_strided(pmap, shape=shape, strides=strides)


def cell_neighbours(pmap, i, j, d):
    """Return d-th neighbors of cell (i, j)"""
    w = sliding_window(pmap, 2 * d + 1)
    # print(w)

    ix = np.clip(i - d, 0, w.shape[0] - 1)
    jx = np.clip(j - d, 0, w.shape[1] - 1)

    i0 = max(0, i - d - ix)
    j0 = max(0, j - d - jx)
    i1 = w.shape[2] - max(0, d - i + ix)
    j1 = w.shape[3] - max(0, d - j + jx)
    print(i0, i1, j0, j1)
    return w[ix, jx][i0:i1, j0:j1].ravel()


def gradient_descent_3d(pmap, x_start, y_start, steps=50, step_size=1):
    # Initial point to start gradient descent at
    step = descent_step(pmap[y_start][x_start], x_start, y_start)
    next_step = 0

    # Store each step taken in gradient descent in a list
    step_history = []
    step_history.append(step)

    current_x = x_start
    current_y = y_start

    # Loop through specified number of steps of gradient descent to take
    for i in range(steps):
        # print(current_x, current_y)
        prev_x = current_x
        prev_y = current_y

        # Extract array of neighbouring cells around current step location with size nominated
        neighbours = cell_neighbours(pmap, current_y, current_x, step_size)

        # Locate minimum in array (steepest slope from current point)
        next_step = neighbours.min()
        # print(next_step)
        indices = np.where(pmap == next_step)
        # print(indices)
        # Update current point to now be the next point after stepping
        current_x, current_y = (indices[1][0], indices[0][0])
        step = descent_step(pmap[current_y][current_x], current_x, current_y)

        step_history.append(step)

        # If step is to the same location as previously, this infers convergence and end loop
        if prev_y == current_y and prev_x == current_x:
            print(f"Converged in {i} steps")
            break

    return next_step, step_history
