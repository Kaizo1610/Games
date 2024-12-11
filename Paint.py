import turtle

# Setup turtle window
screen = turtle.Screen()
screen.title("Simple Paint Program")
screen.setup(width=800, height=600)
screen.bgcolor("white")

# Create the turtle (pen) for drawing
pen = turtle.Turtle()
pen.shape("circle")
pen.speed(0)
pen.pensize(3)

# Variables to track drawing state
drawing = False
pen_color = "black"
pen_size = 3
colors = ["black", "red", "green", "blue", "orange", "purple"]

# Color index to change the pen color
color_index = 0

# Function to start drawing when left mouse button is clicked
def start_drawing(x, y):
    global drawing
    pen.penup()
    pen.goto(x, y)
    pen.pendown()
    drawing = True

# Function to stop drawing when the mouse button is released
def stop_drawing(x, y):
    global drawing
    drawing = False
    pen.penup()

# Function to change the color when the right mouse button is clicked
def change_color(x, y):
    global color_index, pen_color
    color_index = (color_index + 1) % len(colors)  # Cycle through colors
    pen_color = colors[color_index]
    pen.pencolor(pen_color)

# Function to clear the screen when the middle mouse button is clicked
def clear_screen(x, y):
    pen.clear()

# Function to increase pen size with the Up arrow
def increase_pen_size():
    global pen_size
    pen_size += 1
    pen.pensize(pen_size)

# Function to decrease pen size with the Down arrow
def decrease_pen_size():
    global pen_size
    if pen_size > 1:  # Avoid setting pen size below 1
        pen_size -= 1
        pen.pensize(pen_size)

# Function to handle mouse dragging (for drawing)
def draw(x, y):
    if drawing:
        pen.goto(x, y)

# Bind the events to the screen
screen.listen()
screen.onscreenclick(start_drawing, btn=1)  # Left click to start drawing
screen.onscreenclick(change_color, btn=3)   # Right click to change color
screen.onscreenclick(clear_screen, btn=2)   # Middle click to clear the screen
screen.onkey(increase_pen_size, "Up")       # Up arrow to increase pen size
screen.onkey(decrease_pen_size, "Down")     # Down arrow to decrease pen size

# Bind dragging to the pen instead of screen
pen.ondrag(draw)                            # Mouse drag to draw

# Keep the window open
screen.mainloop()
