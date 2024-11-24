import math

from pygame.event import Event
from pygame import USEREVENT
from pygame import sprite,mixer,event,transform
from random import Random

ACTOR_EVENT_START       = USEREVENT + 1
ACTOR_EVENT_END         = USEREVENT + 2
EXIT_EVENT_START        = USEREVENT + 3
EXIT_EVENT_END          = USEREVENT + 4

START_LASER_EVENT       = USEREVENT + 5
END_LASER_EVENT         = USEREVENT + 6


class Actor(sprite.Sprite):
    def __init__(self,mask,position):
        super(Actor,self).__init__()
        self.mask = mask.convert_alpha()
        self.image = self.mask.copy()
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
        self.event_done = False
        self.channel = mixer.Channel(0)
        self.grow = False
        self.growstep = 0
    

    def start_event(self):
        if self.event_done or self.channel.get_busy():
            return
        
        event.post(event.Event(ACTOR_EVENT_START))
        self.channel.set_endevent(ACTOR_EVENT_END)
        self.channel.play(self.soundbite)
        # self.scale(1.5)
        self.grow = True
        self.event_done = True



        # return super().update()

class ExitActor(EventfulActor):
    def __init__(self, mask, position, soundbite):
        super().__init__(mask, position, soundbite)
    
    def start_event(self):
        super().start_event()

class LaserExitActor(ExitActor):
    def start_event(self):
        if self.event_done:
            return
        self.event_done = True
        self.channel.play(self.soundbite)
        event.post(Event(START_LASER_EVENT))

    def update(self):
        if self.grow:
            if self.growstep > 100:
                event.post(Event())
                self.grow = False
            self.growstep+= 1
            or_x,or_y = self.mask.get_size()
            nw_x = or_x + round(self.growstep)
            nw_y = or_y + round(self.growstep)
            self.image = transform.smoothscale(self.mask,(nw_x,nw_y))
            self.rect = self.image.get_rect(center = self.rect.center)      

            
        else:
            super().update()


