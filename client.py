from pygame import *
import random

# --- НАЛАШТУВАННЯ ---
WIDTH, HEIGHT = 800, 600
init()
screen = display.set_mode((WIDTH, HEIGHT))
clock = time.Clock()
display.set_caption("Ping Pong vs Bot")

# --- ПЛАТФОРМИ ---
player_y = HEIGHT // 2 - 50
bot_y = HEIGHT // 2 - 50

PADDLE_SPEED = 7
BOT_SPEED = 4

# --- М'ЯЧ ---
ball_x, ball_y = WIDTH // 2, HEIGHT // 2
ball_dx = random.choice([-5, 5])
ball_dy = random.choice([-4, 4])

# --- РАХУНОК ---
player_score = 0
bot_score = 0

# --- ШРИФТ ---
font_main = font.Font(None, 36)

# --- НАПРЯМОК РУХУ БОТА ---
bot_direction = 1  # 1 = вниз, -1 = вгору

# --- ГОЛОВНИЙ ЦИКЛ ---
while True:
    for e in event.get():
        if e.type == QUIT:
            quit()

    # --- КЕРУВАННЯ ГРАВЦЯ ---
    keys = key.get_pressed()
    if keys[K_w] and player_y > 0:
        player_y -= PADDLE_SPEED
    if keys[K_s] and player_y < HEIGHT - 100:
        player_y += PADDLE_SPEED

    # --- БОТ РУХАЄТЬСЯ ---
    error = random.randint(-20, 20)  # помилки бота
    target_y = ball_y + error

    if bot_y + 50 < target_y:
        bot_y += BOT_SPEED
    elif bot_y + 50 > target_y:
        bot_y -= BOT_SPEED

    # Додатковий рух, щоб бот не стояв
    bot_y += bot_direction
    if bot_y <= 0 or bot_y >= HEIGHT - 100:
        bot_direction *= -1

    # --- РУХ М'ЯЧА ---
    ball_x += ball_dx
    ball_y += ball_dy

    if ball_y <= 0 or ball_y >= HEIGHT:
        ball_dy *= -1

    # --- ВІДБИТТЯ ---
    if 20 < ball_x < 40 and player_y < ball_y < player_y + 100:
        ball_dx *= -1
    if WIDTH - 40 < ball_x < WIDTH - 20 and bot_y < ball_y < bot_y + 100:
        ball_dx *= -1

    # --- ГОЛ ---
    if ball_x < 0:
        bot_score += 1
        ball_x, ball_y = WIDTH // 2, HEIGHT // 2
    if ball_x > WIDTH:
        player_score += 1
        ball_x, ball_y = WIDTH // 2, HEIGHT // 2

    # --- МАЛЮВАННЯ ---
    back = image.load("back.jpg")
    back = transform.scale(back, (800, 600))
    screen.blit(back, (0, 0))
    draw.rect(screen, (0, 255, 0), (20, player_y, 20, 100))
    draw.rect(screen, (255, 0, 255), (WIDTH - 40, bot_y, 20, 100))
    draw.circle(screen, (255, 255, 255), (ball_x, ball_y), 10)

    score = font_main.render(f"{player_score} : {bot_score}", True, (255, 255, 255))
    screen.blit(score, (WIDTH // 2 - 20, 20))

    display.update()
    clock.tick(60)