from examples_common.GuaVE import GuaVE
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

    self.camera.LeftScreenPath.value = self.screen.Path.value[1:]
