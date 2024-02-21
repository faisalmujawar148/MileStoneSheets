import math
try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
from user305_o32FtUyCKk_0 import Vector

CANVAS_WIDTH = 500
CANVAS_HEIGHT = 500

class Wall:
    def __init__(self, x, y, border, color, wall_type):
        self.x = x
        self.y = y
        self.border = border
        self.color = color
        self.wall_type = wall_type
        if self.wall_type == 'r':
            self.normal = Vector(-1, 0)
        elif self.wall_type == 'l':
            self.normal = Vector(1, 0)
        elif self.wall_type == 't':
            self.normal = Vector(0, -1)
        elif self.wall_type == 'b':
            self.normal = Vector(0, 1)
        else:
            print("Error: Invalid wall type")
        
        self.edge_r = x + self.border
        self.edge_l = x - self.border
        self.edge_u = y + self.border
        self.edge_d = y - self.border

    def draw(self, canvas):
        if self.wall_type == 'r' or self.wall_type == 'l':
            canvas.draw_line((self.x, 0),
                             (self.x, CANVAS_HEIGHT),
                             self.border*2+1,
                             self.color)
        elif self.wall_type == 't' or self.wall_type == 'b':
            canvas.draw_line((0, self.y),
                             (CANVAS_WIDTH, self.y),
                             self.border*2+1,
                             self.color)
    
    def hit(self, ball):
        if self.wall_type == 'r':
            return ball.offset_l() <= self.edge_r
        elif self.wall_type == 'l':
            return ball.offset_l() >= self.edge_l
        elif self.wall_type == 't':
            return ball.offset_v() <= self.edge_u
        elif self.wall_type == 'b':
            return ball.offset_v() >= self.edge_d

class Ball:
    def __init__(self, pos, vel, radius, color):
        self.pos = pos
        self.vel = vel
        self.radius = radius
        self.border = 1
        self.color = color

    def draw(self, canvas):
        canvas.draw_circle(self.pos.get_p(),
                self.radius,
                self.border,
                self.color,
                self.color)
                           
    def update(self):
        self.pos.add(self.vel)

    def offset_l(self):
        if self.vel.x > 0:
            return self.pos.x + self.radius
        else:
            return self.pos.x - self.radius
    def offset_v(self):
        if self.vel.y > 0:
            return self.pos.y + self.radius
        else:
            return self.pos.y - self.radius

    def bounce(self, normal):
        self.vel.reflect(normal)

class Interaction:
    def __init__(self, wall, ball):
        self.ball = ball
        self.wall = wall
        self.in_collision = False

    def update(self):
        if self.wall.hit(self.ball):
            if not self.in_collision:
                self.ball.bounce(self.wall.normal)
                self.in_collision = True
        else:
            self.in_collision = False

        self.ball.update()  

    def draw(self, canvas):
        self.update()
        self.ball.draw(canvas)
        self.wall.draw(canvas)

p = Vector(100,200)
v = Vector(1,-1)

b = Ball(p, v, 20, 'blue')
w = Wall(0, 0, 5, 'red', 'r')
i = Interaction(w, b)
w2 = Wall(300, 0, 5, 'red', 'l')
i2 = Interaction(w2, b)
w3 = Wall(0, 0, 10, 'red', 't')  
i3 = Interaction(w3,b)
w4 = Wall(0, 500, 10, 'red', 'b')
i4 = Interaction(w4,b)
frame = simplegui.create_frame("Bounce", CANVAS_WIDTH, CANVAS_HEIGHT)

def draw_handler(canvas):
    i.draw(canvas)  
    i2.draw(canvas)  
    i3.draw(canvas)  
    i4.draw(canvas)

frame.set_draw_handler(draw_handler)
frame.start()
