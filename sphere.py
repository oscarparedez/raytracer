from lib import *

class Sphere(object):
  def __init__(self, center, radius, material):
    self.center = center
    self.radius = radius
    self.material = material

  def ray_intersect(self, origin, direction):  # sourcery skip: return-identity
    L = sub(self.center, origin)
    tca = dot(L, direction)
    l = length(L)

    d2 = l**2 - tca**2

    # pego afuera de la esfera
    if d2 > self.radius**2:
      return None

    thc = (self.radius**2 - d2)**(1/2)

    t0 = tca - thc
    t1 = tca + thc

    if t0 < 0:
      t0 = t1
    if t0 < 0: # esfera atras de la camara
      return None

    hit = sum(origin, mul(direction, t0))
    # normal = sub(hit, self.center)
    normal = norm(sub(hit, self.center))

    # t0 es donde pego el rayo
    return Intersect(
      distance=t0,
      normal=normal,
      point=hit
    )