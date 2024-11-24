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
        self.event_done = False
        self.channel = mixer.Channel(0)
    

    def start_event(self):
        if self.event_done or self.channel.get_busy():
            return
        
        event.post(event.Event(ACTOR_EVENT_START))
        self.channel.set_endevent(ACTOR_EVENT_END)
        self.channel.play(self.soundbite)
        self.event_done = True

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
        event.post(Event(START_LASER_EVENT))


    def scale(self):
        center = self.rect.center
        self.image = transform.scale_by(self.image,1.5) 
        self.rect.center = center