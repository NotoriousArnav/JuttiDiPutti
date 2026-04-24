import pygame
import os
import config
from PIL import Image


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
    pygame.mixer.music.set_volume(volume)


def convert_to_png(input_path: str, output_dir: str) -> str:
    """Convert image to PNG using PIL if not already PNG"""
    input_ext = os.path.splitext(input_path)[1].lower()

    if input_ext == ".png":
        return input_path

    if input_ext in [".jpg", ".jpeg", ".bmp", ".gif", ".tiff", ".webp"]:
        filename = os.path.basename(input_path)
        name_without_ext = os.path.splitext(filename)[0]
        output_path = os.path.join(output_dir, f"{name_without_ext}.png")

        if not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)

        with Image.open(input_path) as img:
            img = img.convert("RGBA")
            img.save(output_path, "PNG")

        return output_path

    return input_path


def load_image(filename: str, scale: tuple = None):
    if not os.path.exists(filename):
        return None

    converted_path = convert_to_png(filename, "assets/converted")

    if converted_path != filename and converted_path:
        filename = converted_path

    try:
        image = pygame.image.load(filename).convert_alpha()
        if scale:
            image = pygame.transform.scale(image, scale)
        return image
    except pygame.error:
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
