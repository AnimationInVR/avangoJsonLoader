import avango
import avango.gua

import fieldcontainer
import application

import json

# json Loader Class
class jsonloader:

  def __init__(self):
    self.json_data = None
    self.root_node = None
    self.TriMeshLoader = avango.gua.nodes.TriMeshLoader()

    self.windows = {}

    self.scenegraphs = {}
    self.viewer = {}

  def create_application_from_json(self, json_path):
    print("creating application from", json_path)
    
    self.open_json(json_path)

    self.app = application.Application()

    self.app.viewer = self.load_viewer()
    self.app.scenegraph = self.load_scenegraph() 
    self.app.window = self.load_window()    

    self.app.scenegraph.Root.value = self.create_root()
    self.create_scenegraph_nodes()

    self.app.basic_setup()

    return self.app 

  def open_json(self, path):
    json_file = open(path)
    self.json_data = json.load(json_file)

  def create_scenegraph_nodes(self):
    nodes = {}
    child_parent_pairs = []

    new_screen, parent_name = self.load_screen()
    nodes[new_screen.Name.value] = new_screen
    child_parent_pairs.append( [new_screen.Name.value, parent_name] )
    self.app.screen = new_screen

    new_camera, parent_name = self.load_camera()
    nodes[new_camera.Name.value] = new_camera
    child_parent_pairs.append( [new_camera.Name.value, parent_name] )
    self.app.camera = new_camera

    for mesh in self.json_data["meshes"]:
      new_mesh, parent_name = self.load_mesh(mesh)
      nodes[new_mesh.Name.value] = new_mesh
      child_parent_pairs.append( [new_mesh.Name.value, parent_name] )

    for transform in self.json_data["transforms"]:
      new_transform, parent_name = self.load_transform(transform)
      nodes[new_transform.Name.value] = new_transform
      child_parent_pairs.append( [new_transform.Name.value, parent_name] )

    for light in self.json_data["lights"]:
      new_light, parent_name = self.load_light(light)
      nodes[new_light.Name.value] = new_light
      child_parent_pairs.append( [new_light.Name.value, parent_name] )

    self.create_scenegraph_structure(nodes, child_parent_pairs)

  def create_scenegraph_structure(self, nodes, child_parent_pairs):
    for pair in child_parent_pairs:
      # TODO
      if pair[1] == "Av_root":
        self.app.scenegraph.Root.value.Children.value.append(nodes[pair[0]])
      else:
        nodes[pair[1]].Children.value.append(nodes[pair[0]])
        

  def second_parse(self):
    self.create_scenegraph_structure() 

    for camera in self.json_data["cameras"]:
      self.load_camera_finish(camera)

    for viewer in self.json_data["viewer"]:
      self.load_viewer_finish(viewer)


  def create_root(self):
    node = avango.gua.nodes.TransformNode(Name = "Av_root")
    # Rotate to switch from Blenders to GL`s coordinate system
    node.Transform.value = avango.gua.make_rot_mat(-90.0, 1.0, 0.0, 0.0)

    return node



  def load_screen(self):
    print("load screen" )        
    
    json_screen = self.json_data["screens"]["Screen"]

    name = str(json_screen["name"])
    parent_name = str(json_screen["parent"])

    transform = load_transform_matrix( json_screen["transform"] )

    # TODO load hight and width

    screen = avango.gua.nodes.ScreenNode(Name = name, Width = 4, Height = 3)
    screen.Transform.value = transform

    return screen, parent_name


  def load_window(self):
    print("load window")   

    json_window = self.json_data["windows"]["Window"]

    title = str(json_window["title"] )
    name = str(json_window["name"])
    size = avango.gua.Vec2ui(json_window["left_resolution"][0], 
                             json_window["left_resolution"][1] )

    mode = 0
    if (json_window["mode"] == "MONO"):
      mode = 0
    # TODO more stereo modes

    display = str(json_window["display"])

    new_window = avango.gua.nodes.GlfwWindow(Name = name, Size = size, LeftResolution = size,
                  StereoMode = mode, Title = title, Display = display)
    
    avango.gua.register_window(name, new_window)

    return new_window 


  def load_mesh(self, mesh):
    print("load mesh" , mesh) 

    json_mesh = self.json_data["meshes"][mesh]

    name = str(json_mesh["name"])
    parent_name = str(json_mesh["parent"])

    transform = load_transform_matrix( json_mesh["transform"] )

    default_material = avango.gua.create_default_material()
    default_material.set_uniform("Color", avango.gua.Vec4(0.4, 0.3, 0.3, 1.0))
    default_material.set_uniform("Roughness", 0.4)
    default_material.set_uniform("Metalness", 0.8)

    geometry = self.TriMeshLoader.create_geometry_from_file( name
                                 , str(json_mesh["file"])
                                 , default_material
                                 , 0)
                                 # TODO
                                 # , avango.gua.LoaderFlags.LOAD_MATERIALS)
  
    fieldcontainer.Trimesh(geometry)

    geometry.Transform.value = transform

    return geometry, parent_name

  def load_camera(self):
    print("load camera")        

    json_camera = self.json_data["cameras"]["Camera"]

    name = str(json_camera["name"])
    parent_name = str(json_camera["parent"])

    transform = load_transform_matrix( json_camera["transform"] )

    scenegraph = str(json_camera["scenegraph"])

    resolution = avango.gua.Vec2ui(json_camera["resolution"][0], json_camera["resolution"][1] )

    output_window = str(json_camera["output_window_name"])


    cam = avango.gua.nodes.CameraNode(Name = name,
                                      # LeftScreenPath = "",
                                      SceneGraph = scenegraph,
                                      Resolution = resolution,
                                      OutputWindowName = output_window,
                                      Transform = transform)
    
    return cam, parent_name 

  def load_camera_finish(self, camera):
    print("load camera" , camera)        

    json_camera = self.json_data["cameras"][camera]

    name = str(json_camera["name"])
    left_screen = str(json_camera["left_screen_path"])

    cam = self.scene_graph_nodes[name]
    screen = self.scene_graph_nodes[left_screen]
    
    sep = '/'
    path = screen.Path.value
    path_parts = path.split(sep)
    path_parts.pop(0)
    path = sep.join(path_parts)
    cam.LeftScreenPath.value = path


  def load_transform(self, transform):       
    print("load transform" , transform)       
 
    json_transform = self.json_data["transforms"][transform]

    name = str(json_transform["name"])
    parent_name = str(json_transform["parent"])

    transform = load_transform_matrix( json_transform["transform"] )

    node = avango.gua.nodes.TransformNode(Name = name)
    node.Transform.value = transform

    return node, parent_name


  def load_light(self, light):      
    print("load light" , light)   

    json_light = self.json_data["lights"][light]

    name = str(json_light["name"])
    parent_name = str(json_light["parent"])


    transform = load_transform_matrix( json_light["transform"] )

    distance = json_light["distance"]
    transform = transform * avango.gua.make_scale_mat(distance)

    color = avango.gua.Color(json_light["color"][0], json_light["color"][1], json_light["color"][2])

    energy = json_light["energy"]

    light = avango.gua.nodes.PointLightNode(Name = name
                                           ,Transform = transform
                                           ,Color = color
                                           ,EnableShadows = True
                                           ,Brightness = energy * 10)

    return light, parent_name

  def load_scenegraph(self):     
    print("load scenegraph")

    json_scenegraph = self.json_data["scenegraphs"]["SceneGraph"]

    name = str(json_scenegraph["name"])
    root = str(json_scenegraph["root"])

    graph = avango.gua.nodes.SceneGraph(Name = name)

    return graph

  def load_viewer(self):
    print("load viewer")

    json_viewer = self.json_data["viewer"]["Viewer"]
    name = json_viewer["name"]
    viewer = avango.gua.nodes.Viewer(Name = name)

    return viewer 

  def load_viewer_finish(self):

    self.app.viewer.Window.value = self.windows[json_viewer["window"]]
    self.app.viewer.SceneGraphs.value = [ self.scenegraphs[json_viewer["camera"]] ]
    self.app.viewer.CameraNodes.value = [ self.scene_graph_nodes[json_viewer["scenegraph"]] ]


  def load_and_set_PipelineOptions(self, pipe):
    # GENERAL
    pipe.EnablePreviewDisplay.value   = self.json_data["pipeline_options"]["enable_preview_display"]
    pipe.EnableFPSDisplay.value       = self.json_data["pipeline_options"]["enable_fps_display"]
    pipe.EnableRayDisplay.value       = self.json_data["pipeline_options"]["enable_ray_display"]
    pipe.EnableBBoxDisplay.value      = self.json_data["pipeline_options"]["enable_bbox_display"]
    # pipe.EnableWireframe.value        = self.json_data["pipeline_options"]["enable_wire_frame"]
    pipe.EnableFXAA.value             = self.json_data["pipeline_options"]["enable_FXAA"]
    pipe.EnableFrustumCulling.value   = self.json_data["pipeline_options"]["enable_frustum_culling"]
    pipe.EnableBackfaceCulling.value  = self.json_data["pipeline_options"]["enable_backface_culling"]

    # CLIPPING
    pipe.NearClip.value  = self.json_data["pipeline_options"]["near_clip"]
    pipe.FarClip.value  = self.json_data["pipeline_options"]["far_clip"]

    # SSAO
    pipe.EnableSsao.value    = self.json_data["pipeline_options"]["ssao_settings"]["enable"]
    pipe.SsaoRadius.value    = self.json_data["pipeline_options"]["ssao_settings"]["radius"]
    pipe.SsaoIntensity.value = self.json_data["pipeline_options"]["ssao_settings"]["intensity"]
    pipe.SsaoFalloff.value   = self.json_data["pipeline_options"]["ssao_settings"]["falloff"]

    # BLOOM
    pipe.EnableBloom.value    = self.json_data["pipeline_options"]["bloom_settings"]["enable"]
    pipe.BloomRadius.value    = self.json_data["pipeline_options"]["bloom_settings"]["radius"]
    pipe.BloomThreshold.value = self.json_data["pipeline_options"]["bloom_settings"]["threshold"]
    pipe.BloomIntensity.value = self.json_data["pipeline_options"]["bloom_settings"]["intensity"]

    # FOG
    pipe.EnableFog.value   = self.json_data["pipeline_options"]["fog_settings"]["enable"]
    pipe.FogStart.value    = self.json_data["pipeline_options"]["fog_settings"]["start"]
    pipe.FogEnd.value      = self.json_data["pipeline_options"]["fog_settings"]["end"]
    pipe.FogTexture.value  = str( self.json_data["pipeline_options"]["fog_settings"]["texture"] )
    fog_color = self.json_data["pipeline_options"]["fog_settings"]["color"]
    pipe.FogColor.value    = avango.gua.Color(fog_color[0], fog_color[1], fog_color[2])

    # BACKGROUND
    pipe.BackgroundMode.value    = self.json_data["pipeline_options"]["background_settings"]["mode"]
    pipe.BackgroundTexture.value = str( self.json_data["pipeline_options"]["background_settings"]["texture"] )
    background_color = self.json_data["pipeline_options"]["background_settings"]["color"]
    pipe.BackgroundColor.value   = avango.gua.Color(background_color[0], background_color[1], background_color[2])

    # VIGNETTE
    pipe.EnableVignette.value   = self.json_data["pipeline_options"]["vignette_settings"]["enable"]
    vignette_color = self.json_data["pipeline_options"]["vignette_settings"]["color"]
    pipe.VignetteColor.value   = avango.gua.Color(vignette_color[0], vignette_color[1], vignette_color[2])
    pipe.VignetteCoverage.value = self.json_data["pipeline_options"]["vignette_settings"]["coverage"]
    pipe.VignetteSoftness.value = self.json_data["pipeline_options"]["vignette_settings"]["softness"]

    # HDR
    pipe.EnableHDR.value = self.json_data["pipeline_options"]["hdr_settings"]["enable"]
    pipe.HDRKey.value    = self.json_data["pipeline_options"]["hdr_settings"]["key"]


def load_transform_matrix(matrix_list):
  transform = avango.gua.make_identity_mat()

  for element in range(len(matrix_list)):
    transform.set_element(int(element/4), element%4 ,matrix_list[element])

  return transform
