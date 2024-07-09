import turtle
import random
import winsound

# Global Variables
bullet_state = "ready"  # Initialize bullet state
up_pressed = False
down_pressed = False
frog_speed = 2  # Initialize frog_speed globally
frog_frozen = False  # Flag to track if frog is currently frozen

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

bullet_speed = 20  # Increased bullet speed

# Hitbox offset
frog_hitbox_offset = 25  # Adjusted to extend slightly lower than the frog's position

def move_up_continuous():
    y = player.ycor() + 5  # Adjusted movement speed
    if y > 220:
        y = 220
    player.sety(y)

def move_down_continuous():
    y = player.ycor() - 5  # Adjusted movement speed
    if y < -220:
        y = -220
    player.sety(y)

def move_frog():
    global frog_speed, frog_frozen

    # Move the frog only if it's not frozen
    if not frog_frozen:
        new_y = frog.ycor() + frog_speed
        # Check border
        if new_y > 220:
            new_y = 220
            frog_speed *= -1
        elif new_y < -220:
            new_y = -220
            frog_speed *= -1
        
        frog.sety(new_y)

    # Schedule next movement after a short interval
    wn.ontimer(move_frog, 50)

def freeze_frog():
    global frog_frozen, frog_speed

    if not frog_frozen:
        # Freeze the frog for a random duration between 1-3 seconds
        freeze_duration = random.uniform(1, 3)
        frog_frozen = True
        frog_speed = 0

        # Schedule unfreeze after freeze_duration seconds
        wn.ontimer(unfreeze_frog, int(freeze_duration * 1000))

    # Schedule the next freeze period after a random delay between 5-20 seconds
    next_freeze_delay = random.uniform(5, 20)
    wn.ontimer(freeze_frog, int(next_freeze_delay * 1000))

def unfreeze_frog():
    global frog_frozen, frog_speed

    # Unfreeze the frog and generate a new random speed between 1 and 5
    frog_frozen = False
    new_speed = random.randint(1, 5)
    frog_speed = new_speed

def game_loop():
    global bullet_state, score

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

        # Check for collision using the distance method with adjusted hitbox offset
        # Extend hitbox slightly lower than frog's position
        if frog.isvisible() and bullet.distance(frog.xcor(), frog.ycor() - 10) < 30:  # Adjusted collision distance
            # Sound
            winsound.PlaySound('audios/death_sfx.wav', winsound.SND_ASYNC)

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

# Start the frog movement loop
move_frog()

# Start the first freeze period after a random delay between 5-20 seconds
next_freeze_delay = random.uniform(5, 20)
wn.ontimer(freeze_frog, int(next_freeze_delay * 1000))

# Start the game loop
game_loop()

turtle.done()