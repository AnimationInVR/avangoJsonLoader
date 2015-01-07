from examples_common.GuaVE import GuaVE
import examples_common.navigator

import avango.gua

class Application:

  def __init__(self):
    self.viewer = None
    self.scenegraph = None
    self.window = None
    self.screen = None
    self.camera = None

  def run(self):
    print("run")
    guaVE = GuaVE()
    guaVE.start(locals(), globals(), show_banner = False)
    self.viewer.run()

  def basic_setup(self):
    self.viewer.CameraNodes.value = [self.camera]
    self.viewer.SceneGraphs.value = [self.scenegraph]
    self.viewer.Window.value = self.window

    self.camera.LeftScreenPath.value = "Camera/Screen"

    self.screen.Transform.value = avango.gua.make_trans_mat(0.0, 0.0, -2.5)
    self.camera.Transform.value = avango.gua.make_trans_mat(0.0, 2.0, 5.0)

    self.navigator = examples_common.navigator.Navigator()
    self.navigator.StartLocation.value = self.camera.Transform.value.get_translate()
    self.navigator.OutTransform.connect_from(self.camera.Transform)

    self.camera.Transform.connect_from(self.navigator.OutTransform)

    self.navigator.RotationSpeed.value = 0.2
    self.navigator.MotionSpeed.value = 0.04