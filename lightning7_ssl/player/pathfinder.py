import numpy as np
from typing import Tuple
from lightning7_ssl.config import GlobalConfig
Vector2 = Tuple[float, float]

def find_path(start: int, goal: Vector2, alpha = 1, influence_factor = 8) -> Vector2:
    """Computes the immediate direction the robot should head towards.
    Returns a unit vector, the global direction.
    """

    obstacles = []
    idx = 0
    for robot_pos in GlobalConfig.world.get_team_position():
        if idx != start:
            obstacles.append(robot_pos)
        else:
            start_pos = robot_pos
        idx += 1
  #  print(start_pos)
    obstacles.extend(GlobalConfig.world.get_opp_position())
    dist = np.sqrt((start_pos[0] - goal[0])**2 + (start_pos[1] - goal[1])**2)
    fx = alpha * (goal[0] - start_pos[0])/dist
    fy = alpha * (goal[1] - start_pos[1])/dist
    attractive_force = alpha * dist**2
    fx*=attractive_force
    fy*=attractive_force


    influence_radius = influence_factor * GlobalConfig.RADIUS_ROBOT * 100
    for ox,oy in obstacles:
        dx = start_pos[0] - ox
        dy = start_pos[1] - oy
        d = np.sqrt(dx**2 + dy**2)
        dx /= d
        dy /= d

        if d < influence_radius:
            repulsive_force = (1.0/d - 1.0/influence_radius)**2
            fx += repulsive_force * dx
            fy += repulsive_force * dy

    # normalize
    len = np.sqrt(fx**2 + fy**2)
    return (fx/len, fy/len)

