import turtle
import random
import winsound

# Global Variables
bullet_state = "ready"
up_pressed = False
down_pressed = False
frog_speed = 5  # Initial speed
frog_frozen = False

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
        bullet.setheading(0)
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
bullet.setheading(0)
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

bullet_speed = 20

def move_frog():
    global frog_speed, frog_frozen

    if not frog_frozen:
        new_y = frog.ycor() + frog_speed
        if new_y > 220:
            new_y = 220
            frog_speed *= -1
        elif new_y < -220:
            new_y = -220
            frog_speed *= -1
        
        frog.sety(new_y)

    wn.ontimer(move_frog, 10)

def change_frog_speed():
    global frog_speed
    frog_speed = random.randint(3, 10)
    next_speed_change = random.uniform(3, 10)
    wn.ontimer(change_frog_speed, int(next_speed_change * 1000))

def freeze_frog():
    global frog_frozen

    if not frog_frozen:
        freeze_duration = random.uniform(1, 3)
        frog_frozen = True

        wn.ontimer(unfreeze_frog, int(freeze_duration * 1000))

    next_freeze_delay = random.uniform(5, 20)
    wn.ontimer(freeze_frog, int(next_freeze_delay * 1000))

def unfreeze_frog():
    global frog_frozen
    frog_frozen = False

def move_bullet():
    global bullet_state, score

    if bullet_state == "fired":
        bullet.fd(bullet_speed)

        if bullet.xcor() > 300:
            bullet.hideturtle()
            bullet_state = "ready"

        frog_x = frog.xcor()
        frog_y = frog.ycor()
        bullet_x = bullet.xcor()
        bullet_y = bullet.ycor()

        if (frog_x - 20 < bullet_x < frog_x + 20) and (frog_y - 30 < bullet_y < frog_y + 10):
            winsound.PlaySound('audios/death_sfx.wav', winsound.SND_ASYNC)

            score += 1
            score_pen.clear()
            score_pen.write('Score: %s' % score, align='left', font=('Arial', 14, 'normal'))

            bullet.hideturtle()
            bullet_state = "ready"
            frog.hideturtle()

            frog.setposition(200, random.randint(-180, 180))
            frog.showturtle()

    wn.ontimer(move_bullet, 10)

def game_loop():
    if up_pressed:
        y = player.ycor() + 5
        if y > 220:
            y = 220
        player.sety(y)
    if down_pressed:
        y = player.ycor() - 5
        if y < -220:
            y = -220
        player.sety(y)

    wn.ontimer(game_loop, 20)  # Adjusted to 20ms for smoother movement

move_frog()

next_freeze_delay = random.uniform(5, 20)
wn.ontimer(freeze_frog, int(next_freeze_delay * 1000))

change_frog_speed()

game_loop()
move_bullet()

turtle.done()