import pygame
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
import config

from assets import load_image, load_music
from entities import move_parent, move_weapon, check_collision
from game_state import init_ui, run_countdown, draw_timer, handle_game_over


# ==================== GLOBAL STATE ====================
screen = None
clock = None
font = None
countdown_font = None
timer_font = None

weapon = None
weapon_rect = None
child = None
child_rect = None
parent = None
parent_rect = None

elapsed_ms = 0


# ==================== INITIALIZATION ====================
def init_pygame():
    global screen, clock, font, countdown_font, timer_font

    pygame.init()
    pygame.mixer.init()

    screen = pygame.display.set_mode(config.current_resolution)
    clock = pygame.time.Clock()

    load_music("assets/background.wav", volume=config.current_volume)

    font = pygame.font.SysFont("Arial", 50)
    countdown_font = pygame.font.SysFont("Arial", 120)
    timer_font = pygame.font.SysFont("Arial", 36)

    init_ui(
        screen,
        {
            "font": font,
            "countdown": countdown_font,
            "timer": timer_font,
        },
    )


def load_assets():
    global weapon, weapon_rect, child, child_rect, parent, parent_rect

    child = load_image(config.current_child_face, (588 / 8, 598 / 8))
    child_rect = child.get_rect()

    parent = load_image(config.current_parent_face, (547 / 5, 457 / 5))
    parent_rect = parent.get_rect()

    weapon = load_image(config.current_weapon, (50, 100))
    weapon_rect = weapon.get_rect()


def reset_positions():
    parent_rect.center = config.SPAWN
    weapon_rect.center = config.SPAWN


# ==================== RENDER ====================
def render_game():
    screen.fill((255, 255, 255))
    screen.blit(weapon, weapon_rect)
    screen.blit(parent, parent_rect)
    screen.blit(child, child_rect)


# ==================== MAIN GAME LOOP ====================
def run_game(player_name: str = "Player"):
    global elapsed_ms

    diff_settings = config.current_difficulty
    parent_speed = diff_settings["parent_speed"]
    weapon_speed = diff_settings["slipper_speed"]
    weapon_offset = diff_settings["offset"]
    start_multiplier = diff_settings.get("start_multiplier", 1.0)

    reset_positions()
    run_countdown()
    elapsed_ms = 0
    speed_multiplier = start_multiplier

    while True:
        dt = clock.tick(config.FPS)
        elapsed_ms += dt

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                return

        mouse_x, mouse_y = pygame.mouse.get_pos()

        elapsed = elapsed_ms // 1000
        # After 30 seconds, increase speed by 0.1x per second (starts from start_multiplier)
        speed_multiplier = start_multiplier + (elapsed / 100)

        move_parent(parent_rect, mouse_x, mouse_y, parent_speed * speed_multiplier)

        weapon_target_x = parent_rect.centerx - weapon_offset
        weapon_target_y = parent_rect.centery
        move_weapon(
            weapon_rect,
            weapon_target_x,
            weapon_target_y,
            weapon_speed * speed_multiplier,
        )

        if check_collision(weapon_rect, mouse_x, mouse_y):
            elapsed = elapsed_ms // 1000
            if handle_game_over(elapsed, player_name, font, countdown_font):
                reset_positions()
                run_countdown()
                elapsed_ms = 0
                continue
            return

        render_game()
        child_rect.center = (mouse_x, mouse_y)
        draw_timer(timer_font, elapsed, speed_multiplier)
        pygame.display.flip()


def main():
    from launcher import show_launcher

    settings = show_launcher()
    if not settings or settings.get("action") != "start":
        return

    config.apply_settings(settings)
    player_name = settings.get("player_name", "Player")

    init_pygame()
    load_assets()
    run_game(player_name)
    pygame.quit()


if __name__ == "__main__":
    main()
