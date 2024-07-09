import turtle
import random
import winsound

# Global Variables
player_dx = 15
bullet_state = "ready"  # Initialize bullet state
up_pressed = False
down_pressed = False

def move_up():
    global up_pressed
    up_pressed = True

def move_up_release():
    global up_pressed
    up_pressed = False

def move_down():
    global down_pressed
    down_pressed = True

def move_down_release():
    global down_pressed
    down_pressed = False

def fire_bullet():
    global bullet_state
    if bullet_state == "ready":
        winsound.PlaySound('audios/laser_sfx.wav', winsound.SND_ASYNC)
        x = player.xcor()
        y = player.ycor()
        bullet.setposition(x + 40, y)
        bullet.setheading(0)  # Set bullet heading to right
        bullet.showturtle()
        bullet_state = "fired"

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
score_pen.hideturtle()
score_pen.write('Score: %s' % score, align='left', font=('Arial', 14, 'normal'))

# Create the player turtle
player = turtle.Turtle()
player.shape('images/watergun_img.gif')
player.up()
player.speed(0)
player.setposition(-220, 0)
player.setheading(90)

# Create player's bullet
bullet = turtle.Turtle()
bullet.color('blue')
bullet.shape('triangle')
bullet.shapesize(stretch_wid=0.2, stretch_len=1.5)
bullet.up()
bullet.speed(0)
bullet.setheading(0)  # Initial bullet heading to right
bullet.hideturtle()

# Create frog turtle
frog = turtle.Turtle()
frog.shape('images/frogcloud_img.gif')
frog.up()
frog.speed(0)
frog.setposition(200, 0)

# Create keyboard binding
turtle.listen()
turtle.onkeypress(move_up, 'Up')
turtle.onkeyrelease(move_up_release, 'Up')
turtle.onkeypress(move_down, 'Down')
turtle.onkeyrelease(move_down_release, 'Down')
turtle.onkey(fire_bullet, 'space')

frog_speed = 2
bullet_speed = 20  # Increased bullet speed

# Hitbox offset
frog_hitbox_offset = 10

def game_loop():
    global bullet_state, score, frog_speed, bullet_speed

    # Move the frog based on its speed
    frog.sety(frog.ycor() + frog_speed)

    # Check border
    if frog.ycor() > 220 or frog.ycor() < -220:
        frog_speed *= -1  # Change direction

    # Move the player
    if up_pressed:
        move_up_continuous()
    if down_pressed:
        move_down_continuous()

    # Move the bullet
    if bullet_state == "fired":
        bullet.fd(bullet_speed)

        # Check if the bullet goes off screen
        if bullet.xcor() > 300:
            bullet.hideturtle()
            bullet_state = "ready"

        # Check for collision using the distance method with hitbox offset
        if bullet.distance(frog.xcor(), frog.ycor() - frog_hitbox_offset) < 30:  # Adjusted collision distance
            # Sound
            winsound.PlaySound('audios/explosion_sfx.wav', winsound.SND_ASYNC)

            # Update the score
            score += 1
            score_pen.clear()
            score_pen.write('Score: %s' % score, align='left', font=('Arial', 14, 'normal'))

            # Reset frog and bullet
            bullet.hideturtle()
            bullet_state = "ready"
            frog.hideturtle()

            frog.setposition(200, random.randint(-180, 180))
            frog.showturtle()

    # Repeat the game loop
    wn.ontimer(game_loop, 10)

def move_up_continuous():
    y = player.ycor() + 15
    if y > 220:
        y = 220
    player.sety(y)

def move_down_continuous():
    y = player.ycor() - 15
    if y < -220:
        y = -220
    player.sety(y)

# Start the game loop
game_loop()

turtle.done()