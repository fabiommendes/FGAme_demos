from FGAme import AABB
from FGAme.extra.tiles import TileObject 
from mario.constants import *  # @UnusedWildImport

class Bowser(AABB, TileObject):
    '''Representa o Bowser'''
    
    def __init__(self, coords=(0, 0), pos = (1200, 300), world=None):
    
        super().__init__(
            shape=(50,60), 
            restitution=0.0, 
            image='images/bowser1',
            image_reference='pos_sw',
            image_scale=SCALE,
            world=world,

        )
        self.tileinit(TILESIZE, coords=coords)
        if pos:
            self.pos = pos
        
        self.name = 'Bowser'
            

    def on_pre_collision(self, col):
        other = col.other(self)
        if other.name == 'platform':
            if other.pos.y > self.pos.y or col.normal.x != 0:
                col.cancel()

        
        if other.name == 'Mario':
            if other.pos.y > self.pos.y and other.vel.y > -30:
                #self.hide()
                self.pos=(0,0)
                
            
            
            
