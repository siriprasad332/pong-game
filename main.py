import random
from js import document, window
from pyodide.ffi import create_proxy

# Setup Canvas
canvas = document.getElementById("pongCanvas")
ctx = canvas.getContext("2d")
WIDTH, HEIGHT = canvas.width, canvas.height

# Game Constants
PADDLE_WIDTH, PADDLE_HEIGHT = 12, 90
BALL_SIZE = 12
PLAYER_SPEED = 7
AI_SPEED = 4.5

# Game State
player_y = HEIGHT // 2 - PADDLE_HEIGHT // 2
ai_y = HEIGHT // 2 - PADDLE_HEIGHT // 2
player_score = 0
ai_score = 0

ball_x = WIDTH // 2
ball_y = HEIGHT // 2
ball_dx = 5 * random.choice([-1, 1])
ball_dy = 5 * random.choice([-1, 1])

# Input State
keys = {"ArrowUp": False, "ArrowDown": False, "w": False, "s": False}

def on_keydown(event):
    if event.key in keys:
        keys[event.key] = True

def on_keyup(event):
    if event.key in keys:
        keys[event.key] = False

# Bind keyboard events
document.addEventListener("keydown", create_proxy(on_keydown))
document.addEventListener("keyup", create_proxy(on_keyup))

def reset_ball():
    global ball_x, ball_y, ball_dx, ball_dy
    ball_x = WIDTH // 2
    ball_y = HEIGHT // 2
    ball_dx = 5 * random.choice([-1, 1])
    ball_dy = 5 * random.choice([-1, 1])

def update():
    global player_y, ai_y, ball_x, ball_y, ball_dx, ball_dy, player_score, ai_score

    # Move Player Paddle
    if (keys["ArrowUp"] or keys["w"]) and player_y > 0:
        player_y -= PLAYER_SPEED
    if (keys["ArrowDown"] or keys["s"]) and player_y < HEIGHT - PADDLE_HEIGHT:
        player_y += PLAYER_SPEED

    # Move AI Paddle (tracks ball center)
    ai_center = ai_y + PADDLE_HEIGHT / 2
    if ai_center < ball_y - 10 and ai_y < HEIGHT - PADDLE_HEIGHT:
        ai_y += AI_SPEED
    elif ai_center > ball_y + 10 and ai_y > 0:
        ai_y -= AI_SPEED

    # Move Ball
    ball_x += ball_dx
    ball_y += ball_dy

    # Top and Bottom Wall Bounce
    if ball_y <= 0 or ball_y >= HEIGHT - BALL_SIZE:
        ball_dy *= -1

    # Player Paddle Collision
    if (ball_x <= 20 + PADDLE_WIDTH and 
        player_y < ball_y + BALL_SIZE and 
        player_y + PADDLE_HEIGHT > ball_y):
        ball_dx = abs(ball_dx) * 1.05  # Speed up slightly on hit

    # AI Paddle Collision
    if (ball_x + BALL_SIZE >= WIDTH - 20 - PADDLE_WIDTH and 
        ai_y < ball_y + BALL_SIZE and 
        ai_y + PADDLE_HEIGHT > ball_y):
        ball_dx = -abs(ball_dx) * 1.05

    # Scoring
    if ball_x < 0:
        ai_score += 1
        reset_ball()
    elif ball_x > WIDTH:
        player_score += 1
        reset_ball()

def draw():
    # Clear Screen
    ctx.fillStyle = "#000000"
    ctx.fillRect(0, 0, WIDTH, HEIGHT)

    # Draw Center Net
    ctx.fillStyle = "#333333"
    for y in range(0, HEIGHT, 30):
        ctx.fillRect(WIDTH // 2 - 2, y, 4, 15)

    # Draw Paddles
    ctx.fillStyle = "#00ffcc"
    ctx.fillRect(20, player_y, PADDLE_WIDTH, PADDLE_HEIGHT)  # Player
    ctx.fillRect(WIDTH - 20 - PADDLE_WIDTH, ai_y, PADDLE_WIDTH, PADDLE_HEIGHT)  # AI

    # Draw Ball
    ctx.fillStyle = "#ffffff"
    ctx.fillRect(ball_x, ball_y, BALL_SIZE, BALL_SIZE)

    # Draw Scores
    ctx.font = "40px Courier New"
    ctx.fillText(str(player_score), WIDTH // 4, 60)
    ctx.fillText(str(ai_score), 3 * WIDTH // 4, 60)

def game_loop(*args):
    update()
    draw()
    window.requestAnimationFrame(create_proxy(game_loop))

# Start the game loop
window.requestAnimationFrame(create_proxy(game_loop))