try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import random
import math
# Some constants
CANVAS_DIMS = (600, 400)
bullet_radius = 5
ship_scale = (100, 100)
asteroid_scale = (50, 50)
IMG1 = simplegui.load_image('https://i.ibb.co/yXPtX31/spaceship1.png')
THRUSTER_IMG1 = simplegui.load_image("https://i.ibb.co/yQ0m2Sm/thrusters.png")
IMG1_DIMS = (360, 360)
IMG1_CENTRE = (IMG1_DIMS[0]/2,IMG1_DIMS[1]/2)
IMG2 = simplegui.load_image('https://images.freeimages.com/vhq/images/previews/e23/asteroid-97287.png?fmt=webp&w=500')
IMG2_DIMS = (500, 500)
IMG2_CENTRE = (IMG2_DIMS[0]/2,IMG2_DIMS[1]/2)

score = 0
button_height = 40
button_width = 150
button_pos = (90, 360)

asteroids = []
bullets = []
shooting = False

def camera(pos):
    return [pos[0]-offset[0],pos[1]-offset[1]]
        
def randomVel(pos):
    if (pos[0] - CANVAS_DIMS[0]/2) >= 0:
        x = random.randint(-5,-1)
    elif (pos[0] - CANVAS_DIMS[0]/2) < 0:
        x = random.randint(1,5)
    if (pos[1] - CANVAS_DIMS[1]/2) >= 0:
        y = random.randint(-2,-1)
    elif (pos[1] - CANVAS_DIMS[1]/2) < 0:
        y=random.randint(1,2)
    return (x, y)

def randomPos():
    x = 600
    y = random.randint(0, 400)
    return (x, y)

def randomRot():
    rot = random.randint(-5, 5)
    return rot

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

class Spaceship:
    def __init__(self, img, thruster_img, img_centre, img_dims, position, hp):
        self.img = img
        self.thruster_img = thruster_img
        self.img_centre = img_centre
        self.img_dims = img_dims
        self.position = position
        self.hp = hp
    def move(self, canvas):
        #thrusters animation and optionally particle effects for that
        global ship_angle
        canvas.draw_image(self.thruster_img, self.img_centre, self.img_dims, self.position, ship_scale, ship_angle-55)
        
    def draw(self, canvas):
        global ship_angle
        canvas.draw_image(self.img, self.img_centre, self.img_dims, self.position, ship_scale, ship_angle-55)
        
    def update(self, canvas):
        self.draw(canvas)
        if self.hp == 0:
            Spaceship.hit(self)
            frame = simplegui.create_frame("Game Over", CANVAS_DIMS[0], CANVAS_DIMS[1])
            frame.set_canvas_background('Red')
            # frame.set_draw_handler(Interaction.draw)
            frame.set_mouseclick_handler(Interaction.mouse_handler)
            frame.set_draw_handler(self.drawer)
            #frame.set_keydown_handler(Interaction.keydown_handler)
            frame.start()

          
    def drawer(self, canvas):
            canvas.draw_text("GAME OVER!", [65, 90], 50, "White")
            canvas.draw_text("You have " + str(self.hp) + " lives", [70, 150], 35, "Blue")
            canvas.draw_text("You have " + str(score) + " points", [70, 200], 35, "Blue")
            canvas.draw_text("Click the button to restart", [70, 250], 25, "Blue")
            canvas.draw_polygon([(button_pos[0] - button_width/2, button_pos[1] - button_height/2),
                             (button_pos[0] - button_width/2, button_pos[1] + button_height/2),
                             (button_pos[0] + button_width/2, button_pos[1] + button_height/2),
                             (button_pos[0] + button_width/2, button_pos[1] - button_height/2)],
                            1, "White", "Green")
            canvas.draw_text("RESTART", (button_pos[0] - button_width/4, button_pos[1] + button_height/4), 24, "White")
        
    def hit(self):
        #ship blinks when hit
        self.hp -= 1

class Asteroid:
    def __init__(self, img, img_centre, img_dims, position, vel, rotation):
        self.img = img
        self.img_centre = img_centre
        self.img_dims = img_dims
        self.position = position
        self.vel = vel
        self.rotation = rotation
        self.isHit = False
        
    def draw(self, canvas):
        canvas.draw_image(self.img, self.img_centre, self.img_dims, self.position, asteroid_scale, self.rotation)

    #def explode(self, canvas, position):
        #insert explosion animation
        #canvas.draw_image(---------------------)

    def update(self, canvas):
        self.position = (self.position[0] + self.vel[0], self.position[1] + self.vel[1])
        self.draw(canvas)
        
