import numpy as np

"""
    Vec2 and Vec3 classes for arithmetic operations between 2- and 3-element vectors.
"""

class Vec2:
    """
        Class for vectors of length 2.
    """
    def __init__(self, x: float | int, y: float | int) -> None:
        """
            Vec2 contains (x, y) coordinates and its own norm.
        """
        self.x = x
        self.y = y
        self.vec = (x, y)
        self.norm = np.linalg.norm(self.vec)
    
    def __str__(self) -> str:
        return "{}".format(self.vec)

    def __add__(self, other):
        """
            Returns the sum of two Vec2 objects.
        """
        x = self.x + other.x
        y = self.y + other.y
        return Vec2(x, y)

    def __sub__(self, other):
        """
            Returns the difference of two Vec2 objects.
        """
        x = self.x - other.x
        y = self.y - other.y
        return Vec2(x, y)
    
    def __mul__(self, other) -> int | float:
        """
            Returns the DOT product of two Vec2 objects.
        """
        return self.x * other.x + self.y * other.y

    def __truediv__(self, other):
        """
            Divides two Vec2 objects if you ever need to do it.
        """
        x = self.x / other.x
        y = self.y / other.y
        return Vec2(x, y)

    def getUnitVec(self):
        """
            Returns the unit vector of this Vec2 object.
        """
        return Vec2(self.x / self.norm, self.y / self.norm)

class Vec3:
    """
        Class for vectors of length 3.
    """
    def __init__(self, x: float | int, y: float | int, z: float | int) -> None:
        """
            Vec3 contains (x, y, z) coordinates and its own norm.
        """
        self.x = x
        self.y = y
        self.z = z
        self.vec = (x, y, z)
        self.norm = np.linalg.norm(self.vec)
    
    def __str__(self) -> str:
        return "{}".format(self.vec)

    def __add__(self, other):
        """
            Returns the sum of two Vec3 objects.
        """
        x = self.x + other.x
        y = self.y + other.y
        z = self.z + other.z
        return Vec3(x, y, z)

    def __sub__(self, other):
        """
            Returns the difference of two Vec3 objects.
        """
        x = self.x - other.x
        y = self.y - other.y
        z = self.z - other.z
        return Vec3(x, y, z)
        
    def __mul__(self, other) -> int | float:
        """
            Returns the DOT product of two Vec3 objects.
        """
        return self.x * other.x + self.y * other.y + self.z * other.z

    def __truediv__(self, other):
        """
            Divides two Vec3 objects if you ever need to do it.
        """
        x = self.x / other.x
        y = self.y / other.y
        z = self.z / other.z
        return Vec3(x, y, z)
    
    def getUnitVec(self):
        """
            Returns the unit vector of this Vec3 object.
        """
        return Vec3(self.x / self.norm, self.y / self.norm, self.z / self.norm)