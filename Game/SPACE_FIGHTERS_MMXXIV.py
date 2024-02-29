#rename later
try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import random
import math
# Some constants
CANVAS_DIMS = (600, 400)
ship_angle = 0
IMG = simplegui.load_image('https://opengameart.org/sites/default/files/ship5.png')
IMG_CENTRE = (183, 152)
IMG_DIMS = (366, 204)
IMG2 = simplegui.load_image('https://images.freeimages.com/vhq/images/previews/e23/asteroid-97287.png?fmt=webp&w=500')
IMG2_CENTRE = (250, 250 )
IMG2_DIMS = (500,500 )

def randomVel():
    vel = random.randInt(1,5)
    return vel

def randomPos():
    x = 600
    y = random.randInt(0,400)
    return (x,y)

class Keyboard:
    def __init__(self):
        self.left = False
        self.right = False
        self.space = False
        self.up = False
        self.down = False

    def keydown_handler(self, key):
        if key == simplegui.KEY_MAP['left']:
            self.left = True
        elif key == simplegui.KEY_MAP['right']:
            self.right = True
        elif key == simplegui.KEY_MAP['up']:  
            self.up = True
        elif key == simplegui.KEY_MAP['down']:
            self.down = True
        elif key == simplegui.KEY_MAP['space']:
            self.space = True

    def keyup_handler(self, key):
        if key == simplegui.KEY_MAP['left']:
            self.left = False
        elif key == simplegui.KEY_MAP['right']:
            self.right = False
        elif key == simplegui.KEY_MAP['up']:  
            self.up = False
        elif key == simplegui.KEY_MAP['down']:
            self.down = False
        elif key == simplegui.KEY_MAP['space']: 
            self.space = False
            

class Interaction:
    def __init__(self, keyboard):
        self.keyboard = keyboard
        self.booster_velocity = -8  # Initial jump velocity
        self.accel = 0.5  # Gravity acceleration
        self.max_vel = 100  # Maximum jump height
        self.friction = 0.9

    def update(self):
        global STEP
        global MOVE
        global ship_angle
        global img_pos
        global speed_x
        global speed_y
        if self.keyboard.left:
                ship_angle-=10*0.01
        elif self.keyboard.right:
                ship_angle+=10*0.01
        elif self.keyboard.up:
                self.booster_velocity = -10
                print(math.cos(ship_angle))
                print(math.sin(ship_angle))
                speed_x+= math.cos(ship_angle) * self.booster_velocity *0.3
                speed_y+= math.sin(ship_angle) * self.booster_velocity *0.3
                if self.booster_velocity < self.max_vel:
                	self.booster_velocity += self.accel
                else:
                    self.booster_velocity = 10
        else:
            speed_x*=self.friction
            speed_y*=self.friction
        img_pos[0]+=speed_x*0.03
        img_pos[1]+=speed_y*0.03
        ship_angle %= 2 * math.pi
        if img_pos[0] % CANVAS_DIMS[0]:
            img_pos[0] = img_pos[0]%CANVAS_DIMS[0]
        if img_pos[1] % CANVAS_DIMS[1]:
            img_pos[1] = img_pos[1] % CANVAS_DIMS[1]
        
        

# Global variables

img_dest_dim = (128,128)
img_pos = [CANVAS_DIMS[0]/2, CANVAS_DIMS[1]/2]
ship_angle = 0
speed_x=speed_y=0
keyboard = Keyboard()
interaction = Interaction(keyboard)

# Drawing handler
def draw(canvas):
    global ship_angle
    global img_pos
    
    interaction.update()
    canvas.draw_image(IMG2, IMG2_CENTRE, IMG2_DIMS, (20,20), img_dest_dim, 0)
    canvas.draw_image(IMG, IMG_CENTRE, IMG_DIMS, img_pos, img_dest_dim, ship_angle+180)

# Create a frame and assign callbacks to event handlers
frame = simplegui.create_frame("SPACE FIGHTERS MMXXIV", CANVAS_DIMS[0], CANVAS_DIMS[1])
frame.set_draw_handler(draw)
frame.set_keydown_handler(keyboard.keydown_handler)
frame.set_keyup_handler(keyboard.keyup_handler)


# Start the frame animation
frame.start()
