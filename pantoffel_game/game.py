import platform


from pygame.surface import Surface
from pygame.rect import Rect
from pygame.sprite import Group
from pygame.event import Event

import pygame

from gameobjects import ACTOR_EVENT_START,ACTOR_EVENT_END,EXIT_EVENT_END,EXIT_EVENT_START,START_LASER_EVENT
import gameobjects

Z_ENC1 = 9
Z_ENC2 = 11

X_ENC1 = 4
X_ENC2 = 17

Y_ENC1 = 22
Y_ENC2 = 23

SERVO = 24
SERVO_ANGLE_MIN = -90
SERVO_ANGLE_MAX = 90

SERVO_LOCK_ANGLE     = SERVO_ANGLE_MAX
SERVO_UNLOCK_ANGLE   = SERVO_ANGLE_MIN

LASER = 18

LASER_WARNING_LIGHT = 27
WARNING_LIGHT_A = 20
WARNING_LIGHT_B = 13

# ESCAPE = /

BLUR_MAX = 100

# test..

LASER_SEQUENCE    = pygame.USEREVENT+ 12
TIMER_FLASH_EVENT =pygame.USEREVENT + 11

UNLOCK_EVENT      = pygame.USEREVENT + 13
TIMER_LOCK_EVENT  = pygame.USEREVENT + 10


LASER_SHOT        = pygame.USEREVENT + 15

SCALE_LASER_TIMER = pygame.USEREVENT + 16

x_pulse = 0
y_pulse = 0
z_pulse = 0

q_flag = False
unlock_flag = False



on_device = False

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
   if laser_enabled:
      pygame.event.post(Event(LASER_SHOT))

def quit_ev():
   global q_flag
   q_flag = True

# def laser_event():
#    global lock_servo,unlock_flag
#    unlock_flag = True
#    lock_servo.angle = SERVO_UNLOCK_ANGLE

# def lock_event():
#    global lock_servo
#    lock_servo.angle = SERVO_LOCK_ANGLE

x_encoder = None
y_encoder = None
z_encoder = None

laser_button = None
laser_light = None
laser_warning_a = None
laser_warning_b = None

escape_button = None

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

   media = "media/"
   # lock_servo = Servo(SERVO,)

   screen = pygame.display.set_mode((0, 0),pygame.FULLSCREEN )
elif platform.system() == 'Windows':
   print("windows mode!")
   media = "media/"
   screen = pygame.display.set_mode((840, 620))



pygame.mouse.set_visible(False) 
pygame.display.set_caption("Hello World")

[w,h] = pygame.display.get_window_size()

map_width = 2000
map_height = 2000

viewing_border_width = 200
viewing_border_height = 200

map_size = (map_width,map_height)
game_map = Surface(map_size)
viewing_area = game_map.get_rect().inflate(-viewing_border_width,-viewing_border_height)

camera_offset_x = viewing_border_width
camera_offset_y = viewing_border_height

background_img = None

clock = pygame.time.Clock()

class LevelContent():
   def __init__(self,background_img_uri,size) -> None:
      self.background_img = pygame.image.load(f"{media}{background_img_uri}").convert_alpha()
      self.background_img = pygame.transform.scale(self.background_img,(size))
      
      self.group = Group()
      self.exit = None

# level 1:
def level1Content():
   rtnLevelContent = LevelContent("grid.jpg",map_size)

   #images:
   arrow_img =       pygame.image.load(f"{media}arrow.png").convert_alpha()
   ball_img =        pygame.image.load(f"{media}ball.png").convert_alpha()
   star_img =        pygame.image.load(f"{media}star.png").convert_alpha()
   triangle_img =    pygame.image.load(f"{media}triangle.png").convert_alpha()
   cartman =         pygame.image.load(f"{media}cartman.svg").convert_alpha()

   #sound
   troep = pygame.mixer.Sound(f"{media}troep.wav")

   # background objects:
   rtnLevelContent.group.add(gameobjects.TravelingActor(ball_img, (map_width /2 , map_height / 2),30,1))
   rtnLevelContent.group.add(gameobjects.Actor(arrow_img,(200,200)))
   rtnLevelContent.group.add(gameobjects.Actor(arrow_img,(300,300)))

   # actors:
   rtnLevelContent.group.add(gameobjects.EventfulActor(star_img,(400,1500),troep))
   rtnLevelContent.group.add(gameobjects.EventfulActor(star_img,(800,800),troep))

   rtnLevelContent.group.add(gameobjects.LaserExitActor(cartman,(1500,1500),troep))


   # exit actor
   rtnLevelContent.exit = gameobjects.ExitActor(triangle_img,(map_width /2 , map_height / 2),troep)
   return rtnLevelContent

# level 2:
def level2Content():   
   rtnLevelContent = LevelContent("grid_2.jpg",map_size)
   arrow_img = pygame.image.load(f"{media}arrow.png")
   ball_img = pygame.image.load(f"{media}ball.png")
   triangle_img = pygame.image.load(f"{media}triangle.png")
   star_img = pygame.image.load(f"{media}star.png")

   troep = pygame.mixer.Sound(f"{media}troep.wav")
   
   rtnLevelContent.group.add(gameobjects.TravelingActor(ball_img, (300 , 300),60,5))
   rtnLevelContent.group.add(gameobjects.Actor(arrow_img,(200,200)))
   rtnLevelContent.group.add(gameobjects.Actor(arrow_img,(300,300)))

   rtnLevelContent.group.add(gameobjects.EventfulActor(star_img,(400,1500),troep))

   rtnLevelContent.exit = gameobjects.ExitActor(triangle_img,(map_width /2 , map_height / 2),troep)
   return rtnLevelContent

