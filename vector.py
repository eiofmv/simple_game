import math

class Vec2d:
    """
    Class for 2D vectors.
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, vec):
        return Vec2d(self.x + vec.x, self.y + vec.y)

    def __sub__(self, vec):
        return Vec2d(self.x - vec.x, self.y - vec.y)

    def __mul__(self, k):
        if type(k) == int or type(k) == float:
            return Vec2d(self.x * k, self.y * k)
        else:
            return Vec2d(self.x * k.x + self.y * k.y)

    def int_pair(self):
        return (int(self.x), int(self.y))

    def __len__(self):
        return int(math.sqrt(self.x * self.x + self.y * self.y))