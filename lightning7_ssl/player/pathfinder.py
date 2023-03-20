from typing import List, Tuple
from ..vecMath.vec_math import Vec2
from ..world.maintainer import World


RADIUS_ROBOT = 0.0793


def get_relative_speed(pos1: Vec2, pos2: Vec2, vel1: Vec2, vel2: Vec2) -> float:
    """
        get the relative speed of two objects based on the position and speed of them.

        Args:
            pos1:  position of the first object
            pos2:  position of the second object
            speed1:  speed of the first object
            speed2:  speed of the second object

        Returns: a scalar, the relative speed which can represents how fast they are approaching each other.
    """
    d = (pos1 - pos2).as_unit()
    s = vel1 - vel2
    return abs(d.dot(s))


def find_path(
    world: World,
    start_id: int,
    goal: Vec2,
    alpha=0.00001,
    beta=0.01,
    influence_factor: Tuple[int, int] = (5, 1),
) -> Vec2:
    """
        Computes the immediate direction the robot should head towards.
        Returns a unit vector, the global direction.
        
        Args:
            world: the world object which contains the current state
            start_id: the id of the robot which is going to move
            goal:  the position of the ball
            alpha: larger alpha will lead to a stronger attractive rate(related to the repulsive rate)
            beta: the relative speed contribution to the repulsive force(compared to no speed)
            influence_factor: = base_factor,speed_factor,
        
                base_factor: in what range the obstacle can have an influence.
                speed_factor: the relative speed contribution to the enlarged radius(compared to no speed)

        Returns: a unit vector, the global direction.
    """

    obstacles: List[Tuple[Vec2, float]] = []
    team_position = world.get_team_position()
    opp_position = world.get_opp_position()
    team_vel = world.get_team_vel()
    opp_vel = world.get_opp_vel()

    start_pos = team_position[start_id]
    for i, pos in enumerate(team_position):
        # Convert everything to Vec2
        if i == start_id:
            continue
        obstacles.append(
            (
                pos,
                get_relative_speed(pos, start_pos, team_vel[i], team_vel[start_id]),
            )
        )

    for i, pos in enumerate(opp_position):
        obstacles.append(
            (
                pos,
                get_relative_speed(pos, start_pos, opp_vel[i], team_vel[start_id]),
            )
        )

    f = (goal - start_pos).as_unit()
    dist = f.norm
    attractive_force = alpha * dist
    f *= attractive_force

    base_factor, speed_factor = influence_factor

    influence_radius = (
        base_factor * RADIUS_ROBOT * 1000
    )  # 1000 -> convert the unit to mm

    for o, speed in obstacles:
        d = (start_pos - o).norm
        final_influence_radius = influence_radius + speed * speed_factor
        if d < final_influence_radius:
            repulsive_force = (
                1.0 / (d - 2 * RADIUS_ROBOT * 1000)
                - 1.0 / (final_influence_radius - 2 * RADIUS_ROBOT * 1000)
            ) * (speed * beta + 1)
            f += (start_pos - o).as_unit() * repulsive_force

    # normalize
    return f.as_unit()
