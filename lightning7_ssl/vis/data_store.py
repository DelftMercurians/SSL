import json
from dataclasses import dataclass, field, asdict
from typing import Any, Dict, Callable, List, Optional
from ..vecMath.vec_math import Vec2, Vec3
from ..world.maintainer import World
from ..world.maintainer import FilteredDataWrapper


@dataclass
class DataStore:
    state: Dict = field(
        default_factory=lambda: {"world": {}, "friends": {}, "opps": {}, "ball": {}}
    )
    _subs: List[Callable[[Dict, "DataStore"], Any]] = field(default_factory=list)

    # def update_world_state(self, world: World):
    #     update = asdict(world.get_status())
    #     self.state["world"] = update
    #     self._publish(self.state)

    def update_player_and_ball_states(self, data: FilteredDataWrapper):
        """
        Updates the states of own robots and ball for this frame.

        friends: own robots
        opps: opponent robots
        """
        update = asdict(data)
        self.state["friends"] = update["own_robots_status"]
        self.state["opps"] = update["opp_robots_status"]
        self.state["ball"] = update["ball_status"]
        self._publish(self.state)

    def subscribe(self, callback: Callable[[Dict], Any]):
        self._subs.append(callback)

    def to_json(self) -> str:
        """Converts the state to a JSON string."""
        json_str = json.dumps(
            self.state,
            default=lambda o: o.vec if isinstance(o, (Vec2, Vec3)) else o,
        )
        return json_str

    def _publish(self, update: Dict):
        for sub in self._subs:
            sub(update, self)
