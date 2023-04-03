import json
from collections import defaultdict
from dataclasses import asdict, dataclass, field
from typing import Any, Callable, Dict, List, Set, Tuple

from lightning7_ssl import cfg
from lightning7_ssl.player.player import Player, Status

from ..vecMath.vec_math import Vec2, Vec3


@dataclass
class DataStore:
    state: Dict = field(default_factory=defaultdict)

    _active_keys: Set[Tuple[str, ...]] = field(
        default_factory=lambda: set([("world", "player_states", "geom")])
    )
    _subs: List[Callable[[Dict, "DataStore"], Any]] = field(default_factory=list)

    def update(self, obj_id: str, value: Any):
        """Updates the state"""
        if obj_id in self._active_keys:
            self.state[obj_id] = value
            self._publish(self.state)

    def set_key_active(self, key: str, active: bool):
        """Activates or deactivates a key."""
        if isinstance(key, str):
            key = (key,)
        if len(key) not in (1, 2, 3):
            raise ValueError("Key must be of length 1, 2 or 3.")
        if active:
            self._active_keys.add(key)
        else:
            self._active_keys.remove(key)

    def update_geom(self):
        """Updates the field geometry and lines for this frame."""
        if cfg.world.field_geometry is None or cfg.world.field_line_segments is None:
            return
        self.update(
            "geom",
            {
                "field_geometry": asdict(cfg.world.field_geometry),
                "lines": [asdict(line) for line in cfg.world.field_line_segments],
                "arcs": [asdict(arc) for arc in cfg.world.field_circular_arcs],
            },
        )

    def update_player_and_ball_states(self):
        """Updates the states of own robots and ball for this frame."""
        ball_state = cfg.world.get_ball_state()
        own_players_state = cfg.world.get_team_state()
        opp_players_state = cfg.world.get_opp_state()
        if ball_state is None or own_players_state is None or opp_players_state is None:
            return
        self.update(
            "world",
            {
                "ball": asdict(ball_state),
                "own_players": [asdict(p) for p in own_players_state],
                "opp_players": [asdict(p) for p in opp_players_state],
            },
        )

    def update_player_state(self, player: Player):
        """Updates the state of a player."""
        player_id = player.id
        state = {
            "status": Status.to_json(player.status),
        }
        self.update("player_states", {str(player_id): state}, overwrite=False)

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
