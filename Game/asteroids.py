try:
  import simplegui
except ImportError:
  import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import random
import math
#Some constants
CANVAS_DIMS = (600, 400)
ship_angle = 0
IMG1 = simplegui.load_image('https://opengameart.org/sites/default/files/ship5.png')
IMG1_CENTRE = (183, 152)
IMG1_DIMS = (366, 204)
ship_scale = (36.6, 20.4)

IMG2 = simplegui.load_image('https://images.freeimages.com/vhq/images/previews/e23/asteroid-97287.png?fmt=webp&w=500')
IMG2_CENTRE = (250, 250)
IMG2_DIMS = (500,500)
asteroid_scale = (20, 20)

asteroids = []

def randomVel():
  x = random.randint(-1,-5)
  y = random.randint(-2,2)
  return (x,y)

def randomPos():
  x = 600
  y = random.randint(0,400)
  return (x,y)

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

class Asteroid:
  def __init__(self, img, img_centre, img_dims, position, vel, rotation):
      self.img = img
      self.img_centre = img_centre
      self.img_dims = img_dims
      self.position = position
      self.vel = vel
      self.rotation = rotation
      self.isHit = False

  def draw(self):
      canvas.draw_image(self.img, self.img_centre, self.img_dims, self.position, asteroid_scale, self.rotation)

  def explode(self, spaceship, index):
    #insert explosion animation
    spaceship.hp -= 1
    asteroids.remove(index)
    spaceship.hit()
    

  def update(self, index):
      self.position[0] += self.vel[0]
      self.position[1] += self.vel[1]
      if self.position[0] < 0:
        asteroids.remove(index)
      draw(canvas)

class Spaceship:
  def __init__(self, img, img_centre, img_dims, position, rotation, hp):
    self.img = img
    self.img_centre = img_centre
    self.img_dims = img_dims
    self.position = position
    self.rotation = rotation
    self.hp = hp

  def draw(self):
    canvas.draw_image(self.img, self.img_centre, self.img_dims, self.position, ship_scale, self.rotation)

  def hit(self):
    pass

  def death(self):
    pass

class Collisions:
  def __init__(self, spaceship):
    self.ship = spaceship
  def update(self):
    global asteroids
    safe_x = ship_scale[0] + asteroid_scale[0]
    safe_y = ship_scale[1] + asteroid_scale[1]
    for i in range(len(asteroids)):
      if (not asteroids[i].isHit) and ((asteroids[i].position[0]-ship.position[0]) < safe_x) and ((asteroids[i].position[1]-ship.position[1]) < safe_y):
        asteroids[i].isHit = True
        asteroids[i].explode(ship, i)
    
class Interaction:
  def __init__(self, keyboard):
      self.keyboard = keyboard
      self.booster_velocity = -8  # Initial jump velocity
      self.accel = 0.5  # Gravity acceleration
      self.max_vel = 100  # Maximum jump height
      self.friction = 0.9

  def update(self):
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
ship_pos = [CANVAS_DIMS[0]/2, 2*CANVAS_DIMS[1]/3]
ship = Spaceship(IMG1, IMG1_CENTRE, IMG1_DIMS, (60, 200), 0, 10)
collisions = Collisions(ship)


def timer_handler():
  global asteroids
  if len(asteroids) < 30:
      asteroids.append(Asteroid(IMG2, IMG2_CENTRE, IMG2_DIMS, randomPos(), randomVel(), randomRot()))

timer = simplegui.create_timer(3000, timer_handler)
timer.start()

# Drawing handler
def draw(canvas):
  collisions.update()
  interaction.update()
  for i in range(len(asteroids)):
      asteroids[i].update(i)

# Create a frame and assign callbacks to event handlers
frame = simplegui.create_frame("canvas", CANVAS_DIMS[0], CANVAS_DIMS[1])
frame.set_canvas_background('#2C6A6A')
frame.set_draw_handler(draw)
frame.set_keydown_handler(keyboard.keydown_handler)
frame.set_keyup_handler(keyboard.keyup_handler)


# Start the frame animation
frame.start()
