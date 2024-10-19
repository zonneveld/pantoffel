import platform
import pygame,sys
import gameobjects

Z_ENC1 = 17
Z_ENC2 = 27

X_ENC1 = 17
X_ENC2 = 27

Y_ENC1 = 17
Y_ENC2 = 27

x_pulse = 0
y_pulse = 0
z_pulse = 0


on_device = False

if platform.system() == 'Linux':
   # import RPi.GPIO as GPIO #<-- vervangen met pizero!
   from gpiozero import RotaryEncoder      

   def x_inc_ev(value):
      global x_pulse
      x_pulse+=1

   def system_start():
      global x_pulse
      x_encoder = RotaryEncoder(X_ENC1,X_ENC2)
      x_encoder.when_rotated_clockwise          = lambda : x_inc_ev(1)
      x_encoder.when_rotated_counter_clockwise  = lambda : x_inc_ev(-1)
      

      y_encoder = RotaryEncoder(Y_ENC1,Y_ENC2)
      
      
      z_encoder = RotaryEncoder(Z_ENC1,Z_ENC2)
      
      pass
   def screen_setup():
      return pygame.display.set_mode((0, 0),pygame.FULLSCREEN )      

   def system_end():
      pass
      # GPIO.cleanup() 



elif platform.system() == 'Windows':
   def system_start():
      pass
   def system_end():
      pass
   def screen_setup():
      return pygame.display.set_mode([640, 640])




system_start()

pygame.init()

# screen = pygame.display.set_mode([640, 640])

screen = screen_setup()

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
system_end()