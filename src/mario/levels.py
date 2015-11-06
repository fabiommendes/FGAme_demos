from FGAme import World, Color
from FGAme.extra.tiles import TileManager
from mario.constants import SCALE, TILESIZE, GRAVITY, FRICTION
from mario.mario_object import Mario 

class LevelBase(World):
    TILES = None 
    
    def __init__(self):
        super().__init__(friction=FRICTION)
    
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
            friction=0,
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
        
class Level1(LevelBase):
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
