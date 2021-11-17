from lib import *

class Plane(object):

  def __init__(self, position, normal, material):
    self.position = position
    self.normal = normal
    self.material = material

  #Basado en https://stackoverflow.com/questions/23975555/how-to-do-ray-plane-intersection
  def ray_intersect(self, origin, direction):
    stdev = 1e-12
    t = 0
    denom = dot(direction, self.normal)

    if abs(denom) > stdev:
        #t es donde pego el rayo
        t = dot(self.normal, sub(self.position, origin)) / denom
        if t >= stdev:
            hit = sum(origin, mul(direction, t))
            return Intersect(
              distance = t, 
              point = hit, 
              normal = self.normal
            )
        else:
          pass
    else:
      return None
