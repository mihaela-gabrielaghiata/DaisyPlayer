from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QVBoxLayout, QPushButton

assets_path = 'app/assets'

class LeftMenu(QVBoxLayout):
    def __init__(self):
        super().__init__()

        button_home= QPushButton('Acasa')
        button_home.setIcon(QIcon(f"{assets_path}/icons/home.png"))
        button_home.setIconSize(QSize(24,24))

        button_settings=QPushButton('Setari')
        button_settings.setIcon(QIcon(f"{assets_path}/icons/settings.png"))
        button_settings.setIconSize(QSize(24,24))

        button_playlist=QPushButton('Albume')
        button_playlist.setIcon(QIcon(f"{assets_path}/icons/playlist1.png"))
        button_playlist.setIconSize(QSize(24,24))

        self.addWidget(button_home)
        self.addWidget(button_settings)
        self.addWidget(button_playlist)
        self.addStretch()





