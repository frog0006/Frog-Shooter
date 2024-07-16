import turtle
import random
import winsound

# Global Variables
bullet_state = "ready"  # Initialize bullet state
up_pressed = False
down_pressed = False
frog_speed_x = -1  # Initialize frog_speed to move left
frog_speed_y = 2  # Initialize frog's vertical speed
frog_frozen = False  # Flag to track if frog is currently frozen
death_sound_playing = False  # Flag to track if death sound is playing
powerup_visible = False  # Flag to track if powerup is visible

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
    if bullet_state == "ready" and not death_sound_playing:
        winsound.PlaySound('audios/laser_sfx.wav', winsound.SND_ASYNC)
        x = player.xcor()
        y = player.ycor()
        bullet.setposition(x + 40, y)
        bullet.setheading(0)  # Set bullet heading to right
        bullet.showturtle()
        bullet_state = "fired"

def restart_game():
    global score, bullet_state, frog_speed_x, frog_speed_y, frog_frozen, powerup_visible
    # Reset the score
    score = 0
    score_pen.clear()
    score_pen.write('Score: %s' % score, align='left', font=('Arial', 14, 'normal'))
    # Reset player position
    player.setposition(-220, 0)
    player.setheading(90)
    # Reset bullet state
    bullet.hideturtle()
    bullet_state = "ready"
    # Reset frog state
    frog.setposition(200, 0)
    frog.showturtle()
    frog_frozen = False
    frog_speed_x = -1
    frog_speed_y = 2
    # Hide powerup
    powerup.hideturtle()
    powerup_visible = False
    # Clear any game over message
    message_pen.clear()
    # Immediately invoke the frog movement and behaviors
    move_frog()
    change_frog_speed()
    # Start the first freeze period after a short delay to ensure the frog moves first
    wn.ontimer(freeze_frog, int(random.uniform(5, 20) * 1000))
    wn.listen()

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
turtle.register_shape('images/powerup.gif')

# Score
score = 0

# Draw scoreboard
score_pen = turtle.Turtle()
score_pen.speed(0)
score_pen.color('black')
score_pen.up()
score_pen.setposition(-280, 210)
score_pen.hideturtle()
score_pen.write('Score: %s' % score, align='left', font=('Arial', 14, 'normal'))

# Draw the arrow and text under the scoreboard
arrow_pen = turtle.Turtle()
arrow_pen.speed(0)
arrow_pen.color('black')
arrow_pen.up()
arrow_pen.setposition(-250, 180)  # Position below the scoreboard, moved 30 pixels to the right
arrow_pen.hideturtle()
arrow_pen.write('Farm', align='left', font=('Arial', 14, 'normal'))
arrow_pen.setposition(-260, 190)
arrow_pen.setheading(180)  # Point the arrow to the left
arrow_pen.down()
arrow_pen.forward(30)
arrow_pen.left(135)
arrow_pen.forward(10)
arrow_pen.backward(10)
arrow_pen.right(270)
arrow_pen.forward(10)
arrow_pen.hideturtle()

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

# Create powerup turtle
powerup = turtle.Turtle()
powerup.shape('images/powerup.gif')
powerup.up()
powerup.speed(0)
powerup.hideturtle()

# Create keyboard bindings
turtle.listen()
turtle.onkeypress(move_up, 'Up')
turtle.onkeyrelease(move_up_release, 'Up')
turtle.onkeypress(move_down, 'Down')
turtle.onkeyrelease(move_down_release, 'Down')
turtle.onkeypress(fire_bullet, 'space')
turtle.onkeypress(restart_game, 'r')

bullet_speed = 10  # Bullet speed

def move_up_continuous():
    y = player.ycor() + 2  # Player speed
    if y > 220:
        y = 220
    player.sety(y)

def move_down_continuous():
    y = player.ycor() - 2  # Player speed
    if y < -220:
        y = -220
    player.sety(y)

def move_frog():
    global frog_speed_x, frog_speed_y, frog_frozen
    # Move the frog only if it's not frozen
    if not frog_frozen:
        new_x = frog.xcor() + frog_speed_x
        new_y = frog.ycor() + frog_speed_y
        # Check border
        if new_x < -300:
            frog.hideturtle()
            display_message("You Lost!", "The Frog ate all your crops!")
            return
        if new_y > 220:
            new_y = 220
            frog_speed_y *= -1
        elif new_y < -220:
            new_y = -220
            frog_speed_y *= -1
        
        frog.setx(new_x)
        frog.sety(new_y)
    # Schedule next movement after a short interval
    wn.ontimer(move_frog, 10)

message_pen = turtle.Turtle()
message_pen.speed(0)
message_pen.color('purple')
message_pen.up()
message_pen.hideturtle()

def display_message(message1, message2):
    message_pen.clear()
    message_pen.setposition(0, 210)  # Move 10 pixels down from original 220
    message_pen.color('purple')
    message_pen.write(message1, align='center', font=('Arial', 16, 'normal'))
    message_pen.setposition(0, 180)  # Move 10 pixels down from original 190
    message_pen.write(message2, align='center', font=('Arial', 16, 'normal'))
    message_pen.setposition(0, 150)  # Move 10 pixels down from the second message
    message_pen.color('dark green')
    message_pen.write('Press R to try again', align='center', font=('Arial', 14, 'normal'))

def freeze_frog():
    global frog_frozen, frog_speed_x, frog_speed_y
    if not frog_frozen:
        # Freeze the frog for a random duration between 1-3 seconds
        freeze_duration = random.uniform(1, 3)
        frog_frozen = True
        frog_speed_x = 0
        frog_speed_y = 0
        # Schedule unfreeze after freeze_duration seconds
        wn.ontimer(unfreeze_frog, int(freeze_duration * 1000))
    # Schedule the next freeze period after a random delay between 5-20 seconds
    next_freeze_delay = random.uniform(5, 20)
    wn.ontimer(freeze_frog, int(next_freeze_delay * 1000))

def unfreeze_frog():
    global frog_frozen, frog_speed_x
    # Unfreeze the frog
    frog_frozen = False
    frog_speed_x = -1

def change_frog_speed():
    global frog_speed_y
    if not frog_frozen:
        # Generate a new random vertical speed for the frog (0.5 to 1.5)
        new_speed_y = random.uniform(0.5, 1.5) * random.choice([-1, 1])
        frog_speed_y = new_speed_y
    # Schedule the next speed change after a random delay
    next_speed_change = random.uniform(3, 10) * 1000
    wn.ontimer(change_frog_speed, int(next_speed_change))

def is_collision(bullet, frog):
    # Define the frog's hitbox dimensions
    frog_width = 50
    frog_height = 50
    hitbox_offset = 20  # Offset to move the hitbox down by 20 pixels
    
    bullet_x = bullet.xcor()
    bullet_y = bullet.ycor()
    frog_x = frog.xcor()
    frog_y = frog.ycor()
    
    # Adjust the hitbox to move it 20 pixels down
    hitbox_top = frog_y - frog_height / 2 - hitbox_offset
    hitbox_bottom = frog_y + frog_height / 2 - hitbox_offset
    hitbox_left = frog_x - frog_width / 2
    hitbox_right = frog_x + frog_width / 2
    
    # Check if the bullet is within the adjusted hitbox
    if (hitbox_left < bullet_x < hitbox_right and
        hitbox_top < bullet_y < hitbox_bottom):
        return True
    return False

def is_powerup_collision(player, powerup):
    # Define the player's hitbox dimensions
    player_width = 40
    player_height = 40
    
    player_x = player.xcor()
    player_y = player.ycor()
    powerup_x = powerup.xcor()
    powerup_y = powerup.ycor()
    
    # Check if the player is within the powerup hitbox
    if (powerup_x - player_width / 2 < player_x < powerup_x + player_width / 2 and
        powerup_y - player_height / 2 < player_y < powerup_y + player_height / 2):
        return True
    return False

def respawn_frog():
    global frog_frozen, frog_speed_x
    new_x = frog.xcor() + 200
    if new_x > 300:
        new_x = 300
    new_y = random.randint(-220, 220)
    frog.setposition(new_x, new_y)
    frog.showturtle()
    frog_frozen = False
    frog_speed_x = -1

def play_death_sound():
    global death_sound_playing
    death_sound_playing = True
    winsound.PlaySound('audios/death_sfx.wav', winsound.SND_ASYNC)
    wn.ontimer(end_death_sound, 500)  # Adjust the timer to the length of the sound effect

def end_death_sound():
    global death_sound_playing
    death_sound_playing = False

def show_powerup():
    global powerup_visible
    if not powerup_visible:
        x = random.randint(-200, 200)
        y = random.randint(-200, 200)
        powerup.setposition(x, y)
        powerup.showturtle()
        powerup_visible = True
        # Hide the powerup after a certain duration (e.g., 5 seconds)
        wn.ontimer(hide_powerup, 5000)
    # Schedule the next powerup appearance after a random delay between 10-30 seconds
    wn.ontimer(show_powerup, int(random.uniform(10, 30) * 1000))

def hide_powerup():
    global powerup_visible
    powerup.hideturtle()
    powerup_visible = False

def game_loop():
    global bullet_state, score, powerup_visible
    wn.tracer(0)  # Turn off automatic screen updates

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
        # Check for collision using the new hitbox method
        if frog.isvisible() and is_collision(bullet, frog):
            # Play death sound without blocking
            play_death_sound()
            # Update the score
            score += 1
            score_pen.clear()
            score_pen.write('Score: %s' % score, align='left', font=('Arial', 14, 'normal'))
            # Reset frog and bullet
            bullet.hideturtle()
            bullet_state = "ready"
            frog.hideturtle()
            frog_frozen = True
            # Move the frog to the right by 200 pixels but not exceeding the boundary
            respawn_frog()

    # Check for powerup collision
    if powerup_visible and is_powerup_collision(player, powerup):
        # Hide the powerup and apply its effect
        powerup.hideturtle()
        powerup_visible = False
        # Apply powerup effect, e.g., increase score or player speed
        score += 5  # Example effect: increase score by 5
        score_pen.clear()
        score_pen.write('Score: %s' % score, align='left', font=('Arial', 14, 'normal'))

    wn.update()  # Update the screen with all changes
    # Repeat the game loop
    wn.ontimer(game_loop, 10)  # Update every 10 milliseconds

# Start the frog movement loop
move_frog()
# Start changing the frog's speed at random intervals
change_frog_speed()
# Start the first freeze period after a random delay between 5-20 seconds
next_freeze_delay = random.uniform(5, 20)
wn.ontimer(freeze_frog, int(next_freeze_delay * 1000))
# Start the game loop
game_loop()
# Schedule the first powerup appearance
wn.ontimer(show_powerup, 10000)  # First powerup appears after 10 seconds
turtle.done()