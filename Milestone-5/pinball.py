import simplegui
import random
from user305_o32FtUyCKk_0 import Vector

CANVAS_WIDTH = 500
CANVAS_HEIGHT = 500

def randomVel():
    vel = random.randrange(-5, 5)
    while vel == 0:
        vel = random.randrange(-5, 5)
    return vel
    
def randFrac():
    return (random.randrange(0,500)/500)

class Ball:
    def __init__(self, pos, vel, radius, color):
        self.pos = pos
        self.vel = vel
        self.radius = radius
        self.border = 1
        self.color = color

    def draw(self, canvas):
        canvas.draw_circle(self.pos.get_p(),
                self.radius ,
                self.border,
                self.color,
                self.color)

    def update(self):
        self.pos.add(self.vel)
        
    def offset_l(self):
        return self.pos.x - self.radius
    
    def offset_r(self):
        return self.pos.x + self.radius
    
    def offset_b(self):
        return self.pos.y - self.radius
    
    def offset_t(self):
        return self.pos.y + self.radius
    
    def bounce(self, normal):
        self.vel.reflect(normal)
        
class Wall:
    def __init__(self, x1, x2, y1, y2, border, color):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.border = border
        self.color = color
        if x1 == x2:
            self.normal = Vector(1, 0)
        else:
            self.normal = Vector(0, 1)
        self.edge_r = x1 + self.border
        self.edge_l = x1 - self.border
        self.edge_b = y1 + self.border
        self.edge_t = y1 - self.border

    def draw(self, canvas):
        canvas.draw_line((self.x1, self.y1),
                         (self.x2, self.y2),
                         self.border*2+1,
                         self.color)

    def hit(self, ball):
        if self.x1 == self.x2:
            if self.x1 == 0:
                return ball.offset_l() <= self.edge_r
            else:
                return ball.offset_r() >= self.edge_l
        else:
            if self.y1 == 0:
                return ball.offset_b() <= self.edge_t
            else:
                return ball.offset_t() >= self.edge_b
            
        
class Domain:
    def __init__(self, pos, rad, border, color, border_col):
        self.pos = pos
        self.radius = rad
        self.border = border
        self.color = color
        self.border_color = border_col
        self.edge = self.radius + self.border

    def draw(self, canvas):
        canvas.draw_circle(self.pos.get_p(),
                           self.radius,
                           self.border*2+1,
                           self.border_color,
                           self.color)

    def hit(self, ball):
        distance = self.pos.copy().subtract(ball.pos).length()
        return distance - ball.radius <= self.edge

    def normal(self, ball):
        perpendicular = self.pos.copy().subtract(ball.pos)
        return perpendicular.normalize()

class Interaction:
    def __init__(self, domains, walls, ball):
        self.ball = ball
        self.walls = walls
        self.domains = domains
        self.in_collision = False
        
    def draw(self, canvas):
        self.update()
        for domain in self.domains:
            domain.draw(canvas)
        for wall in self.walls:
            wall.draw(canvas)
        self.ball.draw(canvas)

    def update(self):
        self.ball.update()
        for domain in self.domains:
            if domain.hit(self.ball):
                if not self.in_collision:
                    normal = domain.normal(self.ball)
                    self.ball.bounce(normal)
                    self.in_collision = True
            else:
                self.in_collision = False
        for wall in self.walls:
            if wall.hit(self.ball):
                if not self.in_collision:
                    self.ball.bounce(wall.normal)
                    self.in_collision = True
            else:
                self.in_collision = False

ball = Ball(Vector(1/6 * CANVAS_WIDTH, 3/4 * CANVAS_HEIGHT), Vector(randomVel(), randomVel()), 10, "blue")
walls = [Wall(0, 0, 0, CANVAS_HEIGHT, 1, 'red'),
         Wall(CANVAS_WIDTH, CANVAS_WIDTH, 0, CANVAS_HEIGHT, 1, 'red'),
         Wall(0, CANVAS_WIDTH, 0, 0, 1, 'red'),
         Wall(0, CANVAS_WIDTH, CANVAS_HEIGHT, CANVAS_HEIGHT, 1, 'red')]
domains = [Domain(Vector(CANVAS_WIDTH*randFrac(), CANVAS_HEIGHT*randFrac()), random.randrange(10, 50), 1, "black", "red"), 
           Domain(Vector(CANVAS_WIDTH*randFrac(), CANVAS_HEIGHT*randFrac()), random.randrange(10, 50), 1, "black", "red"),
           Domain(Vector(CANVAS_WIDTH*randFrac(), CANVAS_HEIGHT*randFrac()), random.randrange(10, 50), 1, "black", "red"),
           Domain(Vector(CANVAS_WIDTH*randFrac(), CANVAS_HEIGHT*randFrac()), random.randrange(10, 50), 1, "black", "red"),
           Domain(Vector(CANVAS_WIDTH*randFrac(), CANVAS_HEIGHT*randFrac()), random.randrange(10, 50), 1, "black", "red"),
           Domain(Vector(CANVAS_WIDTH*randFrac(), CANVAS_HEIGHT*randFrac()), random.randrange(10, 50), 1, "black", "red"),
           Domain(Vector(CANVAS_WIDTH*randFrac(), CANVAS_HEIGHT*randFrac()), random.randrange(10, 50), 1, "black", "red")]
interaction = Interaction(domains, walls, ball)

frame = simplegui.create_frame("Domain", CANVAS_WIDTH, CANVAS_HEIGHT)
frame.set_draw_handler(interaction.draw)

frame.start()