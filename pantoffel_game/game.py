import platform

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

LASER = 18

# test..

x_pulse = 0
y_pulse = 0
z_pulse = 0

q_flag = False

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
   pass

x_encoder = None
y_encoder = None
z_encoder = None

laser_button = None

screen = None

lock_servo = None

media = "media/"

#linux:
if platform.system() == 'Linux':
   print("linux mode!")
   from gpiozero import RotaryEncoder, Button, Servo    
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
   laser_button.when_pressed = quit_ev

   media = "media\\"
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

camera_offset_x = 0
camera_offset_y = 0

map_size = (2000,2000)
game_map = Surface(map_size)
#  test bg
bg =pygame.image.load(f"{media}grid.jpg")
bg = pygame.transform.scale(bg,(map_size))
# 


clock = pygame.time.Clock()

actor=  gameobjects.Actor(f"{media}arrow.png",(10, 10))
actor2=  gameobjects.Actor(f"{media}arrow.png",(w/2,h/2 + 50))

troepsound = pygame.mixer.Sound(f"{media}/troep.wav")


group = Group()
group.add(actor)
group.add(actor2)

running = True

while running:
   if q_flag:
      running = False
   
   for event in pygame.event.get():
      if event.type == pygame.QUIT:
         running = False

   keys = pygame.key.get_pressed()
   if keys[pygame.K_ESCAPE]:
      quit_ev()

   if keys[pygame.K_RIGHT] or x_pulse > 0:
      x_pulse = 0
      if game_map.get_rect().contains(Rect(camera_offset_x + 10, camera_offset_y,w,h)):
         camera_offset_x += 10
   if keys[pygame.K_LEFT] or x_pulse < 0:
      x_pulse = 0
      if game_map.get_rect().contains(Rect(camera_offset_x - 10, camera_offset_y,w,h)):
         camera_offset_x -= 10
   if keys[pygame.K_DOWN] or y_pulse > 0:
      y_pulse = 0
      if game_map.get_rect().contains(Rect(camera_offset_x, camera_offset_y + 10,w,h)):
         camera_offset_y += 10
   if keys[pygame.K_UP] or y_pulse < 0:
      y_pulse = 0
      if game_map.get_rect().contains(Rect(camera_offset_x, camera_offset_y -10,w,h)):
         camera_offset_y -= 10

   if keys[pygame.K_a]:
      actor.move_hor(-1)
   if keys[pygame.K_d]:
      actor.move_hor(1)

   if keys[pygame.K_SPACE]:
      if not pygame.mixer.get_busy():
         pygame.mixer.Sound.play(troepsound)
   # if x_pulse != 0:
   #    actor.move_ver(x_pulse)
   #    x_pulse = 0
   # if y_pulse != 0:
   #    actor.move_hor(y_pulse)
   #    y_pulse = 0

      # print(f'stepping: {z_pulse}')
      # 
      # z_pulse = 0

   #update sprites 
   group.update() 

   game_map.fill((0,0,0))
   game_map.blit(bg,(0,0))
   # camera = pygame.surface()

   group.draw(game_map)
   camera = game_map.subsurface(Rect(camera_offset_x,camera_offset_y,w,h))

   screen.blit(camera)
   pygame.display.flip()
   clock.tick(30)

pygame.quit()
print("exit!")


#level 1
