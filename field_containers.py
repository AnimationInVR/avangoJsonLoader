#!/usr/bin/python
import avango
import avango.gua
import avango.script
from avango.script import field_has_changed

class RotationMatrix(avango.script.Script):

  # Input
  Angle = avango.SFFloat()
  Axis = avango.gua.SFVec3()

  # Output
  Matrix = avango.gua.SFMatrix4()

  def __init__(self):
    self.super(RotationMatrix).__init__()

    self.Name.value = "RotationMatrix"

    self.Angle.value = 0
    self.Axis.value = avango.gua.Vec3(1.0, 0.0, 0.0)

  def set_name(self, name):
    self.Name.value = name

  def evaluate(self):
    self.Matrix.value = avango.gua.make_rot_mat(self.Angle.value, self.Axis.value) 