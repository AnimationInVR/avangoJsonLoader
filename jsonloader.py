import avango
import avango.gua

import json

# json Loader Class
class jsonloader:

  def __init__(self):
    self.json_data = None
    self.root_node = None
    self.TriMeshLoader = avango.gua.nodes.TriMeshLoader()
    self.windows = []
    self.scene_graph_nodes = {}
    self.child_parent_pairs =[]

  def load_json(self, path, root_node):
    json_file = open(path)
    self.json_data = json.load(json_file)
    self.root_node = root_node

    for viewer in self.json_data["viewer"]:
      self.load_viewer(viewer)

    for screen in self.json_data["screens"]:
      new_screen = self.load_screen(screen)
      self.scene_graph_nodes[screen] = new_screen

    for window in self.json_data["windows"]:
      self.windows.append( self.load_window(window) )

    for mesh in self.json_data["meshes"]:
      new_mesh = self.load_mesh(mesh)
      self.scene_graph_nodes[new_mesh.Name.value] = new_mesh

    for camera in self.json_data["cameras"]:
      self.load_camera(camera)

    for transform in self.json_data["transforms"]:
      new_transform = self.load_transform(transform)
      self.scene_graph_nodes[transform] = new_transform

    for light in self.json_data["lights"]:
      new_light = self.load_light(light)
      self.scene_graph_nodes[light] = new_light
    
    for scenegraph in self.json_data["scenegraphs"]:
      self.load_scenegraph(scenegraph)
  
    self.create_scenegraph_structure()  

  def create_scenegraph_structure(self):
    for pair in self.child_parent_pairs:
      # self.scene_graph_nodes[pair[1]].Children.value.append(self.scene_graph_nodes[pair[0]])
      self.root_node.Children.value.append(self.scene_graph_nodes[pair[0]])
      
  def load_viewer(self, viewer):
    print("load viewer" , viewer)
    # TODO        

  def load_screen(self, screen):
    print("load screen" , screen)        
    return "dummy"
    # TODO        

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

    new_window = avango.gua.nodes.Window(Name = name, Size = size, LeftResolution = size,
                  StereoMode = mode, Title = title, Display = display)
    
    return new_window 


  def load_mesh(self, mesh):
    print("load mesh" , mesh) 

    json_mesh = self.json_data["meshes"][mesh]

    name = str(json_mesh["name"])
    parent = str(json_mesh["parent"])

    # translate = self.json_data["objects"][object]["position"]
    # translate = avango.gua.Vec3(translate[0], translate[1], translate[2])
    
    # quaternion = self.json_data["objects"][object]["quaternion"]
    # quaternion = avango.gua.Quat(quaternion[0], quaternion[1], quaternion[2], quaternion[3])
    # quaternion.normalize()
    
    # scale = self.json_data["objects"][object]["scale"]
    # scale = avango.gua.Vec3(scale[0], scale[1], scale[2])

    # transformation = avango.gua.make_trans_mat(translate) \
             # * avango.gua.make_rot_mat(quaternion) \
             # * avango.gua.make_scale_mat(scale)

    transformation = avango.gua.make_identity_mat()
    
    geometry = self.TriMeshLoader.create_geometry_from_file( name
                                 , str(json_mesh["file"])
                                 , "data/materials/White.gmd"
                                 , avango.gua.LoaderFlags.DEFAULTS | avango.gua.LoaderFlags.LOAD_MATERIALS)
    geometry.Transform.value = transformation

    self.child_parent_pairs.append( (name, parent) )
    
    return geometry

  def load_camera(self, camera):
    print("load camera" , camera)        

    json_camera = self.json_data["cameras"][camera]

    name = str(json_camera["name"])
    resolution = avango.gua.Vec2ui(json_camera["resolution"][0], json_camera["resolution"][1] )

    # TODO new camera layout
    # new_camera = avango.gua.nodes.Camera(Name = name, LeftResolution = size,
                  # StereoMode = mode, Title = title, Display = display)
    
    # return new_camera 


  def load_transform(self, transform):       
    print("load transform" , transform)       
 
    json_transform = self.json_data["transforms"][transform]

    name = str(json_transform["name"])
    parent = str(json_transform["parent"])

    # translate = self.json_data["objects"][object]["position"]
    # translate = avango.gua.Vec3(translate[0], translate[1], translate[2])
    
    # quaternion = self.json_data["objects"][object]["quaternion"]
    # quaternion = avango.gua.Quat(quaternion[0], quaternion[1], quaternion[2], quaternion[3])
    # quaternion.normalize()
    
    # scale = self.json_data["objects"][object]["scale"]
    # scale = avango.gua.Vec3(scale[0], scale[1], scale[2])

    # transformation = avango.gua.make_trans_mat(translate) \
    #          * avango.gua.make_rot_mat(quaternion) \
    #          * avango.gua.make_scale_mat(scale)


    node = avango.gua.nodes.TransformNode(Name = name)
    node.Transform.value = avango.gua.make_identity_mat()

    if (json_transform["root"]):
      self.root_node.Children.value.append(node)
    else:
      self.child_parent_pairs.append( (name, parent) )


    return node


  def load_light(self, light):
    # TODO        
    print("load light" , light)        
    return "dummy"

  def load_scenegraph(self, scenegraph):
    # TODO        
    print("load scenegraph" , scenegraph)        


  def load_object(self, object):
    if (self.json_data["objects"][object]["type"] == "TriMeshGeometry"):
      self.load_TriMeshGeometry(object)
    
    if (self.json_data["objects"][object]["type"] == "PointLight"):
      self.load_PointLight(object)
      
    if (self.json_data["objects"][object]["type"] == "Empty"):
      self.load_TransformNode(object)

  def load_TransformNode(self, object):
    print "load Transformnode ", object
    translate = self.json_data["objects"][object]["position"]
    translate = avango.gua.Vec3(translate[0], translate[1], translate[2])
    
    quaternion = self.json_data["objects"][object]["quaternion"]
    quaternion = avango.gua.Quat(quaternion[0], quaternion[1], quaternion[2], quaternion[3])
    quaternion.normalize()
    
    scale = self.json_data["objects"][object]["scale"]
    scale = avango.gua.Vec3(scale[0], scale[1], scale[2])

    transformation = avango.gua.make_trans_mat(translate) \
             * avango.gua.make_rot_mat(quaternion) \
             * avango.gua.make_scale_mat(scale)

    node = avango.gua.nodes.TransformNode(Name = str(object))
    node.Transform.value = transformation

    self.root_node.Children.value.append(node)


  def load_PointLight(self, object):
    print "load light ", object
    translate = self.json_data["objects"][object]["position"] 
    translate = avango.gua.Vec3(translate[0], translate[1], -translate[2])

    scale = self.json_data["objects"][object]["distance"] * 2.0

    transformation = avango.gua.make_trans_mat(translate) \
             * avango.gua.make_scale_mat(scale)
    
    color_hexstring = str(hex(self.json_data["objects"][object]["color"]))
    red = float(int(color_hexstring[2]+color_hexstring[3],16)) /255
    green = float(int(color_hexstring[4]+color_hexstring[5],16)) /255
    blue = float(int(color_hexstring[6]+color_hexstring[7],16)) /255

    
    light = avango.gua.nodes.PointLightNode( Name = str(object)
                         , Color = avango.gua.Color(red, green, blue) )
    light.Transform.value = transformation
    light.EnableShadows.value = True

    self.root_node.Children.value.append(light)


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
