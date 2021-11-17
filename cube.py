from plane import *
from lib import *
class Cube(object):
  def __init__(self, position, size, material):
    self.position = position
    self.material = material
    self.half_size = size / 2

    self.plane_origins = [
      V3(self.half_size, 0, 0),
      V3(0, self.half_size, 0),
      V3(0, 0, self.half_size),
      V3(-self.half_size, 0, 0),
      V3(0, -self.half_size, 0),
      V3(0, 0, -self.half_size),
    ]

    self.plane_directions = [
      norm(V3(1, 0, 0)),
      norm(V3(0, 1, 0)),
      norm(V3(0, 0, 1)),
      norm(V3(-1, 0, 0)),
      norm(V3(0, -1, 0)),
      norm(V3(0, 0, -1)),
    ]

    self.faces = [
      Plane(sum(position, self.plane_origins[0]), self.plane_directions[0], material),
      Plane(sum(position, self.plane_origins[1]), self.plane_directions[1], material),
      Plane(sum(position, self.plane_origins[2]), self.plane_directions[2], material),
      Plane(sum(position, self.plane_origins[3]), self.plane_directions[3], material),
      Plane(sum(position, self.plane_origins[4]), self.plane_directions[4], material),
      Plane(sum(position, self.plane_origins[5]), self.plane_directions[5], material),
    ]

#Basado en https://www.yumpu.com/en/document/read/7542517/an-efficient-and-robust-ray-box-intersection-algorithm-truesculpt
  def ray_intersect(self, origin, direction):
    stdev = 1e-12
    zbuffer = float("inf")
    ray_intersect = None

    inferior_limits = V3(
      self.position.x - (self.half_size + stdev),
      self.position.y - (self.half_size + stdev),
      self.position.z - (self.half_size + stdev)
    )

    superior_limits = V3(
      self.position.x + (self.half_size + stdev),
      self.position.y + (self.half_size + stdev),
      self.position.z + (self.half_size + stdev)
    )

    limit_diff = V3(
      superior_limits.x - inferior_limits.x,
      superior_limits.y - inferior_limits.y,
      superior_limits.z - inferior_limits.z,
    )

    #definir textura a cada cara del cubo
    for face in self.faces:
      face_interception = face.ray_intersect(origin, direction)

      if (face_interception and \
        face_interception.distance < zbuffer and \
        face_interception.point.x > inferior_limits.x and \
        face_interception.point.y > inferior_limits.y and \
        face_interception.point.z > inferior_limits.z and \
        face_interception.point.x <= superior_limits.x and \
        face_interception.point.y <= superior_limits.y and \
        face_interception.point.z <= superior_limits.z):
        
        zbuffer = face_interception.distance # donde golpeo el rayo, misma idea que scene_intersect
        ray_intersect = face_interception

        if abs(face.normal.x) > 0:
          texture = [
            (face_interception.point.y - inferior_limits.y) / limit_diff.y,
            (face_interception.point.z - inferior_limits.z) / limit_diff.z,
          ]
        
        if abs(face.normal.y) > 0:
          texture = [
            (face_interception.point.x- inferior_limits.x) / limit_diff.x,
            (face_interception.point.z - inferior_limits.z) / limit_diff.z,
          ]

        if abs(face.normal.z) > 0:
          texture = [
            (face_interception.point.x - inferior_limits.x) / limit_diff.x,
            (face_interception.point.y - inferior_limits.y) / limit_diff.y,
          ]
      else:
        pass

    if ray_intersect:
      return Intersect(
        distance = ray_intersect.distance, point = ray_intersect.point, normal = ray_intersect.normal, texture = texture
      )
    else:
      return None
    