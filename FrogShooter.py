import turtle
import random
import winsound

# Global Variables
bullet_state = "ready"
up_pressed = False
down_pressed = False
frog_speed = 2
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

frog_hitbox_offset = 25

def move_up_continuous():
    y = player.ycor() + 5
    if y > 220:
        y = 220
    player.sety(y)

def move_down_continuous():
    y = player.ycor() - 5
    if y < -220:
        y = -220
    player.sety(y)

def move_frog():
    global frog_speed, frog_frozen

    if not frog_frozen:
        new_y = frog.ycor() + (frog_speed / 10)  # Smaller steps
        if new_y > 220:
            new_y = 220
            frog_speed *= -1
        elif new_y < -220:
            new_y = -220
            frog_speed *= -1
        
        frog.sety(new_y)

    wn.ontimer(move_frog, 20)  # High-frequency updates

def freeze_frog():
    global frog_frozen, frog_speed

    if not frog_frozen:
        freeze_duration = random.uniform(1, 3)
        frog_frozen = True
        frog_speed = 0

        wn.ontimer(unfreeze_frog, int(freeze_duration * 1000))

    next_freeze_delay = random.uniform(5, 20)
    wn.ontimer(freeze_frog, int(next_freeze_delay * 1000))

def unfreeze_frog():
    global frog_frozen, frog_speed

    frog_frozen = False
    new_speed = random.randint(2, 8)
    frog_speed = new_speed

def game_loop():
    global bullet_state, score

    if up_pressed:
        move_up_continuous()
    if down_pressed:
        move_down_continuous()

    if bullet_state == "fired":
        bullet.fd(bullet_speed)

        if bullet.xcor() > 300:
            bullet.hideturtle()
            bullet_state = "ready"

        if frog.isvisible() and bullet.distance(frog.xcor(), frog.ycor() - 10) < 30:
            winsound.PlaySound('audios/death_sfx.wav', winsound.SND_ASYNC)

            score += 1
            score_pen.clear()
            score_pen.write('Score: %s' % score, align='left', font=('Arial', 14, 'normal'))

            bullet.hideturtle()
            bullet_state = "ready"
            frog.hideturtle()

            frog.setposition(200, random.randint(-180, 180))
            frog.showturtle()

    wn.ontimer(game_loop, 10)

move_frog()

next_freeze_delay = random.uniform(5, 20)
wn.ontimer(freeze_frog, int(next_freeze_delay * 1000))

game_loop()

turtle.done()