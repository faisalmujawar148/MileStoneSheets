try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
# Some constants
CANVAS_DIMS = (600, 400)

IMG = simplegui.load_image('http://www.cs.rhul.ac.uk/courses/CS1830/sprites/coach_wheel-512.png')
IMG_CENTRE = (256, 256)
IMG_DIMS = (512, 512)

class Keyboard:
    def __init__(self):
        self.left = False
        self.right = False
        self.space = False  

    def keydown_handler(self, key):
        if key == simplegui.KEY_MAP['left']:
            self.left = True
        elif key == simplegui.KEY_MAP['right']:
            self.right = True
        elif key == simplegui.KEY_MAP['space']:  
            self.space = True

    def keyup_handler(self, key):
        if key == simplegui.KEY_MAP['left']:
            self.left = False
        elif key == simplegui.KEY_MAP['right']:
            self.right = False
        elif key == simplegui.KEY_MAP['space']: 
            self.space = False

            
class Interaction:
    def __init__(self, keyboard):
        self.keyboard = keyboard
        self.jump_velocity = -8  # Initial jump velocity
        self.gravity = 0.5  # Gravity acceleration
        self.jump_height = 100  # Maximum jump height
        self.on_ground = True

    def update(self):
        global STEP
        global MOVE
        global img_rot
        global img_pos
        if self.on_ground==True:
            if self.keyboard.left:
                STEP = 0.5
                MOVE = -1
            elif self.keyboard.right:
                STEP = -0.5
                MOVE = 1
            else:
                STEP = 0
                MOVE = 0
        if self.keyboard.space and self.on_ground:
            self.jump_velocity = -10  
            self.on_ground = False  

        if not self.on_ground:
            img_pos[1] += self.jump_velocity  
            self.jump_velocity += self.gravity 
            if img_pos[1] >= CANVAS_DIMS[1] - img_dest_dim[1]:
                img_pos[1] = CANVAS_DIMS[1] - img_dest_dim[1]
                self.on_ground = True
                self.jump_velocity = 0  # Reset jump velocity
        img_rot += STEP
        img_pos[0] += MOVE

# Global variables
img_dest_dim = (128,128)
img_pos = [CANVAS_DIMS[0]/2, 2*CANVAS_DIMS[1]/3.]
img_rot = 0

keyboard = Keyboard()
interaction = Interaction(keyboard)

# Drawing handler
def draw(canvas):
    global img_rot
    global img_pos
    interaction.update()
    canvas.draw_image(IMG, IMG_CENTRE, IMG_DIMS, img_pos, img_dest_dim, img_rot)

# Create a frame and assign callbacks to event handlers
frame = simplegui.create_frame("A wheel", CANVAS_DIMS[0], CANVAS_DIMS[1])
frame.set_canvas_background('#2C6A6A')
frame.set_draw_handler(draw)
frame.set_keydown_handler(keyboard.keydown_handler)
frame.set_keyup_handler(keyboard.keyup_handler)


# Start the frame animation
frame.start()
