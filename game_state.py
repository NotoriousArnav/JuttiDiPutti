import pygame
import os
import json
import config


def init_ui(game_screen, fonts):
    global screen, font, countdown_font, timer_font
    screen = game_screen
    font = fonts.get("font")
    countdown_font = fonts.get("countdown")
    timer_font = fonts.get("timer")


def save_highscore(player_name: str, score: int) -> bool:
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


def run_countdown():
    for count in range(3, 0, -1):
        screen.fill((255, 255, 255))
        count_text = countdown_font.render(str(count), True, (0, 0, 0))
        count_rect = count_text.get_rect(
            center=(
                config.current_resolution[0] // 2,
                config.current_resolution[1] // 2,
            )
        )
        screen.blit(count_text, count_rect)
        pygame.display.flip()
        pygame.time.wait(1000)

    start_text = countdown_font.render("START!", True, (0, 200, 0))
    start_rect = start_text.get_rect(
        center=(config.current_resolution[0] // 2, config.current_resolution[1] // 2)
    )
    screen.blit(start_text, start_rect)
    pygame.display.flip()
    pygame.time.wait(500)


def draw_timer(timer_font, elapsed: int, speed_multiplier: float):
    timer_surface = timer_font.render(
        f"Time: {elapsed}s  Speed: {speed_multiplier:.1f}x", True, (0, 0, 0)
    )
    screen.blit(timer_surface, (10, 10))


def show_game_over(elapsed: int, is_new_highscore: bool, font, countdown_font):
    screen.fill((0, 0, 0))
    pygame.display.flip()
    pygame.time.wait(500)

    caught_text = font.render("You were Caught", True, (255, 0, 0))
    caught_rect = caught_text.get_rect(
        center=(config.current_resolution[0] // 2, config.current_resolution[1] // 3)
    )
    screen.blit(caught_text, caught_rect)

    score_text = countdown_font.render(f"Time: {elapsed}s", True, (255, 255, 255))
    score_rect = score_text.get_rect(
        center=(config.current_resolution[0] // 2, config.current_resolution[1] // 2)
    )
    screen.blit(score_text, score_rect)

    if is_new_highscore:
        hs_text = countdown_font.render("NEW HIGHSCORE!", True, (255, 215, 0))
    else:
        hs_text = countdown_font.render(f"Best: {elapsed}s", True, (200, 200, 200))
    hs_rect = hs_text.get_rect(
        center=(
            config.current_resolution[0] // 2,
            config.current_resolution[1] // 2 + 50,
        )
    )
    screen.blit(hs_text, hs_rect)

    restart_text = font.render("Press R to Restart or Q to Quit", True, (150, 150, 150))
    restart_rect = restart_text.get_rect(
        center=(
            config.current_resolution[0] // 2,
            config.current_resolution[1] // 2 + 120,
        )
    )
    screen.blit(restart_text, restart_rect)

    pygame.display.flip()


def handle_game_over(elapsed: int, player_name: str, font, countdown_font):
    is_new_hs = save_highscore(player_name, elapsed)
    show_game_over(elapsed, is_new_hs, font, countdown_font)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True
                elif event.key == pygame.K_q:
                    pygame.quit()
                    exit()
