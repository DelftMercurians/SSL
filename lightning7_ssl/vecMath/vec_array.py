import numpy as np

from lightning7_ssl.vecMath.vec_math import Vec2


class Vec2Array:
    """Class for working with arrays of 2D vectors while providing the same interface as
    Vec2, powered by numpy."""

    def __init__(self, array: np.ndarray) -> None:
        self.x = array[:, 0]
        self.y = array[:, 1]
        self._arr = array

    @property
    def norm(self):
        """Norm (euclidian length) of the vector."""
        return np.sqrt(self.x**2 + self.y**2)

    # Probably useless
    # def __str__(self) -> str:
    #     return f"({self.x}, {self.y})"

    # def __repr__(self) -> str:
    #     return f"Vec2({self.x}, {self.y})"

    def __add__(self, other: "Vec2Array | Vec2") -> "Vec2Array":
        if isinstance(other, Vec2):
            return Vec2Array(self._arr + np.array([other.x, other.y]))
        if not isinstance(other, Vec2Array):
            return NotImplemented
        return Vec2Array(self._arr + other._arr)

    def __sub__(self, other: "Vec2Array | Vec2") -> "Vec2Array":
        if isinstance(other, Vec2):
            return Vec2Array(self._arr - np.array([other.x, other.y]))
        if not isinstance(other, Vec2Array):
            return NotImplemented
        return Vec2Array(self._arr - other._arr)

    def __rsub__(self, other: "Vec2Array | Vec2") -> "Vec2Array":
        if isinstance(other, Vec2):
            return Vec2Array(np.array([other.x, other.y]) - self._arr)
        if not isinstance(other, Vec2Array):
            return NotImplemented
        return Vec2Array(other._arr - self._arr)

    def __mul__(self, scalar: float) -> "Vec2Array":
        return Vec2Array(self._arr * scalar)

    def __truediv__(self, scalar: float) -> "Vec2Array":
        return Vec2Array(self._arr / scalar)

    def __floordiv__(self, scalar: float) -> "Vec2Array":
        return Vec2Array(self._arr // scalar)

    def __divmod__(self, scalar: float) -> "Vec2Array":
        return Vec2Array(self._arr % scalar)

    def __len__(self) -> int:
        return len(self._arr)

    def __getitem__(self, index: int) -> Vec2:
        return Vec2(self._arr[index, 0], self._arr[index, 1])

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Vec2Array):
            return NotImplemented
        return np.array_equal(self._arr, other._arr)

    def dot(self, other: "Vec2Array | Vec2"):
        """
        Returns the dot product of all vectors in this array with the corresponding
        vector in the other array.
        """
        if not isinstance(other, (Vec2Array, Vec2)):
            raise TypeError("other must be a Vec2Array or Vec2")
        return self.x * other.x + self.y * other.y

    def as_unit(self):
        """
        Returns the unit vector of all vectors in this array.
        """
        return self / self.norm

    def to_json(self):
        """
        Returns a json representation of this Vec2 object.
        """
        return self._arr.tolist()
