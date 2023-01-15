import numpy as np


def find_path(start: np.ndarray, end: np.ndarray) -> np.ndarray:
    """Computes the immediate direction the robot should head towards.

    Returns a unit vector.
    """
    # TODO: Actual implementation
    dir = end - start
    return dir / np.linalg.norm(dir)
