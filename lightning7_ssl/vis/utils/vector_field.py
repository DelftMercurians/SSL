from typing import Callable, Tuple

import numpy as np

from lightning7_ssl.vecMath.vec_math import Vec2


def compute_vector_field(
    fun: Callable[[Vec2], Vec2], field_size: Tuple[float, float], grid_size: float
) -> np.ndarray:
    """Computes a vector field for a given function.

    Args:
        fun (Callable[[Vec2], Vec2]): The function to compute the vector field for.
        field_size (Tuple[float, float]): The size of the field in mm as (x, y).
        grid_size (float): The size of the grid in mm.

    Returns:
        np.ndarray: The vector field of shape (x, y, 2).
    """
    x = np.arange(-field_size[0] / 2, field_size[0] / 2 + grid_size, grid_size)
    y = np.arange(-field_size[1] / 2, field_size[1] / 2 + grid_size, grid_size)
    X, Y = np.meshgrid(x, y)
    points = np.stack((X, Y), axis=2)
    result = np.zeros_like(points)
    for i in range(len(points)):
        for j in range(len(points[i])):
            result[i, j] = fun(Vec2(points[i, j, 0], points[i, j, 1])).to_numpy()
    return result
