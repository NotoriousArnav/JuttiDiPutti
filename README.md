# Jutti Di Putti 🏃

A pygame-based survival game where you play as a child trying to avoid getting caught by a parent wielding a weapon.

## How to Play

1. **Launch the game**: `uv run main.py`
2. **Configure your game** in the launcher:
   - Enter your player name
   - Select difficulty (Easy, Medium, Hard, Impossible)
   - Choose resolution
   - Adjust music volume
   - Select character faces and weapon
   - Upload custom images for faces and weapons
3. **Survive!** Move your mouse to control the child character
4. **Press Q** to quit during gameplay
5. **Press R** after getting caught to restart

## Game Mechanics

- **Difficulty Levels**:
  - **Easy**: Slow speeds, large offset between parent and weapon
  - **Medium**: Moderate speeds, starts at 1.5x multiplier
  - **Hard**: Fast speeds, starts at 3.0x multiplier
  - **Impossible**: Extremely fast, starts at 10x multiplier

- **Speed Multiplier**: Increases by 0.1x every 30 seconds of survival
- **High Scores**: Best times are saved per player name
- **Custom Assets**: Upload your own character faces and weapons (supports PNG, JPG, BMP, GIF)

## Project Structure

```
OhNoooooo/
├── main.py          # Main entry point
├── config.py        # Game configuration and settings
├── assets.py        # Asset loading utilities
├── entities.py      # Movement and collision logic
├── game_state.py    # UI, high scores, game over handling
├── launcher.py      # PyQt6-based game launcher
├── faces/           # Character face images
├── assets/          # Weapon images and music
└── settings.json    # Saved user preferences
```

## Requirements

- Python 3.12+
- pygame>=2.6.1
- PyQt6>=6.11.0
- Pillow>=10.0.0

## Installation

```bash
pip install uv
uv sync
```

## Running

```bash
uv run main.py
```

## License

MIT License