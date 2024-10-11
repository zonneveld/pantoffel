import platform
import pygame,sys
import gameobjects

if platform.system() == 'Linux':
   import RPi.GPIO as GPIO
   
   pinData = {}
   pinData['test'] = 4

   GPIO.setmode(GPIO.BCM) 
   def btn_test(channel):
      print(f'edge on:{channel}')

   def system_start():
      GPIO.setmode(GPIO.BCM)
      GPIO.setup(pinData['test'],GPIO.IN)
      GPIO.add_event_detect(pinData['test'], GPIO.RISING, callback=btn_test, bouncetime=200)
      # GPIO.add_event_callback(pinData['test'],btn_test,GPIO.RISING)
      
      # GPIO.add_event_callback(4,)
      pass

   def system_end():
      GPIO.cleanup() 



elif platform.system() == 'Windows':
   def system_start():
      pass
   def system_end():
      pass



system_start()

pygame.init()

screen = pygame.display.set_mode([640, 640])
pygame.display.set_caption("Hello World")

clock = pygame.time.Clock()

actor=  gameobjects.Actor(r'arrow.png',(640/2,50))
actor2=  gameobjects.Actor(r'arrow.png',(640/2,100))

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
      # pass
      # for _actor in group.sprites():
      #    _actor.move_ver(-10)

   group.update()
   screen.fill((0,0,0))
   # screen.convert_alpha()
   group.draw(screen)
   pygame.display.flip()
   clock.tick(60)

pygame.quit()
print("exit!")
system_end()