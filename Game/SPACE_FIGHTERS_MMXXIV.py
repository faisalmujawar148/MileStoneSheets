try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import random
import math

#Img constants
CANVAS_DIMS = (1024, 768)
bullet_radius = 5
ship_scale = (60, 60)
asteroid_scale = (50, 50)
IMG1 = simplegui.load_image('https://i.ibb.co/yXPtX31/spaceship1.png')
THRUSTER_IMG1 = simplegui.load_image("https://i.ibb.co/yQ0m2Sm/thrusters.png")
IMG1_DIMS = (360, 360)
IMG1_CENTRE = (IMG1_DIMS[0]/2,IMG1_DIMS[1]/2)
IMG2 = simplegui.load_image('https://images.freeimages.com/vhq/images/previews/e23/asteroid-97287.png?fmt=webp&w=500')
IMG2_DIMS = (500, 500)
IMG2_CENTRE = (IMG2_DIMS[0]/2,IMG2_DIMS[1]/2)
#Credit SlashDashGames Studio for the Background
BACKGROUND = simplegui.load_image('https://i.postimg.cc/9WRzjmwB/bggif.png')
BACKGROUND_DIMS = (1024, 768)
#MIDGROUND = simplegui.load_image('http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png')
MIDGROUND = simplegui.load_image('https://i.ibb.co/SnNcDCt/midground-2x-RIFE-RIFE4-0-41-332fps-ezgif-com-gif-to-sprite-converter.png')
MIDGROUND_DIMS = (640, 480)
BORDER = simplegui.load_image('https://i.ibb.co/CnYsJmy/border.png')
BORDER_DIMS = (1024, 750)
offset = [0, 0]
#Counter constants
score = 0
final_score = 0
hit_counter = 0
bg_counter = 0
#Sprite constants
asteroids = []
bullets = []
shooting = False
#Button constants
button_height = 40
button_width = 150
button_pos = (90, 360)

#Subroutines
def camera(pos):
    global offset
    return [pos[0]-offset[0],pos[1]-offset[1]]

def hit_timer(canvas, duration):
    global hit_counter
    hit_counter += 1
    if hit_counter >= duration:
        hit_counter = 0
        ship.isHit = False
        
def randomVel(pos):
    if pos[0] >= CANVAS_DIMS[0]/2:
        x = random.randint(-3,-1)
    elif pos[0] < CANVAS_DIMS[0]/2:
        x = random.randint(1,3)
    if pos[1] >= CANVAS_DIMS[1]/2:
        y = random.randint(-2,-1)
    elif pos[1] < CANVAS_DIMS[1]/2:
        y=random.randint(1,2)
    return (x, y)

def randomPos():
    x = random.choice([0,CANVAS_DIMS[0]])
    y = random.randint(0, CANVAS_DIMS[1])
    return camera((x, y))

def randomRot():
    rot = random.randint(-5, 5)
    return rot

#Classes
class Edge:
    def __init__(self):
        pass
    def draw(self, canvas):
        canvas.draw_polygon([camera((-1500,0)), camera((CANVAS_DIMS[0]+500, 0)), camera((CANVAS_DIMS[0]+500, -500)), camera((-1500, -500))],1,'BLACK','BLACK')
        canvas.draw_polygon([camera((0,0)), camera((0, CANVAS_DIMS[1]+500)), camera((-500, CANVAS_DIMS[1]+500)), camera((-500, 0))],1,'BLACK','BLACK')
        canvas.draw_polygon([camera((0,CANVAS_DIMS[1])), camera((0, CANVAS_DIMS[1]+500)), camera((CANVAS_DIMS[0]+500, CANVAS_DIMS[1]+500)), camera((CANVAS_DIMS[0]+500, CANVAS_DIMS[1]))],1,'BLACK','BLACK')
        canvas.draw_polygon([camera((CANVAS_DIMS[0],CANVAS_DIMS[1])), camera((CANVAS_DIMS[0],-500)), camera((CANVAS_DIMS[0]+500, 0)), camera((CANVAS_DIMS[0]+500, CANVAS_DIMS[1]))],1,'BLACK','BLACK')

