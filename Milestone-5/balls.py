
import random
import simplegui
from user305_o32FtUyCKk_0 import Vector

CANVAS_WIDTH = 600
CANVAS_HEIGHT = 400

class Ball:
    def __init__(self, pos, vel, radius, color):
        self.pos = pos
        self.vel = vel
        self.radius = radius
        self.color = color
        
    def update(self):
        self.pos.add(self.vel)
        
    def draw(self, canvas):
        canvas.draw_circle(self.pos.get_p(),
                           self.radius,
                           1,
                           self.color,
                           self.color)

    def hit(self, ball):
        distance = ball.pos.copy().subtract(self.pos).length()
        return distance < ball.radius + self.radius
    
    def random_ball():
        return Ball(Vector(random.randint(0, CANVAS_WIDTH),
                           random.randint(0, CANVAS_HEIGHT)),
                    Vector(random.randint(-5, 5),
                           random.randint(-5, 5)),
                    random.randint(10, 30),
                    "rgb({},{},{})".format(random.randint(0,255),
                                          random.randint(0, 255),
                                          random.randint(0, 255)))
        
class Interaction:
    def __init__(self, balls):
        self.balls = balls
        self.in_collision = set()
        
    def draw(self, canvas):
        self.update()
    
        [b.draw(canvas) for b in self.balls]       

    def update(self):
        [b.update() for b in self.balls]
        
        for b1 in self.balls:
            for b2 in self.balls:
                if b1.hit(b2):
                    if b1 == b2:
                        continue
                        
                    b1b2 = (b1,b2) in self.in_collision
                    b2b1 = (b2,b1) in self.in_collision
                    if not (b1b2 or b2b1):
                        self.collide(b1,b2)
                        self.in_collision.add((b1,b2))
                else:
                    self.in_collision.discard((b1,b2))
                    self.in_collision.discard((b2,b1))                        
            
    def collide(self, ball1, ball2):
        normal = ball1.pos.copy().subtract(ball2.pos).normalize()
        
        v1_par = ball1.vel.get_proj(normal)
        v1_perp = ball1.vel.copy().subtract(v1_par)
        
        v2_par = ball2.vel.get_proj(normal)
        v2_perp = ball2.vel.copy().subtract(v2_par)
        
        ball1.vel = v2_par + v1_perp
        ball2.vel = v1_par + v2_perp
        
balls = [Ball.random_ball() for i in range(10)]

interaction = Interaction(balls)

frame = simplegui.create_frame("balls", CANVAS_WIDTH, CANVAS_HEIGHT)
frame.set_draw_handler(interaction.draw)
frame.start()



                
