export interface XY {
  x: number;
  y: number;
}

export interface PosVel {
  position: XY;
  velocity: XY;
  orientation: number;
}

export interface World {
  ball: PosVel;
  own_players: PosVel[];
  opp_players: PosVel[];
}

export interface PlayerState {
  role: string;
  target: XY;
}

export interface Geometry {
  field_geometry: {
    /** The length of the field in meters. */
    field_length: number;
    /** The width of the field in meters. */
    field_width: number;
    goal_width: number;
    goal_depth: number;
    boundary_width: number;
    penalty_area_depth: number;
    penalty_area_width: number;
  };

  lines: {
    index: number;
    name: string;
    /** The start point of the line, in meters. */
    p1: XY;
    /** The end point of the line, in meters. */
    p2: XY;
    thickness: number;
  }[];

  arcs: {
    index: number;
    name: string;
    center: XY;
    radius: number;
    a1: number;
    a2: number;
    thickness: number;
  }[];
}

export interface ServerState {
  world?: World;
  player_states?: PlayerState[];
  geom?: Geometry;
}