class Border:
    def __init__(self,img,dims):
        self.img = img
        self.dims = dims
        
    def draw(self,canvas):
        val = (CANVAS_DIMS[0]/2,CANVAS_DIMS[1]/2)
        canvas.draw_image(border.img, (self.dims[0]/2, self.dims[1]/2), self.dims, val, (1029, 768))
        
class Midground:
    def __init__(self,img,dims):
        self.img=img
        self.dims=dims
        
    def draw(self, canvas):
        global bg_counter
        global move_x
        print(bg_counter)
        camval = camera((CANVAS_DIMS[0]/2,CANVAS_DIMS[1]/2))
        canvas.draw_image(midground.img, (self.dims[0]/2+move_x,self.dims[1]/2), self.dims, camval, (1028, 768))
        if bg_counter % 1 == 0:
            move_x-=0.2
        if move_x<=0:
            move_x+=1028
            
class Background:
    def __init__(self,img,dims,columns,rows):
        self.img=img
        self.dims=dims
        self.columns = columns
        self.rows = rows
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.frame_width = self.width/self.columns
        self.frame_height = self.height/self.rows
        self.frame_centre = (self.frame_width/2, self.frame_height/2)
        self.frame_index = [0,0]
        
    def draw(self, canvas):
        global bg_counter
        global offset
        center_source = (self.frame_width*self.frame_index[0]+self.frame_centre[0], self.frame_height*self.frame_index[1]+self.frame_centre[1])
        width_height_source = (self.frame_width, self.frame_height)
        
        canvas.draw_image(background.img, center_source, width_height_source, (CANVAS_DIMS[0]/2,CANVAS_DIMS[1]/2), (1024, 758))
        if bg_counter % 10 == 0:
            self.next_frame()
        
    def next_frame(self):
        self.frame_index[0] += 1
        if self.frame_index[0] == self.columns:
            self.frame_index[1] += 1
            self.frame_index[0] = 0
        if self.frame_index[1] == self.rows:
            self.frame_index[1] = 0
                             
