from dataclasses import dataclass

from ..vecMath.vec_math import Vec2


@dataclass
class FieldLinesSegment:
    """
    A single field line segment.

    @params:
        p1: Start point of segment
        p2: End point of segment
    """

    index: int
    name: str
    p1: Vec2
    p2: Vec2
    thickness: float


@dataclass
class FieldCircularArc:
    """
    A class to store a single field arc.

    @params:
        a1: Start angle in counter-clockwise order.
        a2: End angle in counter-clockwise order.
    """

    index: int
    name: str
    center: Vec2
    radius: float
    a1: float
    a2: float
    thickness: float


@dataclass
class FieldGeometry:
    """
    A dataclass to store field geometry data from ssl vision.
    """

    # Excluded field line segments, arcs, and penalty area for now, can be added later
    field_length: int
    field_width: int
    goal_width: int
    goal_depth: int
    boundary_width: int
    penalty_area_depth: int
    penalty_area_width: int
