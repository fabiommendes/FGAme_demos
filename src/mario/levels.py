from FGAme import World, Color
from FGAme.extra.tiles import TileManager

from mario.bowser_object import Bowser
from mario.constants import SCALE, TILESIZE, GRAVITY, FRICTION
from mario.mario_object import Mario 
from mario.plataform_object import Plataform
from mario.boss_object import Boss
from mario.koppa_object import Koppa


class LevelBase(World):
    TILES = None 
    
    def __init__(self):
        super().__init__(friction=FRICTION)
    
    def init(self):
        self.gravity = GRAVITY
        
        self.bowser = Bowser(coords=(2, 2))
        self.plataform = Plataform(coords=(2, 2), gravity=GRAVITY/4)  
        self.boss = Boss(coords=(2, 2))
        self.boss.force = lambda t: -490000 * (self.boss.pos - (self.mario.pos)).normalized()
        self.mario = Mario(coords=(2, 2))
        self.koopa = Koppa(coords=(2, 2))
        
        self.add(self.mario)
        self.add(self.bowser)
        self.add(self.boss)
        self.add(self.plataform)
        self.add(self.koopa)
        self.create_tiles()
        self.background = Color(80, 220, 255)
        
        
        #self.A.force = lambda t: -self.A.mass * (self.A.pos - (self.mario.pos))

    def on_frame_enter(self):
        self.mario.on_frame_enter()

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
            'pipe', '%',
            image='images/pipe', 
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
    |   %                 C
    |  
    |  ===     D
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

