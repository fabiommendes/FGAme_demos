from FGAme import *  # @UnusedWildImport
from FGAme.actions import *  # @UnusedWildImport
from FGAme.extra.tiles import TileObject, TileManager

SCALE = 2
GRAVITY = SCALE * 600
HORIZONTAL_SPEED = SCALE * 100
JUMP_SPEED = SCALE * 220
TILESIZE = 16 * SCALE

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


class Level(World):
    TILES = '''
    |                    C
    |
    |         D
    |                  C
    |                            D
    |    C                                                    D
    |            oo
    |        oo     ===============            D
    |           ===
    |       ===
    |                B                       ii
    |xxxxxxxxxxxxxxxxxxxxxxxxxxxxx    xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    |XXXXXXXXXXXXXXXXXXXXXXXXXXXXXiiiiXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
    '''
    
    def init(self):
        self.gravity = GRAVITY
        self.mario = Mario(coords=(2, 2))
        self.add(self.mario)
        self.create_tiles()
        self.background = Color(80, 220, 255)

    def create_tiles(self):
        self.tilemanager = tm = TileManager((TILESIZE, TILESIZE))
        
        tm.register_spec(
            'brick', 'x', 
            image='images/brick1', 
            image_scale=SCALE,
        )
        tm.register_spec(
            'underbrick', 'X', 
            image='images/brick3', 
            image_scale=SCALE,
        )
        tm.register_spec(
            'platform', '=', 
            image='images/platform-air', 
            image_scale=SCALE,
        )
        tm.register_spec(
            'coin', 'o', 
            shape='circle', 
            image='images/coin4',
            image_scale=SCALE,
        )
        tm.register_spec(
            'flower', 'i',
            image='images/flower1',
            image_scale=SCALE,
        )
        tm.register_spec(
            'cloud-small', 'C',
            image='images/cloud',
            image_scale=SCALE,
            layer=-1,
            physics=False,
        )
        tm.register_spec(
            'cloud-big', 'D',
            image='images/doubleclouds',
            image_scale=SCALE,
            physics=False,
        )
        tm.register_spec(
            'cloud-big', 'B',
            image='images/bush-1',
            image_scale=SCALE,
            physics=False,
        )
        
        tm.add_tilemap(self.TILES)
        self.add(tm)


if __name__ == '__main__':
    world = Level()
    world.run()
