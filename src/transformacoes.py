from FGAme import *
from FGAme.mathtools import *

idx = 0
theta = pi / 60
M = Mat2([[cos(theta), -sin(theta)],
          [sin(theta), cos(theta)]])

theta = pi / 60
M2 = Mat2([[cos(theta), sin(theta)],
           [-sin(theta), cos(theta)]])


world = World()
poly = draw.Poly([M * Vec2(0, 0), M * Vec2(100, 0), M *Vec2(0, 100)])
poly.move(400, 300)
world.add(poly)

@schedule_dt
def update(dt):
    u = pos.middle
    poly._data = [M2 * M * (v - u) + u for v in poly._data]


world.run()
