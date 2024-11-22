import platform
import math

from pygame.surface import Surface
from pygame.rect import Rect
from pygame.sprite import Sprite, Group


import pygame,sys
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

ESCAPE = 20

# test..
ACTOR_EVENT       = pygame.USEREVENT + 1
TIMER_LOCK_EVENT  = pygame.USEREVENT + 1


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
   z_pulse+=value
   print(f"z_pulse:{z_pulse}")

def quit_ev():
   global q_flag
   q_flag = True

def laser_event():
   global lock_servo,unlock_flag
   unlock_flag = True
   lock_servo.angle = SERVO_UNLOCK_ANGLE

def lock_event():
   global lock_servo
   lock_servo.angle = SERVO_LOCK_ANGLE

x_encoder = None
y_encoder = None
z_encoder = None

laser_button = None
escape_button = None

screen = None

lock_servo = None

media = "media/"

#linux:
if platform.system() == 'Linux':
   print("linux mode!")
   from gpiozero import RotaryEncoder, Button, AngularServo  
   x_encoder = RotaryEncoder(X_ENC1,X_ENC2)
   x_encoder.when_rotated_clockwise          = lambda : x_inc_ev(1)
   x_encoder.when_rotated_counter_clockwise  = lambda : x_inc_ev(-1)

   y_encoder = RotaryEncoder(Y_ENC1,Y_ENC2)
   y_encoder.when_rotated_clockwise          = lambda : y_inc_ev(1)
   y_encoder.when_rotated_counter_clockwise  = lambda : y_inc_ev(-1)

   z_encoder = RotaryEncoder(Z_ENC1,Z_ENC2)
   z_encoder.when_rotated_clockwise          = lambda : z_inc_ev(1)
   z_encoder.when_rotated_counter_clockwise  = lambda : z_inc_ev(-1)

   laser_button = Button(LASER, pull_up = True, bounce_time = 0.5)
   laser_button.when_pressed = laser_event
 
   escape_button = Button(ESCAPE, pull_up = True, bounce_time = 0.3)
   escape_button.when_pressed = quit_ev 

   lock_servo = AngularServo(SERVO, min_angle=SERVO_ANGLE_MIN, max_angle=SERVO_ANGLE_MAX)
   lock_servo.angle = SERVO_LOCK_ANGLE
   
   media = "media/"
   # lock_servo = Servo(SERVO,)

   screen = pygame.display.set_mode((0, 0),pygame.FULLSCREEN )
elif platform.system() == 'Windows':
   print("windows mode!")
   media = "media/"
   screen = pygame.display.set_mode((840, 620))

pygame.init()

pygame.mouse.set_visible(False) 
pygame.display.set_caption("Hello World")

[w,h] = pygame.display.get_window_size()





map_width = 2000
map_height = 2000

viewing_border_width = 200
viewing_border_height = 200

map_size = (map_width,map_height)
game_map = Surface(map_size)
camera_area = game_map.get_rect().inflate(-viewing_border_width,-viewing_border_height)

camera_offset_x = viewing_border_width
camera_offset_y = viewing_border_height

#  test bg
bg =pygame.image.load(f"{media}grid.jpg")
bg = pygame.transform.scale(bg,(map_size))
# 

clock = pygame.time.Clock()
# level 1:
def level1Content():
   rtnGroup = Group()
   arrow_img = pygame.image.load(f"{media}arrow.png")
   ball_img = pygame.image.load(f"{media}ball.png")
   # background objects:
   rtnGroup.add(gameobjects.TravelingActor(ball_img, (map_width /2 , map_height / 2),30,1))
   rtnGroup.add(gameobjects.Actor(arrow_img,(10,30)))
   rtnGroup.add(gameobjects.Actor(arrow_img,(200,200)))

   # forground obejects:
   # nothing!
   return rtnGroup

# level 2:
def level2Content():   
   rtnGroup = Group()
   return rtnGroup


# actor=  gameobjects.Actor(f"{media}arrow.png",(10, 10))
# actor2=  gameobjects.Actor(f"{media}arrow.png",(w/2,h/2 + 50))

troepsound = pygame.mixer.Sound(f"{media}/troep.wav")



group = level1Content()

running = True
lock = False

while running:
   if q_flag:
      running = False
   
   if unlock_flag:
      unlock_flag = False
      pygame.time.set_timer(TIMER_LOCK_EVENT,1000,1)
      # lock_event()

   for event in pygame.event.get():
      if event.type == pygame.QUIT:
         running = False
      elif event.type == ACTOR_EVENT:
         lock = True
      elif event.type == TIMER_LOCK_EVENT:
         lock_event()
         

   keys = pygame.key.get_pressed()
   if keys[pygame.K_ESCAPE]:
      quit_ev()

   if not lock:
      if keys[pygame.K_RIGHT] or x_pulse > 0:
         x_pulse = 0
         if camera_area.contains(Rect(camera_offset_x + 10, camera_offset_y,w,h)):
            camera_offset_x += 10
      if keys[pygame.K_LEFT] or x_pulse < 0:
         x_pulse = 0
         if camera_area.contains(Rect(camera_offset_x - 10, camera_offset_y,w,h)):
            camera_offset_x -= 10
      if keys[pygame.K_DOWN] or y_pulse > 0:
         y_pulse = 0
         if camera_area.contains(Rect(camera_offset_x, camera_offset_y + 10,w,h)):
            camera_offset_y += 10
      if keys[pygame.K_UP] or y_pulse < 0:
         y_pulse = 0
         if camera_area.contains(Rect(camera_offset_x, camera_offset_y -10,w,h)):
            camera_offset_y -= 10

   #update sprites 
   group.update() 
   for actor in group.sprites():
      actor.rect.x %= map_width
      actor.rect.y %= map_height

   game_map.fill((0,0,0))
   game_map.blit(bg,(0,0))
   # camera = pygame.surface()

   group.draw(game_map)
   camera = game_map.subsurface(Rect(camera_offset_x,camera_offset_y,w,h))

   screen.blit(camera,(0,0))
   pygame.display.flip()
   clock.tick(60)

pygame.quit()
print("exit!")


#level 1
