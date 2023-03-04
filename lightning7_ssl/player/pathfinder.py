import numpy as np
from lightning7_ssl.config import GlobalConfig


def find_path(start: int, goal: np.ndarray) -> np.ndarray:
    """Computes the immediate direction the robot should head towards.
    Returns a unit vector.
    """
    # TODO: Actual implementation
    world = GlobalConfig.world

    dir = end - start
    return dir / np.linalg.norm(dir)
