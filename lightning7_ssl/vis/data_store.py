import json
from dataclasses import asdict, dataclass, field
from typing import Any, Callable, Dict, List

from lightning7_ssl import cfg

from ..vecMath.vec_math import Vec2, Vec3


@dataclass
class DataStore:
    state: Dict = field(
        default_factory=lambda: {
            "world": {},
            "player_states": [],
            "geom": {},
            "vector_field": None,
        }
    )
    _subs: List[Callable[[Dict, "DataStore"], Any]] = field(default_factory=list)

    def update_geom(self):
        """Updates the field geometry and lines for this frame."""
        if cfg.world.field_geometry is None or cfg.world.field_line_segments is None:
            return
        self.state["geom"] = {
            "field_geometry": asdict(cfg.world.field_geometry),
            "lines": [asdict(line) for line in cfg.world.field_line_segments],
            "arcs": [asdict(arc) for arc in cfg.world.field_circular_arcs],
        }
        self._publish(self.state)

    def update_player_and_ball_states(self):
        """Updates the states of own robots and ball for this frame."""
        ball_state = cfg.world.get_ball_state()
        own_players_state = cfg.world.get_team_state()
        opp_players_state = cfg.world.get_opp_state()
        if ball_state is None or own_players_state is None or opp_players_state is None:
            return

        self.state["world"] = {
            "ball": asdict(ball_state),
            "own_players": [asdict(p) for p in own_players_state],
            "opp_players": [asdict(p) for p in opp_players_state],
        }
        self._publish(self.state)

    def update_player_state(self, id: int, state: Dict):
        """Updates the state of a player for this frame."""
        self.state["player_states"][id] = state
        self._publish(self.state)

    def update_vector_field(self, vector_field: str):
        """Updates the vector field for this frame."""
        self.state["vector_field"] = vector_field
        self._publish(self.state)

    def subscribe(self, callback: Callable[[Dict, "DataStore"], Any]):
        """Subscribes to the state updates."""
        self._subs.append(callback)

    def to_json(self) -> str:
        """Converts the state to a JSON string."""
        json_str = json.dumps(
            self.state,
            default=lambda o: o.to_json() if isinstance(o, (Vec2, Vec3)) else o,
        )
        return json_str

    def _publish(self, update: Dict):
        for sub in self._subs:
            sub(update, self)
