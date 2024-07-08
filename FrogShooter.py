import turtle
import time
import random
import winsound

#Define functions
def move_up():
    y = player.ycor() + 15
    if y > 220:
        y = 220
    player.sety(y)

def move_down():
    y = player.ycor() - 15
    if y < -220:
        y = -220
    player.sety(y)

def fire_bullet():
    x = player.xcor()
    y = player.ycor()
    bullet.setposition(x+50,y)
    bullet.showturtle()

# Set up the screen
wn = turtle.Screen()
wn.setup(width=625, height=500)
wn.title("Frog Shooter")

# Register and set background image
wn.addshape('images/lake.gif')
wn.bgpic('images/lake.gif')

#Register player and target
turtle.register_shape('images/frogcloud_img.gif')
turtle.register_shape('images/watergun_img.gif')

#Create the player turtle
player = turtle.Turtle()
player.shape('images/watergun_img.gif')
player.up()
player.speed(0)
player.setposition(-270, 0)
player.setheading(90)

#Create the player's watergun bullet
bullet = turtle.Turtle()
bullet.color('blue')
bullet.shape('triangle')
bullet.up()
bullet.speed(0)
bullet.setheading(90)
bullet.shapesize(0.5, 0.5)
bullet.hideturtle()

#Create keybinds
turtle.listen()
turtle.onkey(move_up, 'Up')
turtle.onkey(move_down, 'Down')
turtle.onkey(fire_bullet, 'space')

bullet_speed = 10
while True:
    bullet.fd(bullet_speed)


# Main loop
wn.mainloop()