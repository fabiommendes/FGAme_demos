'''
Uma versão do clássico de Atari PONG.
'''

from FGAme import *
from FGAme.physics import Body
from FGAme.draw import Drawable


LIMIT_COLOR = 'white'
PADDLE_HEIGHT = 100
PADDLE_WIDTH = 20
PADDLE_COLOR = 'green'
BALL_RADIUS = 15
BALL_COLOR = 'red'
BALL_SPEED_CHANGE = 5
PADDLE_STEP = 5
LIFE_COLOR = '#999'


class Pong(World):
    def init(self):
        self.background = Color('#000')
        
        # Limites
        self.upper_limit = AABB(-500, 800 + 500, 590, 650, mass='inf', color=LIMIT_COLOR)
        self.lower_limit = AABB(-500, 800 + 500, -50, 10, mass='inf', color=LIMIT_COLOR)
        
        # Linhas
        self.add(draw.AABB(395, 405, 10, 590, color='#333', col_layer=1))
        
        # Vidas
        self.life_p1 = [
            draw.Circle(8, pos=(20, 565), color=LIFE_COLOR),
            draw.Circle(8, pos=(43, 565), color=LIFE_COLOR),
            draw.Circle(8, pos=(66, 565), color=LIFE_COLOR),
        ]
        self.life_p2 = [
            draw.Circle(8, pos=(734, 565), color=LIFE_COLOR),
            draw.Circle(8, pos=(757, 565), color=LIFE_COLOR),
            draw.Circle(8, pos=(780, 565), color=LIFE_COLOR),
        ]
        self.add(self.life_p1, layer=1)
        self.add(self.life_p2, layer=1)
        #self.trash = RegularPoly(3, 50, pos=pos.middle, color='white')
        
        # Insere as pás como AABBs
        self.paddle1 = AABB(
            10, 10 + PADDLE_WIDTH, 300 - PADDLE_HEIGHT / 2, 300 + PADDLE_HEIGHT / 2,
            color=PADDLE_COLOR,
            mass='inf', 
        )
        self.paddle2 = AABB(
            790 - PADDLE_WIDTH, 790, 300 - PADDLE_HEIGHT / 2, 300 + PADDLE_HEIGHT / 2,
            color=PADDLE_COLOR,
            mass='inf',
        )
        self.paddle_list = [self.paddle1, self.paddle2]
        self.paddle2.move(0, 20)
        
        # Insere a bola
        self.ball = Circle(
            BALL_RADIUS, 
            pos=pos.middle - (200, 0), 
            vel=(350, 0),
            color=BALL_COLOR,
        )
        self.ball.listen('pre-collision', self.ball_collision)

    def ball_collision(self, col):
        '''Acionado quando há colisão de algum objeto com a bola'''
        
        ball = self.ball
        other = col.other(ball)
        
        if other is self.paddle1 or other is self.paddle2:
            col.resolve()
            paddle = other
            delta_y = col.pos.y - paddle.pos.y
            ball.vel += (0, BALL_SPEED_CHANGE * delta_y)

    @listen('long-press', 'up', paddle_idx=1, direction=1)
    @listen('long-press', 'down', paddle_idx=1, direction=-1)
    @listen('long-press', 'w', paddle_idx=0, direction=1)
    @listen('long-press', 's', paddle_idx=0, direction=-1)
    def move_paddle(self, paddle_idx, direction):
        paddle = self.paddle_list[paddle_idx]
        x, y = paddle.pos 
        y += direction * PADDLE_STEP
        y = max(y, 10 + PADDLE_HEIGHT / 2)
        y = min(y, 590 - PADDLE_HEIGHT / 2)
        paddle.pos = Vec(x, y)
    
    def __setattr__(self, attr, value):
        super().__setattr__(attr, value) 
        
        if isinstance(value, (Body, Drawable)):
            self.add(value)
        
        
if __name__ == '__main__':
    world = Pong()
    world.run()