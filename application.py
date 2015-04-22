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
    self.planned_time_field_connections = []
    self.root = avango.gua.nodes.TransformNode(
      Name = "Custom_Root",
      Transform = avango.gua.make_rot_mat(-90.0, 1.0, 0.0, 0.0)  
    )
    self.scenegraph.Root.value.Children.value.append(self.root)

  def run(self):
    #HACK FOR TEXTURE LOADING
    self.camera.EnableFrustumCulling.value = False

    guaVE = GuaVE()
    guaVE.start(locals(), globals(), show_banner = False)
    self.viewer.run()

  def start(self):
    self.apply_time_field_connections()
    #HACK FOR TEXTURE LOADING
    self.camera.EnableFrustumCulling.value = True

  def basic_setup(self):

    # size = avango.gua.Vec2ui(2560, 1440)
    size = avango.gua.Vec2ui(1920, 1080)

    # self.camera = avango.gua.nodes.CameraNode(
    #   LeftScreenPath = "/screen",
    #   SceneGraph = "SceneGraph",
    #   Resolution = size,
    #   OutputWindowName = "window",
    #   Transform = avango.gua.make_trans_mat(0.0, 0.0, 3.5)
    # )

    # self.screen = avango.gua.nodes.ScreenNode(
    #   Name = "screen",
    #   Width = 2,
    #   Height = 1.5,
    #   Children = [self.camera],
    #   Transform = avango.gua.make_trans_mat(0.0, 0.0, 15.0)
    # )
    self.camera.LeftScreenPath.value = self.screen.Path.value


    self.scenegraph.Root.value.Children.value.append(self.screen)

    self.window = avango.gua.nodes.GlfwWindow(
      Size = size,
      LeftResolution = size,
      EnableFullscreen = True,
    )
    avango.gua.register_window("window", self.window)

    self.viewer.SceneGraphs.value = [self.scenegraph]
    self.viewer.Windows.value = [self.window]

  def add_field_container(self, field_container):
    self.field_containers[field_container.Name.value] = field_container

  def add_field_connection(self, from_container_name, from_field_name, to_container_name, to_field_name):
    to_field = self.field_containers[to_container_name].get_field(to_field_name)
    from_field = self.field_containers[from_container_name].get_field(from_field_name)
    print( ("add field connection", to_field_name) )
    to_field.connect_from(from_field)

  def plan_field_connection(self, from_container_name, from_field_name, to_container_name, to_field_name):
    from_container_name = from_container_name.replace('.', '_')
    to_container_name = to_container_name.replace('.', '_')
    self.planned_field_connections.append((from_container_name, from_field_name, to_container_name, to_field_name))

  def plan_time_field_connection(self, from_container_name, from_field_name, to_container_name, to_field_name):
    from_container_name = from_container_name.replace('.', '_')
    to_container_name = to_container_name.replace('.', '_')
    self.planned_time_field_connections.append((from_container_name, from_field_name, to_container_name, to_field_name))

  def apply_field_connections(self):
    for fc in self.planned_field_connections:
      self.add_field_connection(fc[0], fc[1], fc[2], fc[3])
    self.planned_field_connections = []

  def apply_time_field_connections(self):
    timer = self.field_containers['time_sensor']
    timer.ReferenceTime.value = timer.RealTime.value
    timer.Time.value = 0.0

    for fc in self.planned_time_field_connections:
      self.add_field_connection(fc[0], fc[1], fc[2], fc[3])
    self.planned_time_field_connections = []

  def set_camera(self, camera):
    self.camera = camera
