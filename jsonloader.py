import avango
import avango.gua

import json

# json Loader Class
class jsonloader:

  def __init__(self):
    self.json_data = None
    self.root_node = None
    self.TriMeshLoader = avango.gua.nodes.TriMeshLoader()


  def load_json(self, path, root_node):
    json_file = open(path)
    self.json_data = json.load(json_file)
    self.root_node = root_node

    for object in self.json_data["objects"]:
      self.load_object(object)


  def load_object(self, object):
    if (self.json_data["objects"][object]["type"] == "TriMeshGeometry"):
      self.load_TriMeshGeometry(object)
    
    if (self.json_data["objects"][object]["type"] == "PointLight"):
      self.load_PointLight(object)


  def load_TriMeshGeometry(self, object):
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
    
    geometry = self.TriMeshLoader.create_geometry_from_file( str(object)
                                                           , str(self.json_data["objects"][object]["geometry"])
                                                           , str(self.json_data["objects"][object]["material"])
                                                           , avango.gua.LoaderFlags.DEFAULTS)
    geometry.Transform.value = transformation
    self.root_node.Children.value.append(geometry)


  def load_PointLight(self, object):
    translate = self.json_data["objects"][object]["position"] 
    translate = avango.gua.Vec3(translate[0], translate[1], translate[2])

    scale = self.json_data["objects"][object]["distance"]

    transformation = avango.gua.make_trans_mat(translate) \
                   * avango.gua.make_scale_mat(scale)
    
    color_hexstring = str(hex(self.json_data["objects"][object]["color"]))
    red = float(int(color_hexstring[2]+color_hexstring[3],16)) /255
    green = float(int(color_hexstring[4]+color_hexstring[5],16)) /255
    blue = float(int(color_hexstring[6]+color_hexstring[7],16)) /255

    
    light = avango.gua.nodes.PointLightNode( Name = str(object)
                                           , Color = avango.gua.Color(red, green, blue) )
    light.Transform.value = transformation

    self.root_node.Children.value.append(light)


  def load_and_set_PipelineOptions(self, pipe):
    # GENERAL
    pipe.EnablePreviewDisplay.value   = self.json_data["pipeline_options"]["enable_preview_display"]
    pipe.EnableFPSDisplay.value       = self.json_data["pipeline_options"]["enable_fps_display"]
    pipe.EnableRayDisplay.value       = self.json_data["pipeline_options"]["enable_ray_display"]
    pipe.EnableBBoxDisplay.value      = self.json_data["pipeline_options"]["enable_bbox_display"]
    pipe.EnableWireframe.value        = self.json_data["pipeline_options"]["enable_wire_frame"]
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
