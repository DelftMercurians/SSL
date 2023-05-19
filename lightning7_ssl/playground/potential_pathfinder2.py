import numpy as np


def get_kernel(origin: np.ndarray, step_size: int, length: int, width: int) -> np.ndarray:
    """
    Returns a kernel for the sliding window.
    """

    kernel = np.zeros((3, 3, 2))
    for i in range(3):
        for j in range(3):
            kernel[i, j] = [
                np.clip(origin[0] - step_size + j, 0, width - 1),
                np.clip(origin[1] - step_size + i, 0, length - 1),
            ]
        # print(kernel[i, j])
    return np.array(kernel).astype(int)


def get_path(pmap: list[list[float]], starting_pos: list[float], goal: list[int]) -> np.ndarray:
    """
    Computes a path from starting position to goal position.
    """
    path = np.asarray([])
    end = [int(goal[0]), int(goal[1])]
    map = np.asarray(pmap)
    curr_point = np.asarray([int(starting_pos[0]), int(starting_pos[1])])
    path = np.append(path, curr_point)
    k = 0
    while k < 50:
        # get the neighboring points
        kernel = get_kernel(curr_point, 1, 90, 60)
        neighbors = np.zeros((3, 3))

        for i in range(3):
            for j in range(3):
                neighbors[i, j] = map[kernel[i, j, 0], kernel[i, j, 1]]
        # print(neighbors)
        min_pot_point = np.argmin(neighbors, axis=0)[:2]

        curr_point = kernel[min_pot_point[0], min_pot_point[1]]
        path = np.append(path, [curr_point]).reshape(-1, 2)

        k += 1

    return path
