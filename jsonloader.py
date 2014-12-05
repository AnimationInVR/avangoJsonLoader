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
    
    
    light = avango.gua.nodes.PointLightNode( Name = str(object)
                                           , Color = avango.gua.Color(1.0, 1.0, 1.0) )
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

    # BLOOM
    pipe.EnableBloom.value    = self.json_data["pipeline_options"]["bloom_settings"]["enable"]
    pipe.BloomRadius.value    = self.json_data["pipeline_options"]["bloom_settings"]["radius"]
    pipe.BloomThreshold.value = self.json_data["pipeline_options"]["bloom_settings"]["threshold"]
    pipe.BloomIntensity.value = self.json_data["pipeline_options"]["bloom_settings"]["intensity"]

    # SSAO
    pipe.EnableSsao.value    = self.json_data["pipeline_options"]["ssao_settings"]["enable"]
    pipe.SsaoRadius.value    = self.json_data["pipeline_options"]["ssao_settings"]["radius"]
    pipe.SsaoIntensity.value = self.json_data["pipeline_options"]["ssao_settings"]["intensity"]
    pipe.SsaoFalloff.value   = self.json_data["pipeline_options"]["ssao_settings"]["falloff"]
