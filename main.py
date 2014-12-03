#!/usr/bin/python

import avango
import avango.script
import avango.gua

from examples_common.GuaVE import GuaVE

import jsonloader

def start():

  # setup scenegraph
  graph = avango.gua.nodes.SceneGraph(Name = "scenegraph")

  loader = jsonloader.jsonloader()
  loader.load_json("test.json", graph.Root.value)

  eye = avango.gua.nodes.TransformNode(Name = "eye")
  eye.Transform.value = avango.gua.make_trans_mat(0.0, 0.0, 3.5)

  screen = avango.gua.nodes.ScreenNode(Name = "screen", Width = 4, Height = 3)
  screen.Children.value = [eye]

  graph.Root.value.Children.value.append(screen)

  # setup viewing
  size = avango.gua.Vec2ui(1024, 768)
  pipe = avango.gua.nodes.Pipeline(Camera = avango.gua.nodes.Camera(LeftEye = "/screen/eye",
                                                                    RightEye = "/screen/eye",
                                                                    LeftScreen = "/screen",
                                                                    RightScreen = "/screen",
                                                                    SceneGraph = "scenegraph"),
                                   Window = avango.gua.nodes.Window(Size = size,
                                                                    LeftResolution = size),
                                   LeftResolution = size)

  loader.load_and_set_PipelineOptions(pipe)


  #setup viewer
  viewer = avango.gua.nodes.Viewer()
  viewer.Pipelines.value = [pipe]
  viewer.SceneGraphs.value = [graph]


  guaVE = GuaVE()
  guaVE.start(locals(), globals())

  viewer.run()


if __name__ == '__main__':
  start()

