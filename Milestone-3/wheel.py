from user304_rsf8mD0BOQ_1 import Vector
try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

WIDTH = 500
HEIGHT = 500
                
class Wheel:
    def __init__(self, pos, radius=10):
        self.pos = pos
        self.vel = Vector()
        self.radius = max(radius, 10)
        self.colour = 'White'

    def draw(self, canvas):
        canvas.draw_circle(self.pos.get_p(), self.radius, 1, self.colour, self.colour)
        
    def update(self):
        self.pos.add(self.vel)
        self.vel.multiply(0.85)
    
class Keyboard:
    def __init__(self):
        self.right = False
        self.left = False

    def keyDown(self, key):
        if key == simplegui.KEY_MAP['right']:
            self.right = True
        elif key == simplegui.KEY_MAP['left']:
            self.left = True

    def keyUp(self, key):
        if key == simplegui.KEY_MAP['right']:
            self.right = False
        elif key == simplegui.KEY_MAP['left']:
            self.left = False

class Interaction:
    def __init__(self, wheel, keyboard):
        self.wheel = wheel
        self.keyboard = keyboard

    def update(self):
        if self.keyboard.right:
            self.wheel.vel.add(Vector(1, 0))
        elif self.keyboard.left:
            self.wheel.vel.add(Vector(-1, 0))

kbd = Keyboard()
wheel = Wheel(Vector(WIDTH/2, HEIGHT-40), 40)
inter = Interaction(wheel, kbd)

def draw(canvas):
    inter.update()
    wheel.update()
    wheel.draw(canvas)

frame = simplegui.create_frame('Interactions', WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(kbd.keyDown)
frame.set_keyup_handler(kbd.keyUp)
frame.start()
