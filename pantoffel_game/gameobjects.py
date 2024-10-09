from pygame import sprite,image
from random import Random

class Actor(sprite.Sprite):
    def __init__(self,imgpath,pos):
        super(Actor,self).__init__()
        self.image = image.load(imgpath)
        self.rect = self.image.get_rect()
        self.rect.center = pos
    
    def move_hor(self,value):
        self.rect.x += value

    def move_ver(self,value):
        self.rect.y += value

    def update(self) :
        r = Random()
        if r.randrange(0,10) == 1:
            self.rect.x += r.randrange(-3,3)
            self.rect.y += r.randrange(-3,3)
        # pass
        # return super().update(*args, **kwargs)
        # super().__init__(*groups)