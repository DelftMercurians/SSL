import numpy as np
from typing import Tuple
Vector2 = Tuple[float, float]

def get_relative_speed(pos1: Vector2, pos2: Vector2, speed1: Vector2, speed2: Vector2) -> Vector2:
    """Returns the magnitude of relative speed of pos1 to pos2."""
    d = (pos1[0] - pos2[0], pos1[1] - pos2[1])
    lend = np.sqrt(d[0]**2 + d[1]**2)
    d = (d[0]/lend, d[1]/lend)
    s = (speed1[0] - speed2[0], speed1[1] - speed2[1])
    return np.abs(d[0]*s[0] + d[1]*s[1])

def find_path(world, start_id: int, goal: Vector2, alpha = 0.00001, beta = 0.01, influence_factor = (5,1)) -> Vector2:
    """Computes the immediate direction the robot should head towards.
    Returns a unit vector, the global direction.
    """

    obstacles = []
    team_position = world.get_team_position()
    opp_position = world.get_opp_position()
    team_speed = world.get_team_speed()
    opp_speed = world.get_opp_speed()

    start_pos = team_position[start_id]
    for i, pos in enumerate(team_position):
        if i == start_id:
            continue
        obstacles.append((pos,get_relative_speed(pos,start_pos,team_speed[i],team_speed[start_id])))
    for i, pos in enumerate(opp_position):
        obstacles.append((pos,get_relative_speed(pos,start_pos,opp_speed[i],team_speed[start_id])))

    #print(obstacles)

    dist = np.sqrt((start_pos[0] - goal[0])**2 + (start_pos[1] - goal[1])**2)
    fx = (goal[0] - start_pos[0])/dist
    fy = (goal[1] - start_pos[1])/dist
    attractive_force = alpha * dist
    fx*=attractive_force
    fy*=attractive_force

    base_factor,speed_factor = influence_factor

    influence_radius = base_factor * GlobalConfig.RADIUS_ROBOT * 1000 #1000 -> convert the unit to mm

    #print(attractive_force)
    for (ox,oy),vel in obstacles:
        dx = start_pos[0] - ox
        dy = start_pos[1] - oy
        d = np.sqrt(dx**2 + dy**2)
        dx /= d
        dy /= d
        final_influence_radius = influence_radius + vel * speed_factor
        if d < final_influence_radius:
            repulsive_force = (1.0/(d-2*GlobalConfig.RADIUS_ROBOT*1000) - 1.0/(final_influence_radius-2*GlobalConfig.RADIUS_ROBOT*1000)) * (vel * beta + 1)
          #  print(repulsive_force)
     #       print(fx,repulsive_force * dx)
      #      print(fy,repulsive_force * dy)
            fx += repulsive_force * dx
            fy += repulsive_force * dy

    # normalize
    len = np.sqrt(fx**2 + fy**2)
    return (fx/len, fy/len)