class Bullet:
    def __init__(self, position, vel, rotation):
        self.position = position
        self.vel = vel
        self.rotation = rotation
    def draw(self, canvas):
        canvas.draw_circle((self.position[0],self.position[1]), bullet_radius, 1, "yellow", "red")

    def update(self, canvas):
        self.position = (self.position[0] + self.vel*math.cos(self.rotation), self.position[1] + self.vel*math.sin(self.rotation))
        self.draw(canvas)

class Interaction:
    def __init__(self, keyboard, spaceship):
        self.keyboard = keyboard
        self.booster_velocity = -8  # Initial jump velocity
        self.accel = 0.5  # Gravity acceleration
        self.max_vel = 100  # Maximum jump height
        self.friction = 0.9
        self.spaceship = spaceship

    def button_clicked():
        # Create a frame and assign callbacks to event handlers
        frame = simplegui.create_frame("Space Fighters", CANVAS_DIMS[0], CANVAS_DIMS[1])
        frame.set_canvas_background('#2C6A6A')
        frame.set_draw_handler(draw)
        frame.set_keydown_handler(keyboard.keydown_handler)
        frame.set_keyup_handler(keyboard.keyup_handler)
        frame.start()
        
    def draw(canvas):
        canvas.draw_polygon([(button_pos[0] - button_width/2, button_pos[1] - button_height/2),
                             (button_pos[0] - button_width/2, button_pos[1] + button_height/2),
                             (button_pos[0] + button_width/2, button_pos[1] + button_height/2),
                             (button_pos[0] + button_width/2, button_pos[1] - button_height/2)],
                            1, "White", "Blue")
        canvas.draw_text("START", (button_pos[0] - button_width/4, button_pos[1] + button_height/4), 24, "White")
        
        
    def welcome(canvas):
        canvas.draw_text("Welcome to Space Fighters!", [65, 90], 45, "Yellow")
        canvas.draw_text("CAN YOU DEFEAT THE ASTEROIDS?", [70, 150], 20, "Blue")
        canvas.draw_text("Use your arrow keys to dodge the asteroids", [70, 190], 20, "Blue")
        canvas.draw_text("and try shooting them by holding the spacebar", [70, 230], 20, "Blue")
        canvas.draw_text("Are you up for the challenge?", [70, 270], 20, "Blue")
        canvas.draw_text("Click the button to start", [70, 320], 20, "Purple")
        Interaction.draw(canvas)
    
    def mouse_handler(pos):
        if (button_pos[0] - button_width / 2) < pos[0] < button_pos[0] + button_width / 2 and \
           (button_pos[1] - button_height / 2 < pos[1] < button_pos[1] + button_height / 2):
            Interaction.button_clicked()  # Corrected indentation
            
    def update(self, canvas):
        global ship_angle
        global speed_x
        global speed_y
        global shooting
        if self.keyboard.left:
            ship_angle -= 10 * 0.01
        elif self.keyboard.right:
            ship_angle += 10 * 0.01
        elif self.keyboard.up:
            self.booster_velocity = 10
            speed_x += math.cos(ship_angle) * self.booster_velocity * 0.1
            speed_y += math.sin(ship_angle) * self.booster_velocity * 0.1
            if self.booster_velocity < self.max_vel:
                self.booster_velocity += self.accel
            else:
                self.booster_velocity = -10
            self.spaceship.move(canvas)
        elif self.keyboard.down:
            self.booster_velocity = 10
            speed_x -= math.cos(ship_angle) * self.booster_velocity * 0.1
            speed_y -= math.sin(ship_angle) * self.booster_velocity * 0.1
            if (-1)*self.booster_velocity < self.max_vel:
                self.booster_velocity -= self.accel
            else:
                self.booster_velocity = -10
            self.spaceship.move(canvas)
        elif self.keyboard.space:
            shooting = True
            
        else:
            speed_x *= self.friction
            speed_y *= self.friction
            shooting = False
        
        self.spaceship.position = (self.spaceship.position[0] + speed_x * 0.03,
                                    self.spaceship.position[1] + speed_y * 0.03)
        ship_angle %= 2 * math.pi
        if self.spaceship.position[0] < 0:
            self.spaceship.position = (self.spaceship.position[0] % CANVAS_DIMS[0], self.spaceship.position[1])
        if self.spaceship.position[1] < 0:
            self.spaceship.position = (self.spaceship.position[0] % CANVAS_DIMS[1], self.spaceship.position[1] % CANVAS_DIMS[1])
        speed_x -= speed_x*self.friction*0.0001
        speed_y -= speed_y*self.friction*0.0001

