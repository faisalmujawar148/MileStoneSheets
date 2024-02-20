import simplegui, math
from user305_o32FtUyCKk_0 import Vector

class Wall:
    def __init__(self, x, border, color):
        self.x = x
        self.border = border
        self.color = color
        # Changing the normal vector to point towards the left
        self.normal = Vector(-1,0)
        self.edge_r = x + self.border
        self.edge_l = x - self.border

    def draw(self, canvas):
        canvas.draw_line((self.x, 0),
                         (self.x, CANVAS_HEIGHT),
                         self.border*2+1,
                         self.color)

    def hit(self, ball):
        # Checking if the right edge of the ball intersects with the left edge of the wall
        h = (ball.offset_r() >= self.edge_l)
        return h

class Ball:
    def __init__(self, pos, vel, radius, border, color):
        self.pos = pos
        self.vel = vel
        self.radius = radius
        self.border = 1
        self.color = color

    def offset_l(self):
        return self.pos.x - self.radius
    
    def offset_r(self):
        return self.pos.x + self.radius

    def update(self):
        self.pos.add(self.vel)

    def draw(self, canvas):
        canvas.draw_circle(self.pos.get_p(),
                           self.radius,
                           self.border,
                           self.color,
                           self.color)

    def bounce(self, normal):
        self.vel.reflect(normal)

class Interaction:
    def __init__(self, wall, ball):
        self.ball = ball
        self.wall = wall

    def update(self):
        if self.wall.hit(self.ball):
            self.ball.bounce(self.wall.normal)
        self.ball.update()

    def draw(self, canvas):
        self.update()
        self.ball.draw(canvas)
        self.wall.draw(canvas)

# The canvas dimensions
CANVAS_WIDTH = 600
CANVAS_HEIGHT = 400

# Initial position and velocity of the ball
p = Vector(500,200)
v = Vector(1,-1)

# Creating the objects
b = Ball(p, v, 20, 50, 'blue')
w = Wall(600, 5, 'red')
i = Interaction(w, b)

# Create a frame and assign callbacks to event handlers
frame = simplegui.create_frame("ball-wall", CANVAS_WIDTH, CANVAS_HEIGHT)
frame.set_draw_handler(i.draw)

# Start the frame animation
frame.start()
