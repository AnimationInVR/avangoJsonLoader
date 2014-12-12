#!/usr/bin/python

import avango
import avango.script
from examples_common.GuaVE import GuaVE
from avango.script import field_has_changed
import avango.gua

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

  eye = avango.gua.nodes.TransformNode(Name = "eye")
  eye.Transform.value = avango.gua.make_trans_mat(0.0, 0.0, 3.5)

  screen = avango.gua.nodes.ScreenNode(Name = "screen", Width = 4, Height = 3)
  screen.Children.value = [eye]

  loader = avango.gua.nodes.TriMeshLoader()
  test = self.TriMeshLoader.create_geometry_from_file( name
                                 , "data/objects/Frog.obj"
                                 , "data/materials/White.gmd"
                                 , avango.gua.LoaderFlags.DEFAULTS | avango.gua.LoaderFlags.LOAD_MATERIALS)

  graph.Root.value.Children.value = [screen, scene, test]

  reloader = Reloader()
  reloader.myConstructor("blabla.json", scene)

  window = reloader.get_window()

  # setup viewing
  size = avango.gua.Vec2ui(1024, 768)
  pipe = avango.gua.nodes.Pipeline(Camera = avango.gua.nodes.Camera(LeftEye = "/screen/eye",
                                                                    RightEye = "/screen/eye",
                                                                    LeftScreen = "/screen",
                                                                    RightScreen = "/screen",
                                                                    SceneGraph = "scenegraph"),
                                   Window = window,
                                   LeftResolution = size)



  #setup viewer
  viewer = avango.gua.nodes.Viewer()
  viewer.Pipelines.value = [pipe]
  viewer.SceneGraphs.value = [graph]


  guaVE = GuaVE()
  guaVE.start(locals(), globals())

  viewer.run()


if __name__ == '__main__':
  start()

