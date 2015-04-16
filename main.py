#!/usr/bin/python

import sys

import avango
import avango.gua
import avango.script
from avango.script import field_has_changed

import examples_common.navigator
from examples_common.GuaVE import GuaVE
from examples_common import device

import jsonloader

from avango.gua.skelanim.CharacterControl import *
from avango.gua.skelanim.GroundFollowing import *
from avango.gua.skelanim.DistanceEvents import *

class Starter(avango.script.Script):

  def __init__(self):
    self.super(Starter).__init__()
    self.always_evaluate(True)

    self.KeyT = False

  def myConstructor(self, app):
    self.app = app
    self.keyboard = self.app.field_containers['keyboard']
    
  def evaluate(self):
    if self.keyboard.KeyT.value and not self.KeyT:
      self.app.start()
      # pass
    self.KeyT = self.keyboard.KeyT.value



def start():

  loader = jsonloader.jsonloader()
  app = loader.create_application_from_json(sys.argv[1])
  
  starter = Starter()
  starter.myConstructor(app)

  skel_loader = avango.gua.skelanim.nodes.SkeletalAnimationLoader()
  bob = app.field_containers["bob"]
  
  bob.load_animation("/opt/project_animation/Assets/UnrealTournament/UniversalAnimations/Idle_Ready_DPi.FBX", "idle")
  bob.load_animation("/opt/project_animation/Assets/UnrealTournament/UniversalAnimations/Run_Fwd_DPi.FBX", "run_fwd")
  bob.load_animation("/opt/project_animation/Assets/UnrealTournament/UniversalAnimations/Run_Fwd_DPi.FBX", "run_fwd_2")
  bob.load_animation("/opt/project_animation/Assets/UnrealTournament/UniversalAnimations/Run_Bwd_DPi.FBX", "run_bwd")
  bob.load_animation("/opt/project_animation/Assets/UnrealTournament/UniversalAnimations/Run_Bwd_DPi.FBX", "run_bwd_2")

  
  # RUN BOB RUN
  bob_nav = app.field_containers["bob_nav"]

  cc_run = CharacterControl(Name="bobs_cc")
  cc_run.my_constructor(bob, bob_nav, app.window)
  cc_run.activate_wall_detection(0.1, 0.2, "idle", app.scenegraph)
  
  # animation and move
  cc_run.on_key_down(87, "idle", AnimationConfig("run_fwd", speed=0.7))
  cc_run.on_key_up(87, "run_fwd", AnimationConfig("idle"))
  cc_run.bind_translation("run_fwd",avango.gua.Vec3(0.01,0.0,0.0))

  cc_run.on_key_down(83, "idle", AnimationConfig("run_bwd", speed=0.7))
  cc_run.on_key_up(83, "run_bwd", AnimationConfig("idle"))
  cc_run.bind_translation("run_bwd",avango.gua.Vec3(-0.01,0.0,0.0))


  # just animation
  cc_run.on_key_down(69, "idle", AnimationConfig("run_fwd_2", speed=0.7))
  cc_run.on_key_up(69, "run_fwd_2", AnimationConfig("idle"))
  
  cc_run.on_key_down(68, "idle", AnimationConfig("run_bwd_2", speed=0.7))
  cc_run.on_key_up(68, "run_bwd_2", AnimationConfig("idle"))

  # ground following
  bob_ground = app.field_containers["bob_ground"]
  ground_following = GroundFollowing(
    Name = "gf",
    SceneGraph = app.scenegraph,
    OffsetToGround = 0.2,
    MaxDistanceToGround = 5.0
  )
  ground_following.InTransform.connect_from(bob.WorldTransform)
  bob_ground.Transform.connect_from(ground_following.OutTransform)
  app.add_field_container(cc_run)
  app.add_field_container(ground_following)

  # FALL DOWN BOB
  action_bob = app.field_containers["action_bob"]
  
  action_bob.load_animation("/opt/project_animation/Assets/UnrealTournament/UniversalAnimations/Idle_Ready_DPi.FBX", "idle")
  action_bob.load_animation("/opt/project_animation/Assets/UnrealTournament/UniversalAnimations/Jump_Idle_DPi_Loop.FBX", "jump_loop")
  action_bob.load_animation("/opt/project_animation/Assets/UnrealTournament/UniversalAnimations/Jump_Idle_DPi_PreLand.FBX", "jump_preland")
  action_bob.load_animation("/opt/project_animation/Assets/UnrealTournament/UniversalAnimations/Jump_Idle_DPi_Land.FBX", "jump_land")
  
  cc_fall = CharacterControl(Name="action_bobs_cc")
  cc_fall.my_constructor(action_bob, action_bob, app.window)

  # cc_fall.on_animation_end("jump_land",AnimationConfig("idle"))
  
  ground_following = GroundFollowing(
    Name = "gf_action",
    SceneGraph = app.scenegraph,
    OffsetToGround = 0.2,
    MaxDistanceToGround = 5.0
  )
  ground_following.InTransform.connect_from(action_bob.WorldTransform)

  distance_events = DistanceEvents()
  distance_events.my_constructor(cc_fall)
  distance_events.DistanceToGround.connect_from(ground_following.DistanceToGround)
  distance_events.bigger_than(0.35, "idle", AnimationConfig("jump_loop", True), 0.0)
  distance_events.bigger_than(0.35, "jump_land", AnimationConfig("jump_loop", True), 0.0)
  distance_events.smaller_than(0.35, "jump_loop", AnimationConfig("jump_preland", False), 0.2)
  distance_events.smaller_than(0.2, "jump_preland", AnimationConfig("jump_land", False), 0.2)
  app.add_field_container(cc_fall)
  app.add_field_container(ground_following)

  # Bob loop
  bob_loop = app.field_containers["bob_loop_m"]

  bob_loop.load_animation("/opt/project_animation/Assets/UnrealTournament/UniversalAnimations/Idle_Ready_DPi.FBX", "idle")
  bob_loop.load_animation("/opt/project_animation/Assets/UnrealTournament/UniversalAnimations/Idle_Ready_DPi.FBX", "idle2")
  bob_loop.load_animation("/opt/project_animation/Assets/UnrealTournament/UniversalAnimations/Run_Fwd_DPi.FBX", "run")
  bob_loop.load_animation("/opt/project_animation/Assets/UnrealTournament/UniversalAnimations/Run_Fwd_DPi.FBX", "run2")

  cc_bob_loop = CharacterControl(Name="cc_bob_loop")
  cc_bob_loop.my_constructor(bob_loop, bob_loop, app.window)

  cc_bob_loop.on_animation_end("idle", AnimationConfig("run", False, duration=3.0), 0.2)
  cc_bob_loop.on_animation_end("run", AnimationConfig("idle2", True, duration=1.0), 0.2)
  cc_bob_loop.on_animation_end("idle2", AnimationConfig("run2", True, duration=3.0), 0.2)
  cc_bob_loop.on_animation_end("run2", AnimationConfig("idle", True, duration=1.0), 0.2)

  cc_bob_loop.blend_animation(AnimationConfig("idle", False))

  app.add_field_container(cc_bob_loop)


  # Bob speed
  bob_speed = app.field_containers["bob_speed_m"]

  bob_speed.load_animation("/opt/project_animation/Assets/UnrealTournament/UniversalAnimations/Idle_Ready_DPi.FBX", "idle")
  bob_speed.load_animation("/opt/project_animation/Assets/UnrealTournament/UniversalAnimations/Idle_Ready_DPi.FBX", "idle2")
  bob_speed.load_animation("/opt/project_animation/Assets/UnrealTournament/UniversalAnimations/Run_Fwd_DPi.FBX", "run")
  bob_speed.load_animation("/opt/project_animation/Assets/UnrealTournament/UniversalAnimations/Run_Fwd_DPi.FBX", "run2")

  cc_bob_speed = CharacterControl(Name="cc_bob_speed")
  cc_bob_speed.my_constructor(bob_speed, bob_speed, app.window)

  cc_bob_speed.on_animation_end("idle", AnimationConfig("run", True, speed=0.5 ,duration=3.0), 0.2)
  cc_bob_speed.on_animation_end("run", AnimationConfig("idle2", True, duration=1.0), 0.2)
  cc_bob_speed.on_animation_end("idle2", AnimationConfig("run2", True, speed=1.5 ,duration=3.0), 0.2)
  cc_bob_speed.on_animation_end("run2", AnimationConfig("idle", True, duration=1.0), 0.2)

  cc_bob_speed.blend_animation(AnimationConfig("idle", False))

  app.add_field_container(cc_bob_speed)


  # Bob duration
  bob_duration = app.field_containers["bob_duration_m"]

  bob_duration.load_animation("/opt/project_animation/Assets/UnrealTournament/UniversalAnimations/Idle_Ready_DPi.FBX", "idle")
  bob_duration.load_animation("/opt/project_animation/Assets/UnrealTournament/UniversalAnimations/Idle_Ready_DPi.FBX", "idle2")
  bob_duration.load_animation("/opt/project_animation/Assets/UnrealTournament/UniversalAnimations/Run_Fwd_DPi.FBX", "run")
  bob_duration.load_animation("/opt/project_animation/Assets/UnrealTournament/UniversalAnimations/Run_Fwd_DPi.FBX", "run2")

  cc_bob_duration = CharacterControl(Name="cc_bob_duration")
  cc_bob_duration.my_constructor(bob_duration, bob_duration, app.window)

  cc_bob_duration.on_animation_end("idle", AnimationConfig("run", True, duration=2.0), 0.2)
  cc_bob_duration.on_animation_end("run", AnimationConfig("idle2", True, duration=1.0), 0.2)
  cc_bob_duration.on_animation_end("idle2", AnimationConfig("run2", True, duration=4.0), 0.2)
  cc_bob_duration.on_animation_end("run2", AnimationConfig("idle", True, duration=1.0), 0.2)

  cc_bob_duration.blend_animation(AnimationConfig("idle", False))

  app.add_field_container(cc_bob_duration)


  app.run()


if __name__ == '__main__':
  start()