# troepsound = pygame.mixer.Sound(f"{media}/troep.wav")

content = level1Content()



running = True
pausing = False # <-- playing any event
holding = False # <-  playing exit event
releasing = False
laser_enabled = False

current_actor = None

yes_color = (0,255,0)
no_color = (255,0,0)

croshair = Rect()

flash_counter = 0
scale_counter = 0


while running:
   if q_flag:
      running = False 

   if unlock_flag:
      unlock_flag = False
      pygame.time.set_timer(TIMER_LOCK_EVENT,1000,1)

   for event in pygame.event.get():

      if event.type == pygame.QUIT:
         running = False
      elif event.type == ACTOR_EVENT_START:
         pausing = True
      elif event.type == ACTOR_EVENT_END:
         pausing = False
         current_actor.event_done = True
         if isinstance(current_actor,gameobjects.ExitActor):
            pygame.event.post(Event(EXIT_EVENT_START))
      elif event.type == EXIT_EVENT_START:
         holding = True
         z_pulse = 0
      elif event.type == EXIT_EVENT_END:
         holding = False
         releasing = True
         content = level2Content()
      
      elif event.type == START_LASER_EVENT:
         print("laser event start")
         pygame.time.set_timer(TIMER_FLASH_EVENT,100)
         laser_enabled = True

      elif event.type == TIMER_FLASH_EVENT:
         flash_counter %= 20
         if flash_counter == 10:
            laser_warning_a.on()
            laser_light.toggle()
         else:
            laser_warning_a.off()
         
         if flash_counter == 0:
            laser_warning_b.on()
            laser_light.toggle()
         else:
            laser_warning_b.off()
         flash_counter+=1

      elif event.type == LASER_SHOT:
         print("laser event shot")
         pygame.time.set_timer(SCALE_LASER_TIMER,100)
      
      elif event.type == SCALE_LASER_TIMER:
         scale_counter += 1
         current_actor.scale(1+ (1/30 *scale_counter))
         print(f"scale step = {scale_counter}")
         if scale_counter > 30:
            pygame.time.set_timer(SCALE_LASER_TIMER,0)
            pygame.time.set_timer(TIMER_FLASH_EVENT,0)
            print("done scaling!")
            pygame.event.post(UNLOCK_EVENT)
      
      elif event.type == UNLOCK_EVENT:
         # unlock it and...
         lock_servo.angle = SERVO_UNLOCK_ANGLE
         pygame.time.set_timer(TIMER_LOCK_EVENT,1000,1)
      elif event.type == TIMER_LOCK_EVENT:
         # lock it!
         lock_servo.angle = SERVO_LOCK_ANGLE



   keys = pygame.key.get_pressed()
   if keys[pygame.K_ESCAPE]:
      quit_ev()

   if holding:
      if keys[pygame.K_z]:
         z_pulse += 1
         # print(z_pulse)
      if z_pulse > BLUR_MAX:
         z_pulse = BLUR_MAX
         pygame.event.post(Event(EXIT_EVENT_END))

   elif releasing:
      if keys[pygame.K_z]:
         z_pulse -= 1
         # print(z_pulse)
      if z_pulse < 1:
         z_pulse = 1
         releasing = False

   elif not pausing:
      if keys[pygame.K_RIGHT] or x_pulse > 0:
         x_pulse = 0
         if viewing_area.contains(Rect(camera_offset_x + 10, camera_offset_y,w,h)):
            camera_offset_x += 10
      if keys[pygame.K_LEFT] or x_pulse < 0:
         x_pulse = 0
         if viewing_area.contains(Rect(camera_offset_x - 10, camera_offset_y,w,h)):
            camera_offset_x -= 10
      if keys[pygame.K_DOWN] or y_pulse > 0:
         y_pulse = 0
         if viewing_area.contains(Rect(camera_offset_x, camera_offset_y + 10,w,h)):
            camera_offset_y += 10
      if keys[pygame.K_UP] or y_pulse < 0:
         y_pulse = 0
         if viewing_area.contains(Rect(camera_offset_x, camera_offset_y -10,w,h)):
            camera_offset_y -= 10
         

   all_events_done = all([e.event_done for e in content.group.sprites() if isinstance(e,gameobjects.EventfulActor)])
   if all_events_done and not any(isinstance(actor, gameobjects.ExitActor) for actor in content.group.sprites()):
      content.group.add(content.exit)
      print("added exit!")

   group = content.group

   group.update() 
   for actor in group.sprites():
      actor.rect.x %= map_width
      actor.rect.y %= map_height

   #set background
   game_map.fill((0,0,0))
   game_map.blit(content.background_img,(0,0))

   group.draw(game_map)
   camera_area =Rect(camera_offset_x,camera_offset_y,w,h)
   croshair_area = Rect(200,200,400,400)
   croshair_area.center = camera_area.center
   any_check = False
   
   for actor in group.sprites():
      if croshair_area.contains(actor.rect):
         any_check = True
         
         if isinstance(actor,gameobjects.LaserExitActor):
            current_actor = actor
            current_actor.start_event()
            
         
         elif isinstance(actor,gameobjects.EventfulActor):
            current_actor = actor
            current_actor.start_event()
         

   pygame.draw.rect(game_map,yes_color if any_check else no_color,croshair_area,3)
   camera =  pygame.transform.box_blur(game_map.subsurface(camera_area),z_pulse + 1,repeat_edge_pixels=False)  
   # effect_camera = camera.copy()
   # camera = pygame.transform.box_blur(camera,z_pulse + 1,repeat_edge_pixels=False)
   screen.blit(camera,(0,0))
   pygame.display.flip()
   clock.tick(60)

pygame.quit()
print("exit!")


#level 1
