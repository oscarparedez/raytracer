from lib import *
from random import random
from math import inf, pi, tan

from sphere import *

MAX_RECURSION_DEPTH = 3

BLACK = color(0,0,0)

class RayTracer(object):
  def __init__(self, width, height):
    self.width = width
    self.height = height
    self.background_color = BLACK
    self.light = None
    self.clear()

  def clear(self):
    self.pixels = [
			[BLACK for _ in range(self.width)]
			for _ in range(self.height)
		]

  def write(self, filename):
    writebmp(filename, self.width, self.height, self.pixels)

  def point(self, x, y, col):
    self.pixels[y][x] = col

  def cast_ray(self, origin, direction, recursion = 0):
    # sourcery skip: inline-immediately-returned-variable
    material, intersect = self.scene_intersect(origin, direction)

    if material is None or recursion >= MAX_RECURSION_DEPTH:
      return self.background_color

    light_dir = norm(sub(self.light.position, intersect.point))

    offset_normal = mul(intersect.normal, 1.1) # shadow bias
    shadow_orig = sum(intersect.point, offset_normal) \
                if dot(light_dir, intersect.normal) >= 0 \
                else sub(intersect.point, offset_normal)
    
    shadow_material, shadow_intersect = self.scene_intersect(shadow_orig, light_dir)
    if shadow_material is None:
      shadow_intensity = 0
    else:
      shadow_intensity = 0.9
    
    if material.albedo[2] > 0:
      reverse_direction = mul(direction, -1)
      # print(reverse_direction)
      reflect_direction = reflect(reverse_direction, intersect.normal)
      reflect_origin = sum(intersect.point, offset_normal) \
                if dot(reflect_direction, intersect.normal) >= 0 \
                else sub(intersect.point, offset_normal)
      reflect_color = self.cast_ray(reflect_origin, reflect_direction, recursion+1)
    else:
      reflect_color = color(0, 0, 0)

    if material.albedo[3] > 0:
      refract_direction = refract(direction, intersect.normal, material.refractive_index)
      if refract_direction is None:
        # print('is NONE')
        refract_color = color(0, 0, 0)
      else:
        refract_origin = sum(intersect.point, offset_normal) \
                  if dot(refract_direction, intersect.normal) >= 0 \
                  else sub(intersect.point, offset_normal)
        refract_color = self.cast_ray(refract_origin, refract_direction, recursion+1)
    else:
      refract_color = color(0, 0, 0)




    diffuse_intensity = self.light.intensity * max(0, dot(light_dir, intersect.normal)) \
                        * (1 - shadow_intensity)
    
    if shadow_intensity > 0:
      specular_intensity = 0
    else:
      specular_reflection = reflect(light_dir, intersect.normal)
      specular_intensity = self.light.intensity * (
        max(0, dot(specular_reflection, direction)) ** material.spec
      )

    diffuse = material.diffuse * diffuse_intensity * material.albedo[0]
    specular = self.light.color* specular_intensity * material.albedo[1]
    reflection = reflect_color * material.albedo[2]
    refraction = refract_color * material.albedo[3]

    c = diffuse + specular + reflection + refraction

    return c

  def scene_intersect(self, origin, direction):
    # sourcery skip: merge-nested-ifs
    zbuffer = float('inf')
    material = None
    intersect = None
    
    for obj in self.scene:
      r_intersect = obj.ray_intersect(origin, direction)

      if r_intersect:
        if r_intersect.distance < zbuffer:
          zbuffer = r_intersect.distance # donde golpeo el rayo
          material = obj.material
          intersect = r_intersect

    return material, intersect

  def render(self):
    fov = pi / 2
    ar = (self.width / self.height)
    for y in range(self.height):
      for x in range(self.width):
        # if x % 2 == 0 and y % 2 == 0: # se usa mas la forma de random
        if random() > 0:
          i = (2 * ((x + 0.5) / self.width) - 1) * ar * tan(fov / 2)
          j = 1 - 2 * ((y + 0.5) / self.height) * ar * tan(fov / 2)

          direction = norm(V3(i, j, -1))
          col = self.cast_ray(V3(0, 0, 0), direction)
          self.point(x, y, col)

r = RayTracer(1000, 1000)

r.light = Light(position = V3(10, 10, 20), intensity = 4, color = color(255, 255, 255))
ivory = Material(diffuse=color(100, 100, 80), albedo=[0.6, 0.3, 0.1, 0], spec=50)
rubber = Material(diffuse=color(80, 0, 0), albedo=[0.9, 0.1, 0.0, 0], spec=10)
mirror = Material(diffuse=color(255, 255, 255), albedo=[0.0, 10, 0.8, 0], spec=1500)
glass = Material(diffuse=color(255, 255, 255), albedo=[0.0, 0.5, 0.1, 0.8], spec=1500, refractive_index=1.5)

r.scene = [
  Sphere(V3(0, -1.5, -10), 1.5, ivory),
  Sphere(V3(-2, 1, -12), 2, glass),
  Sphere(V3(1, 1, -8), 1.7, rubber),
  Sphere(V3(0, 5, -20), 5, rubber),
]
r.render()
r.write('r.bmp')