import avango
import avango.gua

import json

''' TRANSFORM NODE JSON

    "transforms": {
        "Av_root": {
            "type" : "Transform",
            "parent" : "null",
            "transform": [
                1.0,
                0.0,
                0.0,
                0.0,
                0.0,
                1.0,
                0.0,
                0.0,
                0.0,
                0.0,
                1.0,
                0.0,
                0.0,
                0.0,
                0.0,
                1.0
            ],
            "name" : "Av_root"
        }
    },

'''



# json Loader Class
class jsonloader:

  def __init__(self):
    self.json_data = None
    self.root_node = None
    self.TriMeshLoader = avango.gua.nodes.TriMeshLoader()

    self.windows = {}

    self.scene_graph_nodes = {}
    self.child_parent_pairs =[]

    self.scenegraphs = {}
    self.viewer = {}

  def load_json(self, path, root_node):
    json_file = open(path)
    self.json_data = json.load(json_file)
    self.root_node = root_node
    self.first_parse()
    self.second_parse()

  def first_parse(self):
    for screen in self.json_data["screens"]:
      new_screen = self.load_screen(screen)
      self.scene_graph_nodes[screen] = new_screen

    for mesh in self.json_data["meshes"]:
      new_mesh = self.load_mesh(mesh)
      self.scene_graph_nodes[new_mesh.Name.value] = new_mesh

    for camera in self.json_data["cameras"]:
      new_camera = self.load_camera(camera)
      self.scene_graph_nodes[new_camera.Name.value] = new_camera

    for transform in self.json_data["transforms"]:
      new_transform = self.load_transform(transform)
      self.scene_graph_nodes[new_transform.Name.value] = new_transform

    for light in self.json_data["lights"]:
      new_light = self.load_light(light)
      self.scene_graph_nodes[new_light.Name.value] = new_light

    for window in self.json_data["windows"]:
      new_window = self.load_window(window)
      self.windows[new_window.Name.value] = new_window
    
    for scenegraph in self.json_data["scenegraphs"]:
      new_scenegraph = self.load_scenegraph(scenegraph)
      self.scenegraphs[new_scenegraph.Name.value] = new_scenegraph

    for viewer in self.json_data["viewer"]:
      new_viewer = self.load_viewer(viewer)
      self.viewer[new_viewer.Name.value] = new_viewer


  def second_parse(self):
    self.create_scenegraph_structure() 

    for camera in self.json_data["cameras"]:
      self.load_camera_finish(camera)

    for viewer in self.json_data["viewer"]:
      self.load_viewer_finish(viewer)

      

  def create_scenegraph_structure(self):
    for pair in self.child_parent_pairs:
      self.scene_graph_nodes[pair[1]].Children.value.append(self.scene_graph_nodes[pair[0]])
      # self.root_node.Children.value.append(self.scene_graph_nodes[pair[0]])

  def load_screen(self, screen):
    print("load screen" , screen)        
    
    json_screen = self.json_data["screens"][screen]

    name = str(json_screen["name"])
    parent = str(json_screen["parent"])

    # transform = load_transform_matrix( json_screen["transform"] )
    transform = avango.gua.make_trans_mat(0.0, 0.0, -2.5)

    # TODO load hight and width

    screen = avango.gua.nodes.ScreenNode(Name = name, Width = 4, Height = 3)
    screen.Transform.value = transform

    self.child_parent_pairs.append( (name, parent) )

    return screen


  def load_window(self, window):
    print("load window" , window)   

    json_window = self.json_data["windows"][window]

    title = str( json_window["title"] )
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
    parent = str(json_mesh["parent"])

    transform = load_transform_matrix( json_mesh["transform"] )

    default_material = avango.gua.create_default_material()
    default_material.set_uniform("Color", avango.gua.Vec4(0.4, 0.3, 0.3, 1.0))
    default_material.set_uniform("Roughness", 0.4)
    default_material.set_uniform("Metalness", 0.8)

    geometry = self.TriMeshLoader.create_geometry_from_file( name
                                 , str(json_mesh["file"])
                                 , default_material
                                 , avango.gua.LoaderFlags.LOAD_MATERIALS)

    
    geometry.Transform.value = transform

    self.child_parent_pairs.append( (name, parent) )
    
    return geometry

  def load_camera(self, camera):
    print("load camera" , camera)        

    json_camera = self.json_data["cameras"][camera]

    name = str(json_camera["name"])
    parent = str(json_camera["parent"])

    # transform = load_transform_matrix( json_camera["transform"] )
    transform = avango.gua.make_trans_mat(0.0, 0.0, 5.0)

    scenegraph = str(json_camera["scenegraph"])

    resolution = avango.gua.Vec2ui(json_camera["resolution"][0], json_camera["resolution"][1] )

    output_window = str(json_camera["output_window_name"])


    cam = avango.gua.nodes.CameraNode(Name = name,
                                      # LeftScreenPath = "",
                                      SceneGraph = scenegraph,
                                      Resolution = resolution,
                                      OutputWindowName = output_window,
                                      Transform = transform)
    self.child_parent_pairs.append( (name, parent) )
    
    return cam 

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
    parent = str(json_transform["parent"])

    transform = load_transform_matrix( json_transform["transform"] )

    node = avango.gua.nodes.TransformNode(Name = name)
    node.Transform.value = transform

    if (json_transform["parent"] == "null"):
      self.root_node.Children.value.append(node)
    else:
      self.child_parent_pairs.append( (name, parent) )


    return node


  def load_light(self, light):      
    print("load light" , light)   

    json_light = self.json_data["lights"][light]

    name = str(json_light["name"])
    parent = str(json_light["parent"])


    transform = load_transform_matrix( json_light["transform"] )

    distance = json_light["distance"]
    transform = transform * avango.gua.make_scale_mat(distance)

    color = avango.gua.Color(json_light["color"][0], json_light["color"][1], json_light["color"][2])

    energy = json_light["energy"]

    light = avango.gua.nodes.PointLightNode(Name = name, Transform = transform, Color = color, EnableShadows = True, Brightness = energy)

    self.child_parent_pairs.append( (name, parent) )

    return light

  def load_scenegraph(self, scenegraph):     
    print("load scenegraph" , scenegraph)

    json_scenegraph = self.json_data["scenegraphs"][scenegraph]

    name = str(json_scenegraph["name"])
    root = str(json_scenegraph["root"])

    graph = avango.gua.nodes.SceneGraph(Name = name)
    graph.Root.value = self.scene_graph_nodes[root]

    return graph

  def load_viewer(self, viewer):
    print("load viewer" , viewer)

    json_viewer = self.json_data["viewer"][viewer]
    name = json_viewer["name"]
    viewer = avango.gua.nodes.Viewer(Name = name)

    return viewer 

  def load_viewer_finish(self, viewer):
    print("load viewer" , viewer)

    json_viewer = self.json_data["viewer"][viewer]

    name = json_viewer["name"]
    
    viewer = self.viewer[name]

    viewer.Window.value = self.windows[json_viewer["window"]]
    viewer.SceneGraphs.value = [ self.scenegraphs[json_viewer["camera"]] ]
    viewer.CameraNodes.value = [ self.scene_graph_nodes[json_viewer["scenegraph"]] ]


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

  return switch_coordinate_systems(transform)


def switch_coordinate_systems(mat):

  return  avango.gua.make_scale_mat(1.0, 1.0, -1.0) \
          *avango.gua.make_rot_mat(-90, 1.0, 0.0, 0.0) \
          *mat \
          *avango.gua.make_rot_mat(90, 1.0, 0.0, 0.0) \
          *avango.gua.make_scale_mat(1.0, 1.0, -1.0)



def printscenegraph(scenegraph):
  for node in scenegraph.Root.value.Children.value:
    printhelper(node)

def printhelper(node):
  stack = []
  stack.append((node,0))

  while stack:
    tmp = stack.pop()
    printelement(tmp)
    for child in tmp[0].Children.value:
      stack.append((child,tmp[1]+1))

def printelement(nodetupel):
  for i in range(0, nodetupel[1]):
    print(" ", end=""),
  print(nodetupel[0].Name.value + "   ")
  #print nodetupel[0]
  #print nodetupel[0].Transform.value
