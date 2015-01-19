from examples_common.GuaVE import GuaVE
import avango.gua

class Application:

  def __init__(self):
    self.viewer = avango.gua.nodes.Viewer(Name = 'Viewer')
    self.scenegraph = avango.gua.nodes.SceneGraph(Name = 'SceneGraph')
    self.window = None
    self.screen = None
    self.camera = None
    self.field_containers = {}

  def run(self):
    print("run")
    guaVE = GuaVE()
    guaVE.start(locals(), globals(), show_banner = False)
    self.viewer.run()

  def basic_setup(self):
    self.viewer.CameraNodes.value = [self.camera]
    self.viewer.SceneGraphs.value = [self.scenegraph]
    self.viewer.Window.value = self.window

    self.camera.LeftScreenPath.value = self.screen.Path.value[1: ]

  def add_field_container(self, name, field_container):
    self.field_containers[name] = field_container

  def add_field_connection(self, from_container_name, from_field_name, to_container_name, to_field_name):
    to_field = self.field_containers[to_container_name].get_field(to_field_name)
    from_field = self.field_containers[from_container_name].get_field(from_field_name)
    print( ("laod field connection", to_field_name, to_field, from_field, from_field.value) )
    to_field.connect_from(from_field)

  def set_camera(self, camera):
    self.camera = camera
    self.add_field_container(camera.Name.value, camera)