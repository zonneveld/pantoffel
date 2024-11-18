import math

from pygame import sprite,image,transform
from random import Random


# class Coordinate:
#     def __init__(self,pos = (0,0)):
#         (self.x,self.y) = pos
    
#     def __add__(self, pos_to_add):
#         return Coordinate((self.x + pos_to_add.x, self.y + pos_to_add.y))
    
#     def __eq__(self,pos_to_check) -> bool:
#         return (self.x == pos_to_check.x) and (self.y == pos_to_check.y)

#     def get(self):
#         return (self.x,self.y)
#     # def 

class Actor(sprite.Sprite):
    def __init__(self,mask,position):
        super(Actor,self).__init__()
        self.mask = mask
        self.image = self.mask.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = position


class PassiveActor(Actor):
    def __init__(self, mask, position):
        super().__init__(mask, position)

class FloatingActor(PassiveActor):
    def __init__(self, mask, position,range,speed):
        super().__init__(mask, position)
        self.range = range
        self.speed = speed
        (self.position_x,self.position_y) = position
        self.anchor_point = position
        self.target = self.pick_target()
    
    def pick_target(self):
        pass

    def update(self):
        (target_x,target_y) = self.target
        if (self.position_x, self.position_y) == self.target:
            self.target = self.pick_target()
        # if 
        self.rect.x = self.position_x
        self.rect.y = self.position_y


class TravelingActor(PassiveActor):
    def __init__(self, mask, position,direction, speed):
        super().__init__(mask, position)
        rad = math.radians(direction)
        self.delta = (speed *math.cos(rad),speed *math.sin(rad))
        (self.position_x,self.position_y) = position
    
    def update(self):
        (x_step,y_step) = self.delta
        self.position_x += x_step
        self.position_y += y_step
        self.rect.x = self.position_x
        self.rect.y = self.position_y
        


class EventfulActor(Actor):
    def __init__(self, mask, position,soundbite):
        super().__init__(mask, position)
        self.soundbite = soundbite
    
    def event(self):
        pass

# class Actor(sprite.Sprite):
#     def __init__(self,imgpath,pos):
#         super(Actor,self).__init__()
#         self.image = image.load(imgpath).convert_alpha()
#         self.base_image = self.image
#         self.rect = self.image.get_rect()
#         # self.rect.center = pos
#         self.float_ancor = Coordinate(pos)
#         self.float_offset = Coordinate()
#         self.float_target = Coordinate()
#         self.float_speed = 1
#         self.angle = 0
    
#     def move_hor(self,value):
#         self.float_ancor.x += value
#         # self.rect.x += value

#     def move_ver(self,value):
#         self.float_ancor.y += value

#     def float_step(self):
#         return
#         r = Random()
#         if r.randrange(0,10) == 1:
#             self.float_offset.x += r.randrange(-4,5) * 1
#             self.float_offset.y += r.randrange(-4,5) * 1


#     def update(self) :
        
#         self.angle += 1
#         self.float_step()
#         postion = self.float_ancor + self.float_offset
        
#         self.rect.x = postion.x
#         self.rect.y = postion.y