class Collisions1:
    def __init__(self):
        ship

    def update(self):
        global ship
        global asteroids
        safe_dist_sqr = ((ship_scale[0] + asteroid_scale[0])/2)**2
        debris = []
        for i in range(len(asteroids)):
            if (not asteroids[i].isHit):
                if (ship.position[0]-asteroids[i].position[0])**2 + (ship.position[1]-asteroids[i].position[1])**2 < safe_dist_sqr:
                    debris.append(i)
                    asteroids[i].isHit = True
                    print('hit')
                    ship.hp -=1
                    print(ship.hp)
                    #ship.hit()
        for i in range(len(debris)):
            asteroids.pop(debris[i])
            
class Collisions2:
    def __init__(self):
        pass

    def update(self):
        global score
        global bullets
        global asteroids
        safe_dist_sqr = (bullet_radius + (asteroid_scale[0])/2)**2
        debris = [[], []]
        for i in range(len(bullets)):
            for j in range(len(asteroids)):
                if (not asteroids[j].isHit):
                    if (bullets[i].position[0]-asteroids[j].position[0])**2 + (bullets[i].position[1]-asteroids[j].position[1])**2 < safe_dist_sqr:
                        score += 10
                        debris[0].append(i)
                        debris[1].append(j)
                        asteroids[j].isHit = True
                        #asteroids[i].explode(canvas, asteroids[i].position)
        for i in range(len(debris[0])):
            bullets.pop(debris[0][i])
            asteroids.pop(debris[1][i])
            
class Scoreboard:
    def __init__(self):
        pass
    def update(self, canvas):
        global score
        string = str(int(score))
        canvas.draw_text(string,(10,19),20,"black","monospace")
# Global variables
ship_angle = 0
offset = [0,0]
speed_x = speed_y = 0
keyboard = Keyboard()
ship = Spaceship(IMG1, THRUSTER_IMG1, IMG1_CENTRE, IMG1_DIMS, (60, 200), 10)
interaction = Interaction(keyboard, ship)
collisions1 = Collisions1()
collisions2 = Collisions2()
scoreboard = Scoreboard()
def bullet_cd_handler():
    global ship
    global ship_angle
    global shooting
    if shooting:
        bullets.append(Bullet(ship.position, 1, ship_angle))

def timer_handler():
    global asteroids
    if len(asteroids) < 30:
        pos = randomPos()
        vel = randomVel(pos)
        asteroids.append(Asteroid(IMG2, IMG2_CENTRE, IMG2_DIMS, pos, vel, randomRot()))

bullet_cd = simplegui.create_timer(400, bullet_cd_handler)
bullet_cd.start()
timer = simplegui.create_timer(3000, timer_handler)
timer.start()

# Drawing handler
def draw(canvas):
    global score  
    score += 1/30
    collisions1.update()
    collisions2.update()
    interaction.update(canvas)
    out_range = [[], []]
    scoreboard.update(canvas)
    for i in range(len(bullets)):
        bullets[i].update(canvas)
        if (bullets[i].position[0] < 0)|(bullets[i].position[0] > CANVAS_DIMS[0])|(bullets[i].position[1] < 0)|(bullets[i].position[1] > CANVAS_DIMS[1]):
                out_range[0].append(i)
    for i in range(len(out_range[0])):
        bullets.pop(out_range[0][i])
        
    for i in range(len(asteroids)):
        asteroids[i].update(canvas)
        if (asteroids[i].position[0] < 0)|(asteroids[i].position[0] > CANVAS_DIMS[0])|(asteroids[i].position[1] < 0)|(asteroids[i].position[1] > CANVAS_DIMS[1]):
                out_range[1].append(i)
    for i in range(len(out_range[1])):
        asteroids.pop(out_range[1][i])
    ship.update(canvas)

# Create a frame and assign callbacks to event handlers

# Create a frame and assign callbacks to event handlers
frame = simplegui.create_frame("Main Menu", CANVAS_DIMS[0], CANVAS_DIMS[1])
frame.set_canvas_background('Black')
frame.set_draw_handler(Interaction.welcome)
# frame.set_draw_handler(Interaction.draw)
frame.set_mouseclick_handler(Interaction.mouse_handler)
#frame.set_keydown_handler(Interaction.keydown_handler)
frame.start()
