import pygame


def move_entity(
    rect, target_x: int, target_y: int, speed: float, teleport: bool = False
):
    target = pygame.math.Vector2(target_x, target_y)
    current = pygame.math.Vector2(rect.center)

    if teleport:
        rect.center = (target_x, target_y)
    else:
        distance_vector = target - current

        if distance_vector.length() > 0:
            if distance_vector.length() <= speed:
                rect.center = (target_x, target_y)
            else:
                move_step = distance_vector.normalize() * speed
                rect.centerx += move_step.x
                rect.centery += move_step.y


def move_weapon(weapon_rect, target_x: int, target_y: int, speed: float):
    move_entity(weapon_rect, target_x, target_y, speed)


def move_parent(parent_rect, target_x: int, target_y: int, speed: float):
    move_entity(parent_rect, target_x, target_y, speed)


def check_collision(weapon_rect, x: int, y: int, radius: int = 50) -> bool:
    circle_center = pygame.math.Vector2(x, y)
    weapon_center = pygame.math.Vector2(weapon_rect.center)
    distance_vector = circle_center - weapon_center

    return (
        distance_vector.length()
        < radius + max(weapon_rect.width, weapon_rect.height) / 2
    )
