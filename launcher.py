import sys
import os
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QRadioButton,
    QButtonGroup,
    QSlider,
    QComboBox,
    QPushButton,
    QListWidget,
    QGroupBox,
    QFormLayout,
    QMessageBox,
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPixmap, QIcon

# Import config
sys.path.insert(0, os.path.dirname(__file__))
import config


class GameLauncher(QWidget):
    def __init__(self):
        super().__init__()
        self.settings = {}
        self.init_ui()
        self.load_saved_settings()

    def init_ui(self):
        self.setWindowTitle("Jutti Di Putti - Game Launcher")
        self.setMinimumSize(600, 700)

        main_layout = QVBoxLayout()

        # Title
        title = QLabel("🏃 JUTTI DI PUTTI 🏃")
        title.setStyleSheet(
            "font-size: 32px; font-weight: bold; color: #2c3e50; padding: 20px;"
        )
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)

        # Player Name
        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("Player Name:"))
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter your name")
        self.name_input.setText("Player")
        name_layout.addWidget(self.name_input)
        main_layout.addLayout(name_layout)

        # Difficulty
        diff_group = QGroupBox("Difficulty")
        diff_layout = QHBoxLayout()
        self.diff_group = QButtonGroup(self)

        difficulties = list(config.DIFFICULTIES.keys())
        for diff in difficulties:
            rb = QRadioButton(diff)
            rb.setObjectName(diff)
            self.diff_group.addButton(rb)
            diff_layout.addWidget(rb)

        diff_group.setLayout(diff_layout)
        main_layout.addWidget(diff_group)

        # Resolution
        res_layout = QHBoxLayout()
        res_layout.addWidget(QLabel("Resolution:"))
        self.res_combo = QComboBox()
        self.res_combo.addItems(config.RESOLUTIONS)
        res_layout.addWidget(self.res_combo)
        res_layout.addStretch()
        main_layout.addLayout(res_layout)

        # Volume
        vol_layout = QHBoxLayout()
        vol_layout.addWidget(QLabel("Volume:"))
        self.vol_slider = QSlider(Qt.Orientation.Horizontal)
        self.vol_slider.setMinimum(0)
        self.vol_slider.setMaximum(100)
        self.vol_slider.setValue(50)
        self.vol_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.vol_slider.setTickInterval(10)
        self.vol_label = QLabel("50%")
        self.vol_slider.valueChanged.connect(lambda v: self.vol_label.setText(f"{v}%"))
        vol_layout.addWidget(self.vol_slider)
        vol_layout.addWidget(self.vol_label)
        main_layout.addLayout(vol_layout)

        # Asset Selection
        asset_group = QGroupBox("Character & Weapon Selection")
        asset_layout = QFormLayout()

        # Child Face
        child_layout = QHBoxLayout()
        self.child_combo = QComboBox()
        self.populate_asset_combo(self.child_combo, config.CHILD_FACES_DIR)
        self.child_preview = QLabel()
        self.child_preview.setMinimumSize(80, 80)
        self.child_preview.setMaximumSize(80, 80)
        self.child_preview.setStyleSheet("border: 2px solid #ccc; background: #f0f0f0;")
        self.child_combo.currentTextChanged.connect(self.update_child_preview)
        child_layout.addWidget(self.child_combo)
        child_layout.addWidget(self.child_preview)
        asset_layout.addRow("Child Face:", child_layout)

        # Parent Face
        parent_layout = QHBoxLayout()
        self.parent_combo = QComboBox()
        self.populate_asset_combo(self.parent_combo, config.PARENT_FACES_DIR)
        self.parent_preview = QLabel()
        self.parent_preview.setMinimumSize(80, 80)
        self.parent_preview.setMaximumSize(80, 80)
        self.parent_preview.setStyleSheet(
            "border: 2px solid #ccc; background: #f0f0f0;"
        )
        self.parent_combo.currentTextChanged.connect(self.update_parent_preview)
        parent_layout.addWidget(self.parent_combo)
        parent_layout.addWidget(self.parent_preview)
        asset_layout.addRow("Parent Face:", parent_layout)

        # Weapon
        weapon_layout = QHBoxLayout()
        self.weapon_combo = QComboBox()
        self.populate_asset_combo(
            self.weapon_combo, config.WEAPONS_DIR, extensions=[".png"]
        )
        self.weapon_preview = QLabel()
        self.weapon_preview.setMinimumSize(80, 80)
        self.weapon_preview.setMaximumSize(80, 80)
        self.weapon_preview.setStyleSheet(
            "border: 2px solid #ccc; background: #f0f0f0;"
        )
        self.weapon_combo.currentTextChanged.connect(self.update_weapon_preview)
        weapon_layout.addWidget(self.weapon_combo)
        weapon_layout.addWidget(self.weapon_preview)
        asset_layout.addRow("Weapon:", weapon_layout)

        asset_group.setLayout(asset_layout)
        main_layout.addWidget(asset_group)

        # Start Button
        self.start_btn = QPushButton("🎮 START GAME")
        self.start_btn.setStyleSheet("""
            QPushButton {
                font-size: 24px;
                font-weight: bold;
                padding: 15px;
                background-color: #27ae60;
                color: white;
                border: none;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #2ecc71;
            }
        """)
        self.start_btn.clicked.connect(self.start_game)
        main_layout.addWidget(self.start_btn)

        # High Scores
        hs_group = QGroupBox("🏆 High Scores")
        hs_layout = QVBoxLayout()
        self.hs_list = QListWidget()
        self.load_high_scores()
        hs_layout.addWidget(self.hs_list)
        hs_group.setLayout(hs_layout)
        main_layout.addWidget(hs_group)

        self.setLayout(main_layout)

        # Set default preview
        self.update_child_preview(self.child_combo.currentText())
        self.update_parent_preview(self.parent_combo.currentText())
        self.update_weapon_preview(self.weapon_combo.currentText())

    def populate_asset_combo(self, combo, directory, extensions=[".png"]):
        """Populate combo box with available assets"""
        combo.clear()
        if not os.path.exists(directory):
            return

        for f in os.listdir(directory):
            for ext in extensions:
                if f.endswith(ext):
                    full_path = os.path.join(directory, f)
                    combo.addItem(full_path)
                    break

    def update_child_preview(self, path):
        self._update_preview(self.child_preview, path)

    def update_parent_preview(self, path):
        self._update_preview(self.parent_preview, path)

    def update_weapon_preview(self, path):
        self._update_preview(self.weapon_preview, path)

    def _update_preview(self, label, path):
        if not path or not os.path.exists(path):
            label.setText("N/A")
            label.setPixmap(QPixmap())
            return

        pixmap = QPixmap(path)
        if pixmap.isNull():
            label.setText("Error")
            return

        # Scale to fit while maintaining aspect ratio
        label.setPixmap(
            pixmap.scaled(
                label.size(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
        )

    def load_saved_settings(self):
        """Load and apply saved settings"""
        settings = config.load_settings()

        self.name_input.setText(settings.get("player_name", "Player"))

        # Set difficulty
        diff = settings.get("difficulty", "Medium")
        for btn in self.diff_group.buttons():
            if btn.objectName() == diff:
                btn.setChecked(True)
                break

        # Set resolution
        res = settings.get("resolution", "800x600")
        self.res_combo.setCurrentText(res)

        # Set volume
        vol = int(settings.get("volume", 0.5) * 100)
        self.vol_slider.setValue(vol)

        # Set assets
        child = settings.get("child_face", config.DEFAULT_CHILD_FACE)
        parent = settings.get("parent_face", config.DEFAULT_PARENT_FACE)
        weapon = settings.get("weapon", config.DEFAULT_WEAPON)

        self.child_combo.setCurrentText(child)
        self.parent_combo.setCurrentText(parent)
        self.weapon_combo.setCurrentText(weapon)

    def load_high_scores(self):
        """Load and display high scores"""
        self.hs_list.clear()

        filepath = os.path.join(os.path.dirname(__file__), "highscore.json")
        if not os.path.exists(filepath):
            self.hs_list.addItem("No high scores yet!")
            return

        try:
            import json

            with open(filepath, "r") as f:
                scores = json.load(f)

            if not scores:
                self.hs_list.addItem("No high scores yet!")
                return

            # Sort by score (descending)
            sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)

            for i, (name, score) in enumerate(sorted_scores[:10], 1):
                self.hs_list.addItem(f"{i}. {name} - {score}s")
        except:
            self.hs_list.addItem("Error loading scores")

    def get_settings(self) -> dict:
        """Collect all settings from UI"""

        # Find selected difficulty
        selected_diff = "Medium"
        for btn in self.diff_group.buttons():
            if btn.isChecked():
                selected_diff = btn.objectName()
                break

        return {
            "action": "start",
            "player_name": self.name_input.text() or "Player",
            "difficulty": selected_diff,
            "resolution": self.res_combo.currentText(),
            "volume": self.vol_slider.value() / 100.0,
            "child_face": self.child_combo.currentText(),
            "parent_face": self.parent_combo.currentText(),
            "weapon": self.weapon_combo.currentText(),
        }

    def start_game(self):
        """Save settings and close with success"""
        self.settings = self.get_settings()

        # Save settings
        config.save_settings(self.settings)

        self.close()

    def closeEvent(self, event):
        """Handle window close - check if we have settings"""
        if not self.settings:
            self.settings = {"action": "quit"}
        event.accept()


def show_launcher():
    """Show the launcher and return settings dict"""
    app = QApplication(sys.argv)

    # Set app style
    app.setStyle("Fusion")

    launcher = GameLauncher()
    launcher.show()
    app.exec()

    return launcher.settings


if __name__ == "__main__":
    settings = show_launcher()
    print("Settings:", settings)
