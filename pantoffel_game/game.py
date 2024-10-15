import platform
import pygame,sys
import gameobjects

Z_ENC1 = 17
Z_ENC2 = 27

pulse_count = 0

on_device = False

if platform.system() == 'Linux':
   import RPi.GPIO as GPIO

   z_pulse = 0

   GPIO.setmode(GPIO.BCM) 
   def enc(channel):
      global pulse_count
      pulse_count += 1
      
   def z_encoder_event(channel):
      global z_pulse
      if GPIO.input(Z_ENC2):
         z_pulse += 1
      else:
         z_pulse -= 1
      

   def btn_test(channel):
      print(f'edge on:{channel}')

   def system_start():
      GPIO.setmode(GPIO.BCM)
      GPIO.setup(Z_ENC1, GPIO.IN)
      GPIO.setup(Z_ENC2, GPIO.IN)
      
      GPIO.add_event_detect(Z_ENC1,GPIO.RISING,z_encoder_event)
      # GPIO.setup(pinData['test'],GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
      # GPIO.add_event_detect(pinData['test'], GPIO.RISING, callback=enc)
      # GPIO.add_event_callback(pinData['test'],btn_test,GPIO.RISING)
      
      # GPIO.add_event_callback(4,)
      pass
   def screen_setup():
      return pygame.display.set_mode((0, 0),pygame.FULLSCREEN )      

   def system_end():
      GPIO.cleanup() 



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
   if z_pulse:
      print(f'stepping: {z_pulse}')
      actor.move_ver(z_pulse)
      z_pulse = 0


   group.update()
   screen.fill((0,0,0))
   # screen.convert_alpha()
   group.draw(screen)
   pygame.display.flip()
   clock.tick(30)

pygame.quit()
print("exit!")
system_end()