import math

"""
    Vec2 and Vec3 classes for arithmetic operations between 2- and 3-element vectors.
"""


class Vec2:
    """
    Class for vectors of length 2.
    """

    def __init__(self, x: float = 0, y: float = 0) -> None:
        """
        Vec2 contains (x, y) coordinates and its own norm.
        """
        if not isinstance(x, (int, float)) or not isinstance(y, (int, float)):
            raise TypeError("Vec2 coordinates must be numbers.")
        self.x = x
        self.y = y
        self.vec = (x, y)

    @property
    def norm(self):
        """Norm (euclidian length) of the vector."""
        return math.sqrt(self.x**2 + self.y**2)

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"

    def __repr__(self) -> str:
        return f"Vec2({self.x}, {self.y})"

    def __add__(self, other: "Vec2") -> "Vec2":
        """
        Returns the sum of two Vec2 objects.
        """
        if not isinstance(other, Vec2):
            return NotImplemented
        x = self.x + other.x
        y = self.y + other.y
        return Vec2(x, y)

    def __sub__(self, other: "Vec2") -> "Vec2":
        """
        Returns the difference of two Vec2 objects.
        """
        if not isinstance(other, Vec2):
            return NotImplemented
        x = self.x - other.x
        y = self.y - other.y
        return Vec2(x, y)

    def __mul__(self, scalar: float) -> "Vec2":
        """
        Scalar multiplication of a Vec2 object.
        """
        return Vec2(self.x * scalar, self.y * scalar)

    def __truediv__(self, scalar: float) -> "Vec2":
        """
        Scalar division of a Vec2 object.
        """
        return Vec2(self.x / scalar, self.y / scalar)

    def __floordiv__(self, scalar: float) -> "Vec2":
        """
        Scalar floor division of a Vec2 object.
        """
        return Vec2(self.x // scalar, self.y // scalar)

    def __divmod__(self, scalar: float) -> "Vec2":
        """
        Scalar division of a Vec2 object.
        """
        return Vec2(self.x % scalar, self.y % scalar)

    def __len__(self):
        """
        Returns the length of this Vec2 object.
        """
        return 2

    def __getitem__(self, index: int):
        """
        Returns the element at the given index.
        """
        return self.vec[index]

    def __eq__(self, other: object):
        """
        Returns True if the two vectors are equal.
        """
        if not isinstance(other, Vec2):
            return False
        return self.x == other.x and self.y == other.y

    def dot(self, other: "Vec2") -> float:
        """
        Returns the dot product of two Vec2 objects.
        """
        if not isinstance(other, Vec2):
            raise TypeError("Vec2 dot product requires two Vec2 objects.")
        return self.x * other.x + self.y * other.y

    def as_unit(self):
        """
        Returns the unit vector of this Vec2 object.
        """
        if self.x == 0 and self.y == 0:
            return Vec2(0, 0)
        else:
            return Vec2(self.x / self.norm, self.y / self.norm)

    def to_json(self):
        """
        Returns a json representation of this Vec2 object.
        """
        return {"x": self.x, "y": self.y}

    def to_tuple(self):
        """
        Returns a tuple representation of this Vec2 object.
        """
        return (self.x, self.y)

    def to_numpy(self):
        """
        Returns a numpy representation of this Vec2 object.
        """
        import numpy as np

        return np.array([self.x, self.y])


class Vec3:
    """
    Class for vectors of length 3.
    """

    def __init__(self, x: float = 0, y: float = 0, z: float = 0) -> None:
        """
        Vec3 contains (x, y, z) coordinates and its own norm.
        """
        if (
            not isinstance(x, (int, float))
            or not isinstance(y, (int, float))
            or not isinstance(z, (int, float))
        ):
            raise TypeError("Vec3 coordinates must be of type int or float.")
        self.x = x
        self.y = y
        self.z = z
        self.vec = (x, y, z)

    @property
    def norm(self):
        """Norm (euclidian length) of the vector."""
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)

    def __str__(self) -> str:
        return f"({self.x}, {self.y}, {self.z})"

    def __repr__(self) -> str:
        return f"Vec3({self.x}, {self.y}, {self.z})"

    def __add__(self, other: "Vec3") -> "Vec3":
        """
        Returns the sum of two Vec3 objects.
        """
        if not isinstance(other, Vec3):
            return NotImplemented
        x = self.x + other.x
        y = self.y + other.y
        z = self.z + other.z
        return Vec3(x, y, z)

    def __sub__(self, other: "Vec3") -> "Vec3":
        """
        Returns the difference of two Vec3 objects.
        """
        if not isinstance(other, Vec3):
            return NotImplemented
        x = self.x - other.x
        y = self.y - other.y
        z = self.z - other.z
        return Vec3(x, y, z)

    def __mul__(self, scalar: float) -> "Vec3":
        """
        Scalar multiplication of a Vec3 object.
        """
        return Vec3(self.x * scalar, self.y * scalar, self.z * scalar)

    def __truediv__(self, scalar: float) -> "Vec3":
        """
        Scalar division of a Vec3 object.
        """
        return Vec3(self.x / scalar, self.y / scalar, self.z / scalar)

    def __floordiv__(self, scalar: float) -> "Vec3":
        """
        Scalar floor division of a Vec3 object.
        """
        return Vec3(self.x // scalar, self.y // scalar, self.z // scalar)

    def __divmod__(self, scalar: float) -> "Vec3":
        """
        Scalar division of a Vec3 object.
        """
        return Vec3(self.x % scalar, self.y % scalar, self.z % scalar)

    def __len__(self):
        """
        Returns the length of this Vec3 object.
        """
        return 3

    def __getitem__(self, index):
        """
        Returns the element at the given index.
        """
        return self.vec[index]

    def __eq__(self, other: object):
        """
        Returns True if the two vectors are equal.
        """
        if not isinstance(other, Vec3):
            return False
        return self.x == other.x and self.y == other.y and self.z == other.z

    def cross(self, other: "Vec3") -> "Vec3":
        """
        Returns the cross product of two Vec3 objects.
        """
        if not isinstance(other, Vec3):
            raise TypeError("Vec3 cross product requires two Vec3 objects.")
        x = self.y * other.z - self.z * other.y
        y = self.z * other.x - self.x * other.z
        z = self.x * other.y - self.y * other.x
        return Vec3(x, y, z)

    def dot(self, other: "Vec3") -> float:
        """
        Returns the dot product of two Vec3 objects.
        """
        if not isinstance(other, Vec3):
            raise TypeError("Vec3 dot product requires two Vec3 objects.")
        return self.x * other.x + self.y * other.y + self.z * other.z

    def as_unit(self):
        """
        Returns the unit vector of this Vec3 object.
        """
        if self.x == 0 and self.y == 0 and self.z == 0:
            return Vec3(0, 0, 0)
        else:
            return Vec3(self.x / self.norm, self.y / self.norm, self.z / self.norm)

    def to_json(self):
        """
        Returns a json representation of this Vec3 object.
        """
        return {"x": self.x, "y": self.y, "z": self.z}

    def to_tuple(self):
        """
        Returns a tuple representation of this Vec3 object.
        """
        return (self.x, self.y, self.z)

    def to_numpy(self):
        """
        Returns a numpy representation of this Vec3 object.
        """
        import numpy as np

        return np.array([self.x, self.y, self.z])
