import json
import numpy as np
from dataclasses import dataclass, field, asdict
from typing import Any, Dict, Callable, List, Optional
from ..world import World


@dataclass
class DataStore:
    state: Dict = field(default_factory=lambda: {"world": {}, "player_states": {}})
    _subs: List[Callable[[Dict, "DataStore"], Any]] = field(default_factory=list)

    def update_world_state(self, world: World):
        update = asdict(world)
        self.state["world"] = update
        self._publish(update)

    def update_player_state(
        self, id: int, status: str, target: Optional[str], role: Optional[str]
    ):
        update = {
            "status": status,
            "target": target,
            "role": role,
        }
        self.state["player_states"][id] = update
        self._publish(update)

    def subscribe(self, callback: Callable[[Dict], Any]):
        self._subs.append(callback)

    def to_json(self) -> str:
        """Converts the state to a JSON string."""
        json_str = json.dumps(
            self.state,
            default=lambda o: o.tolist() if isinstance(o, np.ndarray) else o,
        )
        return json_str

    def _publish(self, update: Dict):
        for sub in self._subs:
            sub(update, self)
