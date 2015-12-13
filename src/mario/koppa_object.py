from FGAme import AABB
from FGAme.extra.tiles import TileObject 
from mario.constants import *  # @UnusedWildImport

class Koppa(AABB, TileObject):
    '''Representa o Bowser'''
    
    def __init__(self, coords=(0, 0), pos = (600, 90), world=None):
    
        super().__init__(
            shape=(TILESIZE, TILESIZE), 
            restitution=0.0,
            friction = 0, 
            image='images/monster1',
            image_reference='pos_sw',
            image_scale=SCALE*0.8,
            world=world,

        )
        self.tileinit(TILESIZE, coords=coords)
        self.vel = (-KOOPA_MOVE, 0)
        self.name = 'koppa'
        self.direction = 'back'
        if pos:
            self.pos = pos

    def on_pre_collision(self, col):
        other = col.other(self)

        if other.name != 'brick':
            self.vel = self.vel.copy(x=KOOPA_MOVE)
            
        if other.name == 'Mario':
            if other.pos.y > self.pos.y and other.vel.y < -50:
                #self.hide()
                self.pos = (0,0)
                
                
            
            
            
