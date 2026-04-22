import pygame
import os
import json

### GAME MENU SHOULD BE IMPLEMENTED HERE WITH GTK/QT
### #

Player_Name: str = "Player"

pygame.init()
pygame.mixer.init()

RES = (int(os.getenv("RES_WIDTH", 800)), int(os.getenv("RES_HEIGHT", 600)))

screen = pygame.display.set_mode(RES)

pygame.mixer.music.load("assets/background.wav")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.5)

slipper = pygame.transform.scale(
    pygame.image.load("assets/slipper.png").convert_alpha(), (50, 100)
)

slipper_rect = slipper.get_rect()

# 588 598
child = pygame.transform.scale(
    pygame.image.load("faces/child.png").convert_alpha(), (588 / 8, 598 / 8)
)

# 547 457
parent = pygame.transform.scale(
    pygame.image.load("faces/parent.png").convert_alpha(), (547 / 5, 457 / 5)
)

child_rect = child.get_rect()
parent_rect = parent.get_rect()

spawn = (0, 0)

parent_rect.center = spawn
slipper_rect.center = spawn

font = pygame.font.SysFont("Arial", 50)
countdown_font = pygame.font.SysFont("Arial", 120)
timer_font = pygame.font.SysFont("Arial", 36)

text_surface = font.render("You were Caught", True, (255, 0, 0))
timer_surface = timer_font.render("Time: 0s", True, (0, 0, 0))

speed_multiplier = 1.0

text_rect = text_surface.get_rect(center=(400, 300))


def run_countdown():
    for count in range(3, 0, -1):
        screen.fill((255, 255, 255))
        count_text = countdown_font.render(str(count), True, (0, 0, 0))
        count_rect = count_text.get_rect(center=(RES[0] // 2, RES[1] // 2))
        screen.blit(count_text, count_rect)
        pygame.display.flip()
        pygame.time.wait(1000)

    start_text = countdown_font.render("START!", True, (0, 200, 0))
    start_rect = start_text.get_rect(center=(RES[0] // 2, RES[1] // 2))
    screen.blit(start_text, start_rect)
    pygame.display.flip()
    pygame.time.wait(500)


def moveSlipper(x: int, y: int, speed: int = 5, tp: bool = False):
    global slipper_rect

    target = pygame.math.Vector2(x, y)
    current = pygame.math.Vector2(slipper_rect.center)

    if tp:
        slipper_rect.center = (x, y)
    else:
        distance_vector = target - current

        if distance_vector.length() > 0:
            if distance_vector.length() <= speed:
                slipper_rect.center = (x, y)
            else:
                move_step = distance_vector.normalize() * speed

                slipper_rect.centerx += move_step.x
                slipper_rect.centery += move_step.y


def moveParent(x: int, y: int, speed: int = 5, tp: bool = False):
    global parent_rect

    target = pygame.math.Vector2(x, y)
    current = pygame.math.Vector2(parent_rect.center)

    if tp:
        parent_rect.center = (x, y)
    else:
        distance_vector = target - current

        if distance_vector.length() > 0:
            if distance_vector.length() <= speed:
                parent_rect.center = (x, y)
            else:
                move_step = distance_vector.normalize() * speed

                parent_rect.centerx += move_step.x
                parent_rect.centery += move_step.y


def checkSlipperCollision(x: int, y: int, radius: int = 50):
    global slipper_rect

    circle_center = pygame.math.Vector2(x, y)
    slipper_center = pygame.math.Vector2(slipper_rect.center)

    distance_vector = circle_center - slipper_center

    if (
        distance_vector.length()
        < radius + max(slipper_rect.width, slipper_rect.height) / 2
    ):
        return True
    return False


def save_highscore(player_name: str, score: int):
    filepath = "highscore.json"

    highscores = {}
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            highscores = json.load(f)

    existing_score = highscores.get(player_name, 0)

    if score > existing_score:
        highscores[player_name] = score
        with open(filepath, "w") as f:
            json.dump(highscores, f, indent=2)
        return True
    return False


def show_game_over(elapsed: int, is_new_highscore: bool):
    screen.fill((0, 0, 0))
    pygame.display.flip()
    pygame.time.wait(500)

    caught_text = font.render("You were Caught", True, (255, 0, 0))
    caught_rect = caught_text.get_rect(center=(RES[0] // 2, RES[1] // 3))
    screen.blit(caught_text, caught_rect)

    score_text = timer_font.render(f"Time: {elapsed}s", True, (255, 255, 255))
    score_rect = score_text.get_rect(center=(RES[0] // 2, RES[1] // 2))
    screen.blit(score_text, score_rect)

    if is_new_highscore:
        hs_text = timer_font.render("NEW HIGHSCORE!", True, (255, 215, 0))
        hs_rect = hs_text.get_rect(center=(RES[0] // 2, RES[1] // 2 + 50))
        screen.blit(hs_text, hs_rect)
    else:
        hs_text = timer_font.render(f"Best: {elapsed}s", True, (200, 200, 200))
        hs_rect = hs_text.get_rect(center=(RES[0] // 2, RES[1] // 2 + 50))
        screen.blit(hs_text, hs_rect)

    restart_text = font.render("Press R to Restart or Q to Quit", True, (150, 150, 150))
    restart_rect = restart_text.get_rect(center=(RES[0] // 2, RES[1] // 2 + 120))
    screen.blit(restart_text, restart_rect)

    pygame.display.flip()


caught = False

run_countdown()
start_time = pygame.time.get_ticks()
game_started = True

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            break
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                break

    screen.fill((255, 255, 255))

    screen.blit(slipper, slipper_rect)
    screen.blit(parent, parent_rect)

    mouse_x, mouse_y = pygame.mouse.get_pos()

    moveParent(mouse_x, mouse_y, speed=1.6 * speed_multiplier)

    slipper_target_x = parent_rect.centerx - 60
    slipper_target_y = parent_rect.centery - 55
    moveSlipper(slipper_target_x, slipper_target_y, speed=2 * speed_multiplier)

    if checkSlipperCollision(mouse_x, mouse_y):
        elapsed = (pygame.time.get_ticks() - start_time) // 1000
        is_new_hs = save_highscore(Player_Name, elapsed)
        show_game_over(elapsed, is_new_hs)

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        waiting = False
                        parent_rect.center = spawn
                        slipper_rect.center = spawn
                        run_countdown()
                        start_time = pygame.time.get_ticks()
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        exit()

    screen.blit(child, child_rect)
    child_rect.center = (mouse_x, mouse_y)

    elapsed = (pygame.time.get_ticks() - start_time) // 1000
    speed_multiplier = 1.0 + (elapsed / 100.0)

    timer_surface = timer_font.render(
        f"Time: {elapsed}s  Speed: {speed_multiplier:.1f}x", True, (0, 0, 0)
    )
    screen.blit(timer_surface, (10, 10))

    pygame.display.flip()

pygame.quit()
