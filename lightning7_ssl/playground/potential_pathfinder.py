import numpy as np
from dataclasses import dataclass


@dataclass
class descent_step:
    """Class for storing each step taken in gradient descent"""

    value: float
    x_index: float
    y_index: float


def get_kernel(origin: np.ndarray, step_size: int, length: int, width: int) -> np.ndarray:
    """
    Returns a kernel for the sliding window.
    """

    kernel = np.zeros((3, 3, 2))
    for i in range(3):
        for j in range(3):
            kernel[i, j] = [
                np.clip(origin[0] - step_size + j * step_size, 0, width - 1),
                np.clip(origin[1] - step_size + i * step_size, 0, length - 1),
            ]
    return np.array(kernel).astype(int)


def get_path(pmap: list[list[float]], starting_pos: list[float], goal: list[int]) -> np.ndarray:
    """
    Computes a path from starting position to goal position.
    """
    path = np.asarray([])
    map = np.asarray(pmap)
    curr_point = np.asarray([int(starting_pos[0]), int(starting_pos[1])])
    kernel = np.zeros((3, 3, 2))
    min_pot_point = np.zeros(2)
    check_point = np.zeros(2)
    k = 0

    while not np.allclose(check_point, goal):
        # get the neighboring points
        kernel = get_kernel(curr_point, 1, 90, 60)
        # print(kernel)
        neighbors = np.zeros((3, 3))

        for i in range(3):
            for j in range(3):
                neighbors[i, j] = map[kernel[i, j, 0], kernel[i, j, 1]]

        neighbors[1, 1] = np.infty

        min_pot = np.min(neighbors)
        min_pot_point = np.where(neighbors == min_pot)  # type: ignore

        curr_point = kernel[min_pot_point[0], min_pot_point[1]][0]

        step = descent_step(np.min(neighbors).astype(float), curr_point[0], curr_point[1])

        path = np.append(path, step)  # type: ignore

        check_point[0] = curr_point[1]
        check_point[1] = curr_point[0]

        k += 1

    return path
