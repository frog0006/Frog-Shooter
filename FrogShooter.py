import turtle
import time
import random
import winsound

# Functions
player_dx = 15

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
    winsound.PlaySound('audios/laser_sfx.wav', winsound.SND_ASYNC)
    x = player.xcor()
    y = player.ycor()
    bullet.setposition(x + 40, y)
    bullet.setheading(0)  # Set bullet heading to right
    bullet.showturtle()

# Set up window
wn = turtle.Screen()
wn.setup(width=625, height=500)
wn.title("Frog Shooter")

# Register and set background image
wn.addshape('images/lake.gif')
wn.bgpic('images/lake.gif')

# Register shapes
turtle.register_shape('images/frogcloud_img.gif')
turtle.register_shape('images/watergun_img.gif')

# Score
# Set score to be 0 initially
score = 0

# Draw score board
score_pen = turtle.Turtle()
score_pen.speed(0)
score_pen.color('black')
score_pen.up()
score_pen.setposition(-200, 210)
score_pen.write('Score: %s' % score)
score_pen.hideturtle()

# Create the player turtle
player = turtle.Turtle()
player.shape('images/watergun_img.gif')
player.up()
player.speed(0)
player.setposition(-220, 0)
player.setheading(90)

# Create player's bullet​
bullet = turtle.Turtle()
bullet.color('yellow')
bullet.shape('triangle')
bullet.up()
bullet.speed(0)
bullet.setheading(0)  # Initial bullet heading to right
bullet.shapesize(0.5, 0.5)
bullet.hideturtle()

# Create frog turtle
frog = turtle.Turtle()
frog.shape('images/frogcloud_img.gif')
frog.up()
frog.speed(0)
frog.setposition(-180, 180)

# Create keyboard binding
turtle.listen()
turtle.onkey(move_up, 'Up')
turtle.onkey(move_down, 'Down')
turtle.onkey(fire_bullet, 'space')

frog_speed = 2
bullet_speed = 10

while True:
    frog.fd(frog_speed)

    # Check border
    if frog.xcor() > 190 or frog.xcor() < -190:
        frog.right(180)
        frog.fd(frog_speed)

    # Fire the bullet
    bullet.fd(bullet_speed)

    # Check for collision
    if abs(bullet.xcor() - frog.xcor()) < 15 and abs(bullet.ycor() - frog.ycor()) < 15:
        # Sound
        winsound.PlaySound('audios/explosion_sfx.wav', winsound.SND_ASYNC)

        # Update the score
        score += 1
        score_pen.clear()
        score_pen.write('Score: %s' % score)

        # Reset frog and player
        bullet.hideturtle()
        frog.hideturtle()
        time.sleep(2)

        frog.showturtle()
        x = random.randint(-180, 180)
        frog.setposition(x, 180)

        player.setposition(-220, 0)