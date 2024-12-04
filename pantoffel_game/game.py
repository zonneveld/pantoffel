import platform
from os import listdir
from os.path import join
from pathlib import Path

from pygame.surface import Surface
from pygame.rect import Rect
from pygame.sprite import Group
from pygame.event import Event

import pygame

from events import *
from hardwarealocations import *

import gameobjects


BLUR_MAX = 100

x_pulse = 0
y_pulse = 0
z_pulse = BLUR_MAX

# unlock_flag = False

def x_inc_ev(value):
   global x_pulse
   x_pulse+=value
   print(f"x_pulse:{x_pulse}")

def y_inc_ev(value):
   global y_pulse
   y_pulse+=value
   print(f"y_pulse:{y_pulse}")

def z_inc_ev(value):
   global z_pulse
   if holding:
      z_pulse+=value
      print(f"z_pulse:{z_pulse}")
   if releasing:
      z_pulse -= value
      print(f"z_pulse:{z_pulse}")

def shoot_laser_ev(value):
   global laser_enabled
   print("laser pressed")
   if laser_enabled:
      pygame.event.post(Event(LASER_SHOT))
      laser_enabled = False

# 
servo_do = None

#
button_light_toggle = None

#
warning_light_a_do = None
warning_light_b_do = None


x_encoder = None
y_encoder = None
z_encoder = None

laser_button = None
laser_light = None
laser_warning_a = None
laser_warning_b = None

screen = None

lock_servo = None

media = "media/"

pygame.init()

#linux:
if platform.system() == 'Linux':
   print("linux mode!")
   from gpiozero import RotaryEncoder, Button, AngularServo, LED
   x_encoder = RotaryEncoder(X_ENC1,X_ENC2)
   
   x_encoder.when_rotated_clockwise          = lambda : x_inc_ev(1)
   x_encoder.when_rotated_counter_clockwise  = lambda : x_inc_ev(-1)

   y_encoder = RotaryEncoder(Y_ENC1,Y_ENC2)
   y_encoder.when_rotated_clockwise          = lambda : y_inc_ev(1)
   y_encoder.when_rotated_counter_clockwise  = lambda : y_inc_ev(-1)

   z_encoder = RotaryEncoder(Z_ENC1,Z_ENC2)
   z_encoder.when_rotated_clockwise          = lambda : z_inc_ev(1)
   z_encoder.when_rotated_counter_clockwise  = lambda : z_inc_ev(-1)

   laser_button = Button(LASER, pull_up = True, bounce_time = 0.3)
   laser_button.when_pressed                 = shoot_laser_ev

   laser_light = LED(LASER_WARNING_LIGHT)
   laser_light.on() #<-- pull up high side

   laser_warning_a = LED(WARNING_LIGHT_A)
   laser_warning_b = LED(WARNING_LIGHT_B)
 
   lock_servo = AngularServo(SERVO, min_angle=SERVO_ANGLE_MIN, max_angle=SERVO_ANGLE_MAX)
   lock_servo.angle = SERVO_LOCK_ANGLE

   def servo_do(angle):
       lock_servo.angle = angle
      
   def button_light_toggle():
      laser_light.toggle()

   def warning_light_a_do(v):
      laser_warning_a.on() if v else laser_warning_a.off()
   
   def warning_light_b_do(v):
      laser_warning_b.on() if v else laser_warning_b.off()

   #
   # lock_servo = Servo(SERVO,)

   screen = pygame.display.set_mode((0, 0),pygame.FULLSCREEN )
elif platform.system() == 'Windows':
   print("windows mode!")
   def servo_do(angle):
       print(f"servo to {angle}")
      
   def button_light_toggle():
      # laser_light.toggle()
      pass
      # print("toggling button light")

   def warning_light_a_do(v):
      pass
      # print("blip ")
      # laser_warning_a.on if v else laser_warning_a.off
   
   def warning_light_b_do(v):
      pass
      # laser_warning_b.on if v else laser_warning_b.off
   screen = pygame.display.set_mode((840, 620))



pygame.mouse.set_visible(False) 

[w,h] = pygame.display.get_window_size()

map_width = 2338
map_height = 1700

viewing_border_width = 200
viewing_border_height = 200

#the level size
map_size = (map_width,map_height)

#the map
game_map = Surface(map_size)

#what is visable
viewing_area = game_map.get_rect().inflate(-viewing_border_width,-viewing_border_height)

#what area is being showed
camera_rect = Rect(0,0,w,h)

#setting the camera in the middle
camera_rect.center = game_map.get_rect().center

clock = pygame.time.Clock()

class LevelContent():
   def __init__(self):
      # self.background_img = background_img
      # self.background_img = pygame.transform.scale(self.background_img,(size))
      self.background = None   
      self.group = Group()
      self.exit = None
      self.event_count = 0
      self.sounds =None
      self.exit_spawned = False
      # self.background_sound_channel = None
      self.background_sound = None

# level 1:
def level1Content():
   # rtnLevelContent = LevelContent(join('media' , 'lvl1' , ''),map_size)

   # images = os.
   img_location = join('media', 'lvl1' , 'images')
   images = {Path(x).stem: pygame.image.load(join(img_location, x )).convert_alpha() for x in listdir(img_location)}
   snd_location = join('media', 'lvl1' , 'sounds')
   sounds = {Path(x).stem: pygame.mixer.Sound(join(snd_location, x ))for x in listdir(snd_location)}
   
   #images:
   # arrow_img =       images["arrow"]
   # ball_img =        images["ball"]
   # star_img =        images["star"]
   # triangle_img =    images["triangle"]
   # cartman =         images["cartman"]
   # passief_1

   #sound
   # troep = sounds["troep"]

   rtnLevelContent = LevelContent()
   rtnLevelContent.sounds = sounds
   rtnLevelContent.background = pygame.transform.scale(images["achtergrond"],map_size)
   
   rtnLevelContent.background_sound = sounds["underwater"]


   # background objects:
   rtnLevelContent.group.add(gameobjects.TravelingActor(images["passief1"], (map_width /2 , map_height / 2),30,1))
   rtnLevelContent.group.add(gameobjects.TravelingActor(images["passief2"], (map_width /4 , map_height / 3),100,1))
   rtnLevelContent.group.add(gameobjects.TravelingActor(images["passief3"], (map_width /5 , map_height / 2),127,3))
   rtnLevelContent.group.add(gameobjects.TravelingActor(images["passief4"], (map_width /2 , map_height / 5),45 + 180,4))
   # rtnLevelContent.group.add(gameobjects.Actor(images[""],(200,200)))

   # actors:
   rtnLevelContent.group.add(gameobjects.EventfulActor(images["event1"],(1570,1200),sounds["politie"]))
   rtnLevelContent.group.add(gameobjects.EventfulActor(images["event4"],(609,1270),sounds["paranoide"]))
   rtnLevelContent.group.add(gameobjects.EventfulActor(images["event3"],(1299,450), sounds["beerdiertje"]))
   # rtnLevelContent.group.add(gameobjects.EventfulActor(images["event4"],(500,500),troep))

   rtnLevelContent.exit = gameobjects.ExitActor(images["event2"],(map_width /2 , map_height / 2),sounds["pantoffeldiertje"])

   # rtnLevelContent.background_sound.play()

   rtnLevelContent.event_count = 3

   # exit actor
   return rtnLevelContent

