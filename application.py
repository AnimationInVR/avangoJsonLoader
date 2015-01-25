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
    self.planned_field_connections = []

  def run(self):
    guaVE = GuaVE()
    guaVE.start(locals(), globals(), show_banner = False)
    self.viewer.run()

  def basic_setup(self):
    self.camera.LeftScreenPath.value = self.screen.Path.value
    self.viewer.CameraNodes.value = [self.camera]
    self.viewer.SceneGraphs.value = [self.scenegraph]
    self.viewer.Window.value = self.window

  def add_field_container(self, name, field_container):
    self.field_containers[name] = field_container

  def add_field_connection(self, from_container_name, from_field_name, to_container_name, to_field_name):
    to_field = self.field_containers[to_container_name].get_field(to_field_name)
    from_field = self.field_containers[from_container_name].get_field(from_field_name)
    print( ("add field connection", to_field_name, to_field, from_field, from_field.value) )
    to_field.connect_from(from_field)

  def plan_field_connection(self, from_container_name, from_field_name, to_container_name, to_field_name):
    self.planned_field_connections.append((from_container_name, from_field_name, to_container_name, to_field_name))

  def apply_field_connections(self):
    for fc in self.planned_field_connections:
      self.add_field_connection(fc[0], fc[1], fc[2], fc[3])
    self.planned_field_connections = []

  def set_camera(self, camera):
    self.camera = camera
    self.add_field_container(camera.Name.value, camera)