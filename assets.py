import pygame
import os
import config


def load_sound(filename: str):
    if os.path.exists(filename):
        sound = pygame.mixer.Sound(filename)
        return sound
    return None


def load_music(filename: str, volume: float = 0.5, loops: int = -1):
    if os.path.exists(filename):
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play(loops)
        pygame.mixer.music.set_volume(volume)


def set_volume(volume: float):
    """Set music volume (0.0 to 1.0)"""
    pygame.mixer.music.set_volume(volume)


def load_image(filename: str, scale: tuple = None):
    if os.path.exists(filename):
        image = pygame.image.load(filename).convert_alpha()
        if scale:
            image = pygame.transform.scale(image, scale)
        return image
    return None


def load_game_assets(
    child_face_path: str = None, parent_face_path: str = None, weapon_path: str = None
):
    """Load game assets using configurable paths"""

    # Use provided paths or fall back to config
    child_path = child_face_path or config.current_child_face
    parent_path = parent_face_path or config.current_parent_face
    weapon_path = weapon_path or config.current_weapon

    # Scale factors (from original code)
    child_scale = (588 / 8, 598 / 8)
    parent_scale = (547 / 5, 457 / 5)
    weapon_scale = (50, 100)

    child = load_image(child_path, child_scale)
    parent = load_image(parent_path, parent_scale)
    weapon = load_image(weapon_path, weapon_scale)

    return child, parent, weapon


def get_child_rect(child):
    return child.get_rect()


def get_parent_rect(parent):
    return parent.get_rect()


def get_weapon_rect(weapon):
    return weapon.get_rect()
