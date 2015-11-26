from FGAme.extra.orientation_objects import pos
from FGAme.objects import Circle, Poly, AABB
from FGAme.world import World
from FGAme.events.util import listen
from FGAme import draw
from FGAme.actions import *

class ElasticPong(World):

    def init(self):

        A = Circle(30, pos=(150, 210), color='red')
        B = AABB(100,150,100,300,color='black', mass='inf' )
        box = AABB(0,800,0,100, mass='inf', color = 'blue')
        self.A, self.B = A, B
        self.add(draw.Circle(500, color=(255, 255, 0)), layer=-1)
        self.line = draw.Segment((150, 210), (150, 210))
        self.add([A,B,box])
        self.add(self.line)
        
        K1 = self.K = A.mass
        self.A.force = lambda t: -K1 * (A.pos - (150,210))


        self.damping = 0.2
        self.modify_speed = False
        self.add_bounds(width = 5)
        
    @listen('long-press', 'right')
    def startingA(self):
        #canvas = Canvas
        #canvas.draw_segment(20, 'right')
        self.A.vel = (150,0)
    
    
    @listen('frame-enter')
    def update_line(self):
        self.line._end = self.A.pos
        
    @listen('mouse-button-down', 'left')
    def start_vel_line(self, pos):
        if hasattr(self, 'vel_line'):
            self.remove(self.vel_line)
        
        if abs(self.A.pos - pos) < self.A.radius:
            self.toggle_pause()
            self.vel_line = draw.Segment(pos, pos, color='red', linewidth=5)
            self.add(self.vel_line)
            self.modify_speed = True
            
            def func():
                if hasattr(self, 'vel_line'):
                    self.remove(self.vel_line)
            
            action = delay(1.5) >> call_function(func)
            action.start()
            
            
    @listen('mouse-long-press', 'left')
    def update_vel_line(self, pos):
        if self.modify_speed:
            self.vel_line._end = pos
        
    @listen('mouse-button-up', 'left')
    def destroy_vel_line(self, pos):
        if self.modify_speed:
            #self.remove(self.vel_line)
            self.A.vel =  2 * (self.vel_line.end - self.vel_line.start)
            self.toggle_pause()
            self.modify_speed = False

        
if __name__ == '__main__':
    world = ElasticPong()
    world.run()