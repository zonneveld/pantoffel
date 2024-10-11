from pygame import sprite,image,transform
from random import Random

class Actor(sprite.Sprite):
    def __init__(self,imgpath,pos):
        super(Actor,self).__init__()
        self.image = image.load(imgpath).convert_alpha()
        self.base_image = self.image
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.angle = 0
    
    def move_hor(self,value):
        self.rect.x += value

    def move_ver(self,value):
        self.rect.y += value

    def update(self) :
        r = Random()
        self.angle += 1
        self.image = transform.rotozoom(self.base_image, self.angle,1)
        # self.image = transform.box_blur(self.base_image,self.angle)
        self.rect =  self.image.get_rect(center=self.rect.center)

        if r.randrange(0,10) == 1:
            self.rect.x += r.randrange(-1,2) * 0.2
            self.rect.y += r.randrange(-1,2) * 0.2
