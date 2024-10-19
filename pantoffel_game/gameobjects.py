from pygame import sprite,image,transform
from random import Random

class Coordinate:
    def __init__(self,pos = (0,0)):
        (self.x,self.y) = pos
    
    def __add__(self, pos_to_add):
        return Coordinate((self.x + pos_to_add.x, self.y + pos_to_add.y))
    
    def __eq__(self,pos_to_check) -> bool:
        return (self.x == pos_to_check.x) and (self.y == pos_to_check.y)

    def get(self):
        return (self.x,self.y)

    # def 

class Actor(sprite.Sprite):
    def __init__(self,imgpath,pos):
        super(Actor,self).__init__()
        self.image = image.load(imgpath).convert_alpha()
        self.base_image = self.image
        self.rect = self.image.get_rect()
        # self.rect.center = pos
        self.float_ancor = Coordinate(pos)
        self.float_offset = Coordinate()
        self.float_target = Coordinate()
        self.float_speed = 1
        self.angle = 0
    
    def move_hor(self,value):
        self.float_ancor.x += value
        # self.rect.x += value

    def move_ver(self,value):
        self.float_ancor.y += value

    def float_step(self):
        return
        r = Random()
        if r.randrange(0,10) == 1:
            self.float_offset.x += r.randrange(-4,5) * 1
            self.float_offset.y += r.randrange(-4,5) * 1


    def update(self) :
        
        self.angle += 1
        self.float_step()
        postion = self.float_ancor + self.float_offset
        
        self.rect.x = postion.x
        self.rect.y = postion.y