# level 2:
def level2Content():   
   img_location = join('media', 'lvl2' , 'images')
   images = {Path(x).stem: pygame.image.load(join(img_location, x )).convert_alpha() for x in listdir(img_location)}

   snd_location = join('media', 'lvl2' , 'sounds')
   sounds = {Path(x).stem: pygame.mixer.Sound(join(snd_location, x ))for x in listdir(snd_location)}
   troep = sounds["troep"]


   rtnLevelContent = LevelContent()

   rtnLevelContent.sounds = sounds
   rtnLevelContent.background_sound = sounds["space"]
   rtnLevelContent.background =  pygame.transform.scale(images["achtergrond"],map_size)
   rtnLevelContent.event_count = 3


   # background objects:
   rtnLevelContent.group.add(gameobjects.TravelingActor(images["passief1"], (map_width /2 , map_height / 2),30,1))
   rtnLevelContent.group.add(gameobjects.TravelingActor(images["passief2"], (map_width /4 , map_height / 3),100,1))
   rtnLevelContent.group.add(gameobjects.TravelingActor(images["passief3"], (map_width /5 , map_height / 2),127,3))
   rtnLevelContent.group.add(gameobjects.TravelingActor(images["passief4"], (map_width /2 , map_height / 5),45 + 180,4))

   #event actors:
   rtnLevelContent.group.add(gameobjects.EventfulActor(images["event1"],(1689, 1190),sounds["plankdeeltjes"]))
   rtnLevelContent.group.add(gameobjects.EventfulActor(images["event2"],(1809, 700),sounds["radikaal"]))
   rtnLevelContent.group.add(gameobjects.EventfulActor(images["event4"],(609, 1240),sounds["kerst"]))

   #exit actors:
   rtnLevelContent.exit = gameobjects.LaserExitActor(images["event3"],(map_width /2 , map_height / 2),sounds["outro"])

   # rtnLevelContent.event_count = 1

   return rtnLevelContent

# troepsound = pygame.mixer.Sound(f"{media}/troep.wav")

content = level1Content()



running = True
pausing = False  # <-- playing any event
holding = False  # <-  playing exit event
releasing = True #<-- ending exit event

laser_enabled = False
game_done = False
anger_effect = False

current_actor = None

yes_color = (0,255,0)
no_color = (255,0,0)

alpha_screen = Surface(pygame.display.get_window_size())
alpha_screen.fill((255,0,0))
alpha_screen.set_alpha(0)

croshair = None

flash_counter = 0
scale_counter = 0

background_sound_channel = pygame.mixer.Channel(2)


background_sound_channel.play(content.background_sound,-1)
background_sound_channel.set_volume(0.03)
pygame.mixer.Channel(0).play(content.sounds["intro"])
pygame.mixer.Channel(0).set_volume(0.5)


# content.background_sound.play(-1)

while running:
   for event in pygame.event.get():

      # if event.type == INTRO_EVENT_START:

      #quitting..
      if event.type == pygame.QUIT:
         running = False
      
      #event start
      elif event.type == ACTOR_EVENT_START:
         pausing = True
      
      #event end
      elif event.type == ACTOR_EVENT_END:
         pausing = False
         #current_actor.event_done = True
         if isinstance(current_actor,gameobjects.ExitActor):
            pygame.event.post(Event(EXIT_EVENT_START))
         if isinstance(current_actor,gameobjects.LaserExitActor):
            pygame.event.post(Event(START_LASER_EVENT))
      
      #next level start event
      elif event.type == EXIT_EVENT_START:
         holding = True
         z_pulse = 0
      
      #next level end event
      elif event.type == EXIT_EVENT_END:
         holding = False
         releasing = True
         content = level2Content()
         background_sound_channel.play(content.background_sound,-1)
         background_sound_channel.set_volume(0.01)
      
      #start end sequence event, lights and sounds..
      elif event.type == START_LASER_EVENT:
         print("laser event start")
         background_sound_channel.play(content.sounds["alarm"],-1)
         background_sound_channel.set_volume(0.01)
         pausing = True
         pygame.time.set_timer(TIMER_FLASH_EVENT,100)
         laser_enabled = True

      #flashing stuff
      elif event.type == TIMER_FLASH_EVENT:
         flash_counter %= 20
         if flash_counter == 10:
            # laser_warning_a.on()
            warning_light_a_do(True)
            button_light_toggle()
            # laser_light.toggle()
         else:
            warning_light_a_do(False)
         
         if flash_counter == 0:
            warning_light_b_do(True)
            button_light_toggle()
         else:
            warning_light_b_do(False)
         flash_counter+=1

      #laser shot, start to grow actor..
      elif event.type == LASER_SHOT:
         print("laser event shot")
         content.sounds["laser_attack"].play()
         current_actor.grow = True
         anger_effect = True

      #end laser sequence event
      elif event.type == END_LASER_EVENT:
         print("end laser event")
         pygame.event.post(Event(UNLOCK_EVENT))
      
      #unlock chest, wait a second.
      elif event.type == UNLOCK_EVENT:
         # unlock it and...
         # lock_servo.angle = SERVO_UNLOCK_ANGLE
         servo_do(SERVO_UNLOCK_ANGLE)
         pygame.time.set_timer(TIMER_LOCK_EVENT,1000,1)
      
      #reset lock after second
      elif event.type == TIMER_LOCK_EVENT:
         # lock it!
         servo_do(SERVO_LOCK_ANGLE)
         pygame.mixer.stop()
         laser_enabled = False
         pausing = True
         # running = False



   keys = pygame.key.get_pressed()
   if keys[pygame.K_ESCAPE]:
      pygame.event.post(Event(pygame.QUIT))
      # quit_ev()

   if holding:
      if keys[pygame.K_z]:
         z_pulse += 1
      if z_pulse > BLUR_MAX:
         z_pulse = BLUR_MAX
         pygame.event.post(Event(EXIT_EVENT_END))

   elif releasing:
      if keys[pygame.K_z]:
         z_pulse -= 1
      if z_pulse < 1:
         z_pulse = 1
         releasing = False
   elif pausing:
      # print("pause")
      if keys[pygame.K_SPACE]:
         shoot_laser_ev(True)
   
   elif not pausing:
      if keys[pygame.K_RIGHT] or x_pulse > 0:
         x_pulse = 0
         if viewing_area.contains(camera_rect.move(+10,0)):
            camera_rect.centerx += 10

      if keys[pygame.K_LEFT] or x_pulse < 0:
         x_pulse = 0
         if viewing_area.contains(camera_rect.move(-10,0)):
            camera_rect.centerx -= 10

      if keys[pygame.K_DOWN] or y_pulse > 0:
         y_pulse = 0
         if viewing_area.contains(camera_rect.move(0,+10)):
            camera_rect.centery += 10

      if keys[pygame.K_UP] or y_pulse < 0:
         y_pulse = 0
         if viewing_area.contains(camera_rect.move(0,-10)):
            camera_rect.centery -= 10

         
      if keys[pygame.K_p]:
         print(camera_rect.center)

   # all_events_done = all([e.event_done for e in content.group.sprites() if isinstance(e,gameobjects.EventfulActor)])

   if content.event_count == 0 and not content.exit_spawned:
      content.group.add(content.exit)
      content.exit_spawned = True
      print("added exit!")

   group = content.group

   group.update() 
   for actor in group.sprites():
      actor.rect.x %= map_width
      actor.rect.y %= map_height

   #set background
   game_map.fill((0,0,0))
   
   if not game_done:
      game_map.blit(content.background,(0,0))
      group.draw(game_map)
      camera_area = camera_rect
      croshair_area = Rect(0,0,200,200)
      croshair_area.center = camera_area.center
      any_check = False
      
      for actor in group.sprites():
         if croshair_area.collidepoint(actor.rect.center):
            any_check = True


            if isinstance(actor,gameobjects.EventfulActor) and not actor.event_done:
               content.event_count -= 1
               current_actor = actor
               current_actor.start_event()

            

      pygame.draw.rect(game_map,yes_color if any_check else no_color,croshair_area,3)
      camera =  pygame.transform.box_blur(game_map.subsurface(camera_area),z_pulse + 1,repeat_edge_pixels=False)  
      
      if anger_effect:
         alpha_screen.set_alpha(255/1000*current_actor.growstep)
      
      screen.blit(camera,(0,0))
      screen.blit(alpha_screen,(0,0))
      
      
   else:
      screen.blit(game_map,(0,0))
   pygame.display.flip()
   clock.tick(30)

pygame.quit()
print("exit!")


#level 1
