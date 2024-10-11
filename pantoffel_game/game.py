import pygame,sys
import gameobjects

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

while True:
   for event in pygame.event.get():
      if event.type == pygame.QUIT:
         pygame.quit()
         print("exit!")
         sys.exit()

   keys = pygame.key.get_pressed()
   if keys[pygame.K_ESCAPE]:
      pygame.quit()
      print("exit!")
      sys.exit()



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