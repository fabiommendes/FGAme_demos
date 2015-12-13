from FGAme import AABB, listen
from FGAme import camera
from FGAme.extra.tiles import TileObject 
from FGAme.objects import Circle

from mario.constants import *  # @UnusedWildImport


class Boss(Circle, TileObject):
    '''Representa o BOSS'''
    
    def __init__(self, coords=(0, 0), pos = (450, 320), world=None, **kwargs):
    
        super().__init__(
            restitution=0,
            radius = 10,
            image='images/angry-sun',
            image_reference='pos_sw',
            image_scale=SCALE,
            gravity = 0,
            mass = 930,       
            world=world,

        )
        self.tileinit(TILESIZE, coords=coords)
        if pos:
            self.pos = pos
        
        self.name = 'Boss'

            
    def on_pre_collision(self, col):
        other = col.other(self)
        if other.name != 'Mario' and other.name != 'brick' and other.name !="Bowser":
            col.cancel()
        
   
            
