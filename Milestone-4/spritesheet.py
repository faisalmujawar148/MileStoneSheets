# CodeSkulptor runs Python programs in your browser.
# Click the upper left button to run this simple demo.

# CodeSkulptor is tested to run in recent versions of
# Chrome, Firefox, Safari, and Edge.

import simplegui

class Spritesheet:
    def __init__(self, image, columns, rows):
        self.image = simplegui.load_image(image)
        self.columns = columns
        self.rows = rows
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.frame_width = self.width/self.columns
        self.frame_height = self.height/self.rows
        self.frame_centre = (self.frame_width/2, self.frame_height/2)
        self.frame_index = [0,0]

    def draw(self, canvas):
        center_source = (self.frame_width*self.frame_index[0]+self.frame_centre[0], self.frame_height*self.frame_index[1]+self.frame_centre[1])
        width_height_source = (self.frame_width, self.frame_height)
        
        canvas.draw_image(self.image, center_source, width_height_source, (300, 200), (100, 100))
        
        self.next_frame()
        
    def next_frame(self):
        self.frame_index[0] += 1
        if self.frame_index[0] == self.columns:
            self.frame_index[1] += 1
            self.frame_index[0] = 0
        if self.frame_index[1] == self.rows:
            self.frame_index[1] = 0

            
spritesheet = Spritesheet('https://www.cs.rhul.ac.uk/courses/CS1830/sprites/runnerSheet.png', 6, 5)

class Clock:
    def __init__(self):
        self.time = 0
    # increments the value of time by one
    def tick(self):
        self.time += 1
        
    def transition(self, frame_duration):
        # returns a boolean that indicates if it is time to move to the next frame.
        return self.time % frame_duration == 0
        
clock = Clock()
def draw(canvas):
    if clock.transition(6):  # Change speed by modifying the frame_duration
        spritesheet.next_frame()
    spritesheet.draw(canvas)
    clock.tick()
    
# Create a frame and assign callbacks to event handlers
frame = simplegui.create_frame('canvas', 600, 400)
frame.set_draw_handler(draw)
frame.set_draw_handler(draw)

# Start the frame animation
frame.start()
