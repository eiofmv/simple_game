import pygame
from vector import Vec2d

class Polyline:
    '''
    Class for drawing dots.
    '''
    def __init__(self):
        self.points = []
        self.speeds = []
        self.velocity = 1

    def new_point(self, point, speed):
        '''
        Adds new point.
        :param point:
        :param speeds:
        :return:
        '''
        self.points.append(Vec2d(*point))
        self.speeds.append(Vec2d(*speed))

    def pop_point(self):
        '''
        Deletes last point.
        :return:
        '''
        if len(self.points) > 0:
            self.points.pop()
            self.speeds.pop()

    def set_points(self, screen_dim):
        '''
        Re-positioning of every point.
        :return:
        '''
        for p in range(len(self.points)):
            self.points[p] = self.points[p] + self.speeds[p] * self.velocity
            if self.points[p].x > screen_dim[0] or self.points[p].x < 0:
                self.speeds[p].x = -self.speeds[p].x
            if self.points[p].y > screen_dim[1] or self.points[p].y < 0:
                self.speeds[p].y = -self.speeds[p].y

    def draw_points(self, display, width=3, color=(255, 255, 255)):
        for p in self.points:
            pygame.draw.circle(display, color, p.int_pair(), width)


class Knot(Polyline):
    '''
    Class for drawing curves. And also points.
    '''
    def __init__(self, steps):
        super().__init__()
        self.steps = steps
        self.knot = []

    def get_point(self, points, alpha, deg=None):
        if deg is None:
            deg = len(points) - 1
        if deg == 0:
            return points[0]
        return ((points[deg] * alpha) + (self.get_point(points, alpha, deg - 1) * (1 - alpha)))

    def get_points(self, points):
        alpha = 1 / self.steps
        res = []
        for i in range(self.steps):
            res.append(self.get_point(points, i * alpha))
        return res

    def get_knot(self):
        '''
        Finds curve's coords.
        :return:
        '''
        if len(self.points) < 3:
            self.knot = []
        else:
            res = []
            for i in range(-2, len(self.points) - 2):
                ptn = []
                ptn.append(((self.points[i] + self.points[i + 1]) * 0.5))
                ptn.append(self.points[i + 1])
                ptn.append(((self.points[i + 1] + self.points[i + 2]) * 0.5))

                res.extend(self.get_points(ptn))
            self.knot = res

    def new_point(self, point, speeds):
        super().new_point(point, speeds)
        self.get_knot()

    def set_points(self, screen_dim):
        super().set_points(screen_dim)
        self.get_knot()

    def pop_point(self):
        super().pop_point()
        self.get_knot()

    def draw_points(self, display, width=3, color=(255, 255, 255)):
        super().draw_points(display)
        for p_n in range(-1, len(self.knot) - 1):
            pygame.draw.line(display, color, self.knot[p_n].int_pair(),
                             self.knot[p_n + 1].int_pair(), width)

class ManyCurves:
    '''
    Extra task class for many curves.
    '''
    def __init__(self, steps):
        self.curves = []
        self.knot = Knot(steps)
        self.curves.append(self.knot)
        self.curve_num = 0

    def change_curve(self, direction):
        self.curve_num = (self.curve_num + direction) % len(self.curves)
        self.knot = self.curves[self.curve_num]

    def new_curve(self):
        self.knot = Knot(self.curves[0].steps)
        self.curve_num = len(self.curves)
        self.curves.append(self.knot)

    def del_curve(self):
        if len(self.curves) > 1:
            if self.curve_num == len(self.curves) - 1:
                self.curves.pop()
                self.curve_num -= 1
                self.knot = self.curves[self.curve_num]
            else:
                self.curves.pop()

    def update_steps(self, steps):
        for i in self.curves:
            i.steps = steps

    def update_velocity(self, velocity):
        for i in self.curves:
            i.velocity *= velocity

    def draw_points(self, display, color):
        for i in self.curves:
            i.draw_points(display, color=color)

    def set_points(self, SCREEN_DIM):
        for i in self.curves:
            i.set_points(SCREEN_DIM)

    def new_point(self, point, speed):
        self.knot.new_point(point, speed)

    def pop_point(self):
        self.knot.pop_point()