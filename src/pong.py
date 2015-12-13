'''
Uma versão do clássico de Atari PONG.
'''

from FGAme import *
from FGAme.physics import Body
from FGAme.extra.letters import add_word
from FGAme.draw import Drawable
from random import choice


LIMIT_COLOR = 'white'
PADDLE_HEIGHT = 100
PADDLE_WIDTH = 20
PADDLE_COLOR = 'green'
BALL_RADIUS = 15
BALL_COLOR = 'red'
BALL_SPEED_CHANGE = 5
BALL_SPEED_INCREMENT = 20
PADDLE_STEP = 5
BALL_SPEED = 300

LIFE_COLOR = '#999'


class Pong(World):
    def init(self):
        self.background = Color('#000')
        
        # Limites
        self.upper_limit = AABB(-500, 800 + 500, 590, 650, mass='inf', color=LIMIT_COLOR)
        self.lower_limit = AABB(-500, 800 + 500, -50, 10, mass='inf', color=LIMIT_COLOR)
        
        self.ball_direction = choice([1,2])
        
        self.front_cover = None
        # Linhas
        self.add(AABB(395, 405, 10, 590, color='#333', col_layer=1), -1)
        
        self.init_life()
        
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
            pos=pos.middle, 
            vel=(0, 0),
            color=BALL_COLOR,
        )
        self.ball.listen('pre-collision', self.ball_collision)

    def init_life(self):
        # Vidas
        self.life_p1 = [
            Circle(8, pos=(20, 565), color=LIFE_COLOR, col_layer=1),
            Circle(8, pos=(43, 565), color=LIFE_COLOR, col_layer=1),
            Circle(8, pos=(66, 565), color=LIFE_COLOR, col_layer=1),
        ]
        self.life_p2 = [
            Circle(8, pos=(729, 30), color=LIFE_COLOR, col_layer=1),
            Circle(8, pos=(752, 30), color=LIFE_COLOR, col_layer=1),
            Circle(8, pos=(775, 30), color=LIFE_COLOR, col_layer=1),
        ]
        self.add(self.life_p1, layer=1)
        self.add(self.life_p2, layer=1) 


    def ball_collision(self, col):
        '''Acionado quando há colisão de algum objeto com a bola'''
        
        ball = self.ball
        other = col.other(ball)
        
        if other is self.paddle1 or other is self.paddle2:
            col.resolve()
            paddle = other
            delta_y = col.pos.y - paddle.pos.y
            old_speed = ball.vel.norm()
            ball.vel += (0, BALL_SPEED_CHANGE * delta_y)
            ball.vel = (ball.vel.normalized() * (old_speed + BALL_SPEED_INCREMENT) )
        
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
        
    @listen('key-up', 'space')   
    def shoot_ball(self):    
        
        if self.front_cover is None:
            
            if self.ball_direction is None:
                return
            elif self.ball_direction == 1:
                self.ball.vel = (-BALL_SPEED, 0)
            elif self.ball_direction == 2:
                self.ball.vel = (BALL_SPEED, 0)
            else:
                raise RuntimeError("Ta errado")
            
            self.ball_direction = None
        else:
            self.remove(self.front_cover)
            self.init_life()
            self.ball_direction = choice([1,2])
            
        
    
    def on_frame_enter(self):
        ball = self.ball
        if ball.pos.x < -BALL_RADIUS:
            self.remove(self.life_p1.pop())
            if not self.life_p1:
                self.game_over(1)
            else:
                self.restart(1)
             
        elif ball.pos.x > 800+ BALL_RADIUS:
            self.remove(self.life_p2.pop())
            if not self.life_p2:
                self.game_over(2)
            else:
                self.restart(2)
            
    
    def __setattr__(self, attr, value):
        super().__setattr__(attr, value) 
        
        if isinstance(value, (Body, Drawable)):
            self.add(value)
        
    def game_over(self, player):
        self.restart(choice([1,2]))
        self.front_cover = AABB(0,800,0,600, color='red', col_layer=2)
        self.add(self.front_cover, layer=2)
        
        print("Game Over: Player %s lose" % player)
        #raise SystemExit
    
    def restart(self, player_number):
        self.ball.pos=pos.middle
        self.ball_direction = player_number
        self.ball.vel=(0,0)
        
        self.paddle1.pos = self.paddle1.pos.copy(y=300)
        self.paddle2.pos = self.paddle2.pos.copy(y=300)
        
if __name__ == '__main__':
    world = Pong()
    world.run()