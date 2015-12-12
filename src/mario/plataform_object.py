from FGAme.extra.tiles import TileObject 

from FGAme import AABB, listen

from mario.constants import *  # @UnusedWildImport

## PARA O POLIGONO K1 = self.K = A.mass
        ##self.A.force = lambda t: -K1 * (A.pos - (150,210)).normalized()


class Plataform(AABB, TileObject):
    '''Representa Plataforma'''
    
    def __init__(self, coords=(0, 0), pos=(500, 260), density=9999 , **kwargs):
    
        super().__init__(
            shape=(50, 10), 
            restitution=0, 
            image='images/cloud',
            image_reference='pos_sw',
            density=density,
            **kwargs
        )
        self.tileinit(TILESIZE, coords=coords)
        if pos:
            self.pos = pos
        
        self.num_coins = 0
        self.name = 'elevator'

    def on_pre_collision(self, col):
        other = col.other(self)
        if other.name == 'platform':
            if other.pos.y > self.pos.y or col.normal.x != 0:
                col.cancel()
            
        if other.name == 'coin':
            col.cancel()
            
        if other.name == 'Mario':
            if other.pos.y > self.pos.y:
                self.vel = other.vel.copy((other.vel.x)*0.90, y=CLOUD_SPEED)
            
            
            
