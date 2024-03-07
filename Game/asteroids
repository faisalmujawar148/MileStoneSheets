try:
  import simplegui
except ImportError:
  import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import random
import math
# Some constants
CANVAS_DIMS = (600, 400)
ship_angle = 0
IMG1 = simplegui.load_image('https://opengameart.org/sites/default/files/ship5.png')
IMG1_CENTRE = (183, 152)
IMG1_DIMS = (366, 204)

IMG2 = simplegui.load_image('')
IMG2_CENTRE = (, )
IMG2_DIMS = (, )

asteroids = []

def randomVel():
  x = random.randInt(-1,-5)
  y = random.randInt(-2,2)
  return (x,y)

def randomPos():
  x = 600
  y = random.randInt(0,400)
  return (x,y)

def randomRot():
  rot = random.randInt(-5, 5)
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

class asteroid:
  def __init__(self, img, img_centre, img_dims, position, vel, rotation):
      self.img = img
      self.img_centre = img_centre
      self.img_dims = img_dims
      self.position = position
      self.vel = vel
      self.rotation = rotation

def draw(self):
    canvas.draw_image(self.img, self.img_centre, self.img_dims, self.position, (20, 20), self.rotation)

def update(self, index):
    global asteroids
    self.position += self.vel
    if self.position < 0:
      asteroids.remove(index)


class Interaction:
  def __init__(self, keyboard, spaceship):
      self.keyboard = keyboard
      self.booster_velocity = -8  # Initial jump velocity
      self.accel = 0.5  # Gravity acceleration
      self.max_vel = 100  # Maximum jump height
      self.friction = 10

  def update(self):
      global ship_angle
      global speed_x
      global speed_y
      if self.keyboard.left:
              ship_angle-=10*0.01
      elif self.keyboard.right:
              ship_angle+=10*0.01
      elif self.keyboard.up:
              self.booster_velocity = -10
              speed_x+= math.cos(ship_angle) * self.booster_velocity *0.3
              speed_y+= math.sin(ship_angle) * self.booster_velocity *0.3
              if self.booster_velocity < self.max_vel:
                  self.booster_velocity += self.accel
              else:
                  self.booster_velocity = 10

      spaceship.position[0]+=speed_x*0.03
      spaceship.position[1]+=speed_y*0.03
      ship_angle %= 2 * math.pi
      if spaceship.position[0] % CANVAS_DIMS[0]:
          spaceship.position[0] = spaceship.position[0]%CANVAS_DIMS[0]
      if spaceship.position[1] % CANVAS_DIMS[1]:
          spaceship.position[1] = spaceship.position[1] % CANVAS_DIMS[1]
      speed_x,speed_y-=self.friction


# Global variables
ship_pos = [CANVAS_DIMS[0]/2, 2*CANVAS_DIMS[1]/3]
ship_angle = 0
speed_x=speed_y=0
keyboard = Keyboard()
ship = spaceship(IMG1 IMG1_CENTRE, IMG1_DIMS, (60, 200), 10)
interaction = Interaction(keyboard, ship)

def timer_handler():
  global asteroids
  if len(asteroids) < 30:
      asteroids.append(asteroid(IMG2, IMG2_CENTRE, IMG2_DIMS, randomPos(), randomVel(), randomRot()))

timer = simplegui.create_timer(3000, timer_handler)
timer.start()

# Drawing handler
def draw(canvas):
  interaction.update()
  for i in range(len(asteroids)):
      asteroids[i].update(i)
      collision[i].update()

# Create a frame and assign callbacks to event handlers
frame = simplegui.create_frame("A wheel", CANVAS_DIMS[0], CANVAS_DIMS[1])
frame.set_canvas_background('#2C6A6A')
frame.set_draw_handler(draw)
frame.set_keydown_handler(keyboard.keydown_handler)
frame.set_keyup_handler(keyboard.keyup_handler)


# Start the frame animation
frame.start()
