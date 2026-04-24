# ==================== CONFIG ====================
import os
import json

# Settings file path
SETTINGS_FILE = "settings.json"

# Player
Player_Name: str = os.getenv("PLAYER_NAME", "Player")

# Resolution
RES = (int(os.getenv("RES_WIDTH", 800)), int(os.getenv("RES_HEIGHT", 600)))
RESOLUTIONS = ["800x600", "1024x768", "1280x720", "1920x1080"]

# FPS
FPS = 60

# Difficulty Settings (name: {parent_speed, slipper_speed, offset, start_multiplier})
DIFFICULTIES = {
    "Easy": {
        "parent_speed": 1.5,
        "slipper_speed": 1.8,
        "offset": 80,
        "start_multiplier": 1.0,
    },
    "Medium": {
        "parent_speed": 2.0,
        "slipper_speed": 2.4,
        "offset": 60,
        "start_multiplier": 1.5,
    },
    "Hard": {
        "parent_speed": 2.8,
        "slipper_speed": 3.2,
        "offset": 40,
        "start_multiplier": 3.0,
    },
    "Impossible": {
        "parent_speed": 6.0,
        "slipper_speed": 8.0,
        "offset": 10,
        "start_multiplier": 10.0,
    },
}
DEFAULT_DIFFICULTY = "Medium"

# Asset directories
CHILD_FACES_DIR = "faces/"
PARENT_FACES_DIR = "faces/"
WEAPONS_DIR = "assets/"

# Default assets
DEFAULT_CHILD_FACE = "faces/child.png"
DEFAULT_PARENT_FACE = "faces/parent.png"
DEFAULT_WEAPON = "assets/slipper.png"
DEFAULT_MUSIC = "assets/background.wav"
MUSIC_DIR = "assets/"

# Audio
MUSIC_VOLUME = 0.5
MUSIC_ENABLED = True

# Spawn
SPAWN = (0, 0)


# ==================== SETTINGS PERSISTENCE ====================
def get_settings_path():
    return os.path.join(os.path.dirname(__file__), SETTINGS_FILE)


def load_settings():
    """Load settings from JSON file, return defaults if not exists"""
    defaults = {
        "player_name": "Player",
        "difficulty": DEFAULT_DIFFICULTY,
        "resolution": "800x600",
        "volume": 0.5,
        "music_enabled": True,
        "music": DEFAULT_MUSIC,
        "child_face": DEFAULT_CHILD_FACE,
        "parent_face": DEFAULT_PARENT_FACE,
        "weapon": DEFAULT_WEAPON,
    }

    path = get_settings_path()
    if os.path.exists(path):
        try:
            with open(path, "r") as f:
                loaded = json.load(f)
                # Merge with defaults to ensure all keys exist
                return {**defaults, **loaded}
        except (json.JSONDecodeError, IOError):
            return defaults
    return defaults


def save_settings(settings: dict):
    """Save settings to JSON file"""
    path = get_settings_path()
    try:
        with open(path, "w") as f:
            json.dump(settings, f, indent=2)
    except IOError:
        pass  # Silently fail if can't save


# ==================== CURRENT RUNTIME VALUES ====================
# These are set at runtime from launcher settings
current_difficulty = DIFFICULTIES[DEFAULT_DIFFICULTY]
current_child_face = DEFAULT_CHILD_FACE
current_parent_face = DEFAULT_PARENT_FACE
current_weapon = DEFAULT_WEAPON
current_volume = MUSIC_VOLUME
current_resolution = RES
current_music = DEFAULT_MUSIC
current_music_enabled = MUSIC_ENABLED


def apply_settings(settings: dict):
    """Apply settings to runtime globals"""
    global current_difficulty, current_child_face, current_parent_face
    global current_weapon, current_volume, current_resolution
    global current_music, current_music_enabled

    difficulty_name = settings.get("difficulty", DEFAULT_DIFFICULTY)
    current_difficulty = DIFFICULTIES.get(
        difficulty_name, DIFFICULTIES[DEFAULT_DIFFICULTY]
    )

    current_child_face = settings.get("child_face", DEFAULT_CHILD_FACE)
    current_parent_face = settings.get("parent_face", DEFAULT_PARENT_FACE)
    current_weapon = settings.get("weapon", DEFAULT_WEAPON)
    current_volume = settings.get("volume", MUSIC_VOLUME)
    current_music = settings.get("music", DEFAULT_MUSIC)
    current_music_enabled = settings.get("music_enabled", MUSIC_ENABLED)

    res_str = settings.get("resolution", "800x600")
    try:
        w, h = map(int, res_str.split("x"))
        current_resolution = (w, h)
    except:
        current_resolution = RES


def get_current_settings() -> dict:
    """Get current runtime settings as dict"""
    return {
        "player_name": Player_Name,
        "difficulty": list(DIFFICULTIES.keys())[
            list(DIFFICULTIES.values()).index(current_difficulty)
        ],
        "resolution": f"{current_resolution[0]}x{current_resolution[1]}",
        "volume": current_volume,
        "child_face": current_child_face,
        "parent_face": current_parent_face,
        "weapon": current_weapon,
    }


# ==================== ASSET DISCOVERY ====================
def scan_assets(directory: str, extension: str = ".png") -> list:
    """Scan directory for files with given extension"""
    if not os.path.exists(directory):
        return []
    files = []
    for f in os.listdir(directory):
        if f.endswith(extension):
            files.append(os.path.join(directory, f))
    return sorted(files)
