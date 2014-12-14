#!/usr/bin/python

import avango
import avango.script
from examples_common.GuaVE import GuaVE
from avango.script import field_has_changed
import avango.gua


import examples_common.navigator
from examples_common import device

import jsonloader


class Reloader(avango.script.Script):

  Keyboard = device.KeyboardDevice()


  def __init__(self):
    self.super(Reloader).__init__()
    self.always_evaluate(True)

    self.KeyR = False


  def myConstructor(self, json_path, root):
    self.loader = jsonloader.jsonloader()
    self.json_path = json_path
    self.root = root
    # self.pipe = pipe
    self.reload()    

  def get_window(self):
    return self.loader.windows[0]

  def reload(self):
    self.root.Children.value = []
    self.loader.load_json(self.json_path, self.root)
    # self.loader.load_and_set_PipelineOptions(self.pipe)

  def evaluate(self):
    if self.Keyboard.KeyR.value and not self.KeyR:
      pass
      # self.reload()
    self.KeyR = self.Keyboard.KeyR.value



def start():

  # setup scenegraph
  graph = avango.gua.nodes.SceneGraph(Name = "scenegraph")

  scene = avango.gua.nodes.TransformNode(Name = "scene")
  scene.Transform.value = avango.gua.make_identity_mat()

  light = avango.gua.nodes.PointLightNode(
                Name = "light",
                Color = avango.gua.Color(1.0, 1.0, 1.0),
                EnableShadows = True,
                Brightness = 30.0)

  light.Transform.value = avango.gua.make_trans_mat(1, 5, 4) * avango.gua.make_scale_mat(35, 35, 35)

  # graph.Root.value.Children.value = [screen, scene]


  reloader = Reloader()
  reloader.myConstructor("blabla.json", scene)

  # window = reloader.get_window()

  # setup viewing
  size = avango.gua.Vec2ui(1920, 1080)

  window = avango.gua.nodes.GlfwWindow(
    Size = size,
    LeftResolution = size
  )

  # pipe_desc = avango.gua.nodes.PipelineDescription()
  # pipe_desc.add_tri_mesh_pass()

  cam = avango.gua.nodes.CameraNode(Name = "cam",
                                    LeftScreenPath = "/cam/screen",
                                    SceneGraph = "scenegraph",
                                    Resolution = size,
                                    OutputWindowName = "window") 

  screen = avango.gua.nodes.ScreenNode(Name = "screen", Width = 4, Height = 3)
  screen.Transform.value = avango.gua.make_trans_mat(0.0, 0.0, -2.5)
  cam.Children.value = [screen]
  cam.Transform.value = avango.gua.make_trans_mat(0.0, 2.0, 5.0)



  graph.Root.value.Children.value = [cam, scene, light]

  avango.gua.register_window("window", window)

  #setup viewer
  viewer = avango.gua.nodes.Viewer()
  viewer.CameraNodes.value = [cam]
  viewer.SceneGraphs.value = [graph]
  viewer.Window.value = window

  navigator = examples_common.navigator.Navigator()
  navigator.StartLocation.value = cam.Transform.value.get_translate()
  navigator.OutTransform.connect_from(cam.Transform)

  cam.Transform.connect_from(navigator.OutTransform)

  navigator.RotationSpeed.value = 0.2
  navigator.MotionSpeed.value = 0.04

  guaVE = GuaVE()
  guaVE.start(locals(), globals(), show_banner = False)

  viewer.run()


if __name__ == '__main__':
  start()

