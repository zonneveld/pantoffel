import platform
import pygame,sys
import gameobjects

Z_ENC1 = 2
Z_ENC2 = 3

X_ENC1 = 14
X_ENC2 = 15

Y_ENC1 = 23
Y_ENC2 = 24

# test..

x_pulse = 0
y_pulse = 0
z_pulse = 0

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

#linux:
from gpiozero import RotaryEncoder      
x_encoder = RotaryEncoder(X_ENC1,X_ENC2)
x_encoder.when_rotated_clockwise          = lambda : x_inc_ev(1)
x_encoder.when_rotated_counter_clockwise  = lambda : x_inc_ev(-1)

y_encoder = RotaryEncoder(Y_ENC1,Y_ENC2)
y_encoder.when_rotated_clockwise          = lambda : y_inc_ev(1)
y_encoder.when_rotated_counter_clockwise  = lambda : y_inc_ev(-1)

z_encoder = RotaryEncoder(Z_ENC1,Z_ENC2)
z_encoder.when_rotated_clockwise          = lambda : z_inc_ev(1)
z_encoder.when_rotated_counter_clockwise  = lambda : z_inc_ev(-1)



# elif platform.system() == 'Windows':
#    def system_start():
#       pass
#    def system_end():
#       pass
#    def screen_setup():
#       return pygame.display.set_mode([640, 640])


pygame.init()
screen = pygame.display.set_mode((0, 0),pygame.FULLSCREEN )
pygame.mouse.set_visible(False) 
pygame.display.set_caption("Hello World")

[w,h] = pygame.display.get_window_size()

clock = pygame.time.Clock()

actor=  gameobjects.Actor(r'arrow.png',(w/2,h/2))
actor2=  gameobjects.Actor(r'arrow.png',(w/2,h/2 + 50))

troepsound = pygame.mixer.Sound("troep.wav")


group = pygame.sprite.RenderPlain()
group.add(actor)
group.add(actor2)

running = True

while running:
   for event in pygame.event.get():
      if event.type == pygame.QUIT:
         running = False

   keys = pygame.key.get_pressed()
   if keys[pygame.K_ESCAPE]:
      running = False

   if keys[pygame.K_LEFT]:
      for _actor in group.sprites():
         _actor.move_hor(10)
   if keys[pygame.K_RIGHT]:
      for _actor in group.sprites():
         _actor.move_hor(-10)
   if keys[pygame.K_UP]:
      for _actor in group.sprites():
         _actor.move_ver(10)
   if keys[pygame.K_DOWN]:
      for _actor in group.sprites():
         _actor.move_ver(-10)
   if keys[pygame.K_SPACE]:
      if not pygame.mixer.get_busy():
         pygame.mixer.Sound.play(troepsound)
   if x_pulse != 0:
      actor.move_ver(x_pulse)
      x_pulse = 0
   if y_pulse != 0:
      actor.move_hor(y_pulse)
      y_pulse = 0

      # print(f'stepping: {z_pulse}')
      # 
      # z_pulse = 0


   group.update()
   screen.fill((0,0,0))
   # screen.convert_alpha()
   group.draw(screen)
   pygame.display.flip()
   clock.tick(30)

pygame.quit()
print("exit!")
