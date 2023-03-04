export interface XY {
  x: number;
  y: number;
}

export interface PosVel {
  pos: XY;
  vel: XY;
}

export interface World {
  ball: PosVel;
  own_players: PosVel[];
  opp_players: PosVel[];
  field_dimensions: XY;
}

export interface PlayerState {
  role: string;
  target: XY;
}

export interface ServerState {
  world: World;
  player_states: PlayerState[];
}
