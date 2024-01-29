try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import math

w = 400
h = 400
class Ball:
    def __init__(self, position, radius=20, colour="Blue"):
        self.position = position
        self.radius = radius
        self.colour = colour

    def draw(self, canvas):
        canvas.draw_circle(self.position, self.radius, 2, self.colour, self.colour)
    def disappear(self):
        self.position=[1000,1000]


class Mouse:
    def __init__(self):
        self.click_pos = None

    def click_handler(self, pos):
        self.click_pos = pos

    def click_pos_reset(self):
        pos = self.click_pos
        self.click_pos = None
        return pos


class Interaction:
    def __init__(self, ball, mouse):
        self.ball = ball
        self.mouse = mouse

    def update(self, canvas):
        click_pos = self.mouse.click_pos_reset()
        if click_pos:
            distance = math.sqrt((click_pos[0] - self.ball.position[0])**2 + (click_pos[1] - self.ball.position[1])**2)
            if distance <= self.ball.radius:
                self.ball.disappear()
                canvas.draw_polygon([(0, 0), (w, 0), (w, h), (0, h)], 1, "Black", "Black")
            else:

                # Click is outside the ball, teleport the ball to the new location
                self.ball.position = click_pos

        # Draw the background (simulate clearing)
        canvas.draw_polygon([(0, 0), (400, 0), (400, 400), (0, 400)], 1, "Black", "Black")

        # Draw the ball on the cleared canvas
        self.ball.draw(canvas)


def draw_handler(canvas):
    interaction.update(canvas)


def click_handler(pos):
    mouse.click_handler(pos)


# Create objects
initial_ball_position = [1000, 1000]
ball = Ball(initial_ball_position)
mouse = Mouse()
interaction = Interaction(ball, mouse)

frame = simplegui.create_frame("Interactive Ball", 400, 400)
frame.set_draw_handler(draw_handler)
frame.set_mouseclick_handler(click_handler)

frame.start()
