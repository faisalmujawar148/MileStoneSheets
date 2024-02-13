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

def draw(canvas):
    spritesheet.draw(canvas)

# Create a frame and assign callbacks to event handlers
frame = simplegui.create_frame('canvas', 600, 400)
frame.set_draw_handler(draw)
frame.set_draw_handler(draw)

# Start the frame animation
frame.start()