#def explode(self, canvas, position):
    #insert explosion animation
    #canvas.draw_image(---------------------)

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
        self.isHit = False
        
    def move(self, canvas):
        #thrusters animation and optionally particle effects for that
        global ship_angle
        canvas.draw_image(self.thruster_img, self.img_centre, self.img_dims, camera(self.position), ship_scale, ship_angle-55)
    def draw(self, canvas):
        global ship_angle
        canvas.draw_image(self.img, self.img_centre, self.img_dims, camera(self.position), ship_scale, ship_angle-55)
        
    def update(self, canvas):
        global offset
        global score
        global final_score
        offset = [self.position[0]-512, self.position[1]-384]
        self.draw(canvas)
        if self.hp == 0:
            self.hp -= 1
            final_score = score
            global frame3
            frame3 = simplegui.create_frame("Game Over", CANVAS_DIMS[0], CANVAS_DIMS[1])
            frame3.set_canvas_background('Red')
            frame3.set_mouseclick_handler(Spaceship.mouse_handler)
            frame3.set_draw_handler(self.game_over)
            frame3.start()
    
    def mouse_handler(pos):
        global bullets
        global asteroids
        frame3.stop()
        if (button_pos[0] - button_width / 2 < pos[0] < button_pos[0] + button_width / 2) and (button_pos[1] - button_height / 2 < pos[1] < button_pos[1] + button_height / 2):
            bullets = []
            asteroids = []
            Interaction.button_clicked()
               
    def game_over(self, canvas):
        global final_score
        canvas.draw_text("GAME OVER!", [65, 90], 50, "White")
        canvas.draw_text("You have " + str(final_score//1) + " points", [70, 200], 35, "Blue")
        canvas.draw_text("Click the button to restart", [70, 250], 25, "Blue")
        canvas.draw_polygon([(button_pos[0] - button_width/2, button_pos[1] - button_height/2),
                             (button_pos[0] - button_width/2, button_pos[1] + button_height/2),
                             (button_pos[0] + button_width/2, button_pos[1] + button_height/2),
                             (button_pos[0] + button_width/2, button_pos[1] - button_height/2)],
                            1, "White", "Green")
        canvas.draw_text("RESTART", (button_pos[0] - button_width/4, button_pos[1] + button_height/4), 24, "White")

    def hit(self, canvas, text):
        #displays randomised text responses when ship collides with asteroids
        canvas.draw_polygon((camera((self.position[0]+30,self.position[1]+20)),camera((self.position[0]+70,self.position[1]+50))),1,'white','white')
        canvas.draw_text(text, camera((self.position[0]+70,self.position[1]+60)), 28, 'white')
        hit_timer(canvas, 180)
        
class Asteroid:
    def __init__(self, img, img_centre, img_dims, position, vel, rotation):
        self.img = img
        self.img_centre = img_centre
        self.img_dims = img_dims
        self.position = position
        self.vel = vel
        self.rotation = rotation
        self.isHit = False
        self.lifespan = 0
        
    def draw(self, canvas):
        canvas.draw_image(self.img, self.img_centre, self.img_dims, camera(self.position), asteroid_scale, self.rotation)

    def update(self, canvas):
        self.position = (self.position[0] + self.vel[0], self.position[1] + self.vel[1])
        self.lifespan += 1
        self.draw(canvas)
        
class Bullet:
    def __init__(self, position, vel, rotation):
        self.position = position
        self.vel = vel
        self.rotation = rotation
        
    def draw(self, canvas):
        canvas.draw_circle(camera(self.position), bullet_radius, 1, "yellow", "red")

    def update(self, canvas):
        self.position = (self.position[0] + self.vel*math.cos(self.rotation), self.position[1] + self.vel*math.sin(self.rotation))
        self.draw(canvas)

class Interaction:
    def __init__(self, keyboard, spaceship):
        self.keyboard = keyboard
        self.booster_velocity = -8  # Initial jump velocity
        self.accel = 0.5  # Gravity acceleration
        self.max_vel = 60  # Maximum jump height
        self.friction = 0.9
        self.spaceship = spaceship
                          
    def button_clicked():
        #Create a frame and assign callbacks to event handlers
        global score
        global frame2
        score = 0
        frame2 = simplegui.create_frame("Space Fighters", CANVAS_DIMS[0], CANVAS_DIMS[1])
        frame2.set_canvas_background('#2C6A6A')
        frame2.set_draw_handler(draw)
        frame2.set_keydown_handler(keyboard.keydown_handler)
        frame2.set_keyup_handler(keyboard.keyup_handler)
        frame2.start()
        
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
        global bullets
        global asteroids
        frame1.stop()
        if (button_pos[0] - button_width / 2 < pos[0] < button_pos[0] + button_width / 2) and (button_pos[1] - button_height / 2 < pos[1] < button_pos[1] + button_height / 2):
            bullets = []
            asteroids = []
            bullet_cd.start()
            timer.start()
            Interaction.button_clicked()
    
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
            speed_x += math.cos(ship_angle) * self.booster_velocity * 0.4
            speed_y += math.sin(ship_angle) * self.booster_velocity * 0.4
            if self.booster_velocity < self.max_vel:
                self.booster_velocity += self.accel
            else:
                self.booster_velocity = -10
            self.spaceship.move(canvas)
        elif self.keyboard.down:
            self.booster_velocity = 10
            speed_x -= math.cos(ship_angle) * self.booster_velocity * 0.4
            speed_y -= math.sin(ship_angle) * self.booster_velocity * 0.4
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
        
        self.spaceship.position = (self.spaceship.position[0] + speed_x * 0.03, self.spaceship.position[1] + speed_y * 0.03)
        ship_angle %= 2 * math.pi
        if self.spaceship.position[0] < 0 or self.spaceship.position[0] > CANVAS_DIMS[0]:
            self.spaceship.position = (self.spaceship.position[0] % CANVAS_DIMS[0], self.spaceship.position[1])
        if self.spaceship.position[1] < 0 or self.spaceship.position[1] > CANVAS_DIMS[1]:
            self.spaceship.position = (self.spaceship.position[0] % CANVAS_DIMS[1], self.spaceship.position[1] % CANVAS_DIMS[1])
        speed_x -= speed_x*self.friction*0.005
        speed_y -= speed_y*self.friction*0.005

class Collisions1:
    def __init__(self):
        pass

    def update(self, canvas):
        global text
        global ship
        global asteroids
        global time_count
        safe_dist_sqr = ((ship_scale[0] + asteroid_scale[0])/2)**2
        debris = []
        for i in range(len(asteroids)):
            if (not asteroids[i].isHit):
                if (ship.position[0]-asteroids[i].position[0])**2 + (ship.position[1]-asteroids[i].position[1])**2 < safe_dist_sqr:
                    debris.append(i)
                    asteroids[i].isHit = True
                    ship.isHit = True
                    text=random.choice(["L bozo", "-1", "Checkmate in 1", "!! Brilliant move","XD"])
                    print('hit')             
                    ship.hp -=1
                    print(ship.hp)
                    #explode(canvas, asteroids[i].position)
                    ship.hit(canvas, text)
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
                        #explode(canvas, asteroids[j].position)
        for i in range(len(debris[0])):
            bullets.pop(debris[0][i])
            asteroids.pop(debris[1][i])
            
class Scoreboard:
    def __init__(self):
        pass
    def update(self, canvas):
        global score
        string = "Score: " + str(int(score))
        string2 = "Hp: " + str(int(ship.hp))
        canvas.draw_polygon([(0,0),(0,50),(180,50),(180,0)],1, 'black', 'black')
        canvas.draw_text(string,(10,19),30,"white","monospace")
        canvas.draw_text(string2,(10,40),30,"white","monospace")
# Global variables
move_x=1028
ship_angle = 0
offset = [0,0]
text=""
speed_x = speed_y = 0
keyboard = Keyboard()
ship = Spaceship(IMG1, THRUSTER_IMG1, IMG1_CENTRE, IMG1_DIMS, (CANVAS_DIMS[0]/2, CANVAS_DIMS[1]/2), 10)
interaction = Interaction(keyboard, ship)
collisions1 = Collisions1()
collisions2 = Collisions2()
scoreboard = Scoreboard()
background = Background(BACKGROUND, BACKGROUND_DIMS,5,10)
midground = Midground(MIDGROUND, MIDGROUND_DIMS)
border = Border(BORDER, BORDER_DIMS)
edge = Edge()
def bullet_cd_handler():
    global ship
    global ship_angle
    global shooting
    if shooting:
        bullets.append(Bullet(ship.position, 3, ship_angle))

def timer_handler():
    global asteroids
    if len(asteroids) < 50:
        pos = randomPos()
        vel = randomVel(pos)
        asteroids.append(Asteroid(IMG2, IMG2_CENTRE, IMG2_DIMS, pos, vel, randomRot()))
bullet_cd = simplegui.create_timer(200, bullet_cd_handler)
timer = simplegui.create_timer(2000, timer_handler)

# Drawing handler
def draw(canvas):
    global bg_counter
    global score
    bg_counter += 1
    out_range = [[], []]
    
    background.draw(canvas)
    midground.draw(canvas)
    
    for i in range(len(bullets)):
        bullets[i].update(canvas)
        if (bullets[i].position[0]-offset[0] < 0)|(bullets[i].position[0]-offset[0] > CANVAS_DIMS[0])|(bullets[i].position[1]-offset[1] < 0)|(bullets[i].position[1]-offset[1] > CANVAS_DIMS[1]):
            out_range[0].append(bullets[i])
    for i in range(len(out_range[0])):
        bullets.remove(out_range[0][i])
        
    for i in range(len(asteroids)):
        asteroids[i].update(canvas)
        if asteroids[i].lifespan > 1800:
            out_range[1].append(i)
    for i in range(len(out_range[1])):
        asteroids.pop(out_range[1][i])
    
    edge.draw(canvas)
    score += 1/30
    collisions1.update(canvas)
    collisions2.update()
    interaction.update(canvas)
    
    border.draw(canvas)
    scoreboard.update(canvas)
    ship.update(canvas)
    
    if ship.isHit:
        ship.hit(canvas, text)

    if ship.hp < 1:
        ship.hp = 10
        frame2.stop()

# Create a frame and assign callbacks to event handlers
frame1 = simplegui.create_frame("Main Menu", CANVAS_DIMS[0], CANVAS_DIMS[1])
frame1.set_canvas_background('Black')
frame1.set_draw_handler(Interaction.welcome)
frame1.set_mouseclick_handler(Interaction.mouse_handler)
frame1.start()
