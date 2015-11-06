from FGAme import AABB, listen
from FGAme.extra.tiles import TileObject 
from mario.constants import *  # @UnusedWildImport

class Mario(AABB, TileObject):
    '''Representa o Mario'''
    
    def __init__(self, coords=(0, 0), pos=None, world=None):
        super().__init__(
            shape=(TILESIZE, TILESIZE), 
            restitution=0,
            image='images/mario1',
            image_reference='pos_sw',
            image_scale=SCALE,
            world=None,
        )
        self.tileinit(TILESIZE, coords=coords)
        if pos:
            self.pos = pos
            
    @listen('long-press', 'left', direction=-1)
    @listen('long-press', 'right', direction=1)
    def move_horizontally(self, direction=1):
        _, vy = self.vel
        self.vel = (HORIZONTAL_SPEED * direction, vy)

    @listen('key-up', 'left')
    @listen('key-up', 'right')
    def stop_horizontally(self, direction=1):
        _, vy = self.vel
        if abs(vy) < 5: 
            self.vel = (0, vy)

    @listen('key-down', 'up')
    @listen('key-down', 'space')
    def jump(self):
        if abs(self.vel.y) < 5:
            self.vel = self.vel.copy(y=JUMP_SPEED)

    def on_pre_collision(self, col):
        other = col.other(self)
        if other.name == 'platform':
            if other.pos.y > self.pos.y or col.normal.x != 0:
                col.cancel()
