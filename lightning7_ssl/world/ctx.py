from dataclasses import dataclass

from lightning7_ssl.vecMath.vec_math import Vec2

from .frame import Frame


@dataclass
class WorldCtx:
    frames: list[Frame]

    @property
    def last_frame(self) -> Frame:
        return self.frames[-1]

    def closest_player(self, pos: Vec2) -> int:
        """Finds the closest player to the given position."""
        frame = self.last_frame
        return min(
            range(len(frame.own_players)),
            key=lambda id: (frame.own_players[id].position - pos).norm,
        )
