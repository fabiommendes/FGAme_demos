from FGAme import AABB, listen
from FGAme.extra.tiles import TileObject 
from mario.constants import *  # @UnusedWildImport
from FGAme import camera

class Mario(AABB, TileObject):
    '''Representa o Mario'''
    
    def __init__(self, coords=(0, 0), pos = (100, 80), world=None):
    
        super().__init__(
            shape=(TILESIZE, TILESIZE), 
            restitution=0, 
            image='images/mario1',
            image_reference='pos_sw',
            image_scale=SCALE,
            world=world,

        )
        self.tileinit(TILESIZE, coords=coords)
        if pos:
            self.pos = pos
        
        self.num_coins = 0
        self.name = 'Mario'
            
    @listen('long-press', 'left', direction=-1)
    @listen('long-press', 'right', direction=1)
    def move_horizontally(self, direction=1):
        _, vy = self.vel
        self.vel = (HORIZONTAL_SPEED * direction, vy)

    @listen('key-up', 'left')
    @listen('key-up', 'right')
    def stop_horizontally(self, direction=1):
        _, vy = self.vel
        self.move(0, 1)
        if abs(vy) < 5: 
            self.vel = (0, vy)

    @listen('key-down', 'up')
    @listen('key-down', 'space')
    def jump(self):
        if abs(self.vel.y) < 5 or abs(self.vel.y-CLOUD_SPEED)<1:
            self.vel = self.vel.copy(y=JUMP_SPEED)
            
    def on_frame_enter(self):
        
        camera.xmin
        real_camera = camera._CachingProxy__data
        camera_xmin = -real_camera.displacement.x
        camera_xmax = camera_xmin + real_camera.width
        camera_ymin = -real_camera.displacement.y
        camera_ymax = camera_ymin + real_camera.height 
        
        if self.xmin <= camera_xmin + 20:
            self.pos_left = self.pos_left.copy(x=camera_xmin + 20) 
             
        if self.pos.x + 400 > camera_xmax:
            real_camera.panright(4)
        
        if self.pos.y + 300 > camera_ymax:
            real_camera.panup(4)
        
        if self.pos.y - 50 < camera_ymin:
            real_camera.pandown(8)

    def on_pre_collision(self, col):
        other = col.other(self)
        if other.name == 'platform':
            if other.pos.y > self.pos.y or col.normal.x != 0:
                col.cancel()
            
        if other.name == 'coin':
            col.cancel()
            other.hide()
            other.name = 'getted coin'
            self.num_coins += 1
        
        if other.name == 'getted coin':
            col.cancel()
        
        #if other.name == 'Boss':
        #    self._image_scale=self.image_scale/2
        #    self.shape=(TILESIZE/2, TILESIZE/2)
