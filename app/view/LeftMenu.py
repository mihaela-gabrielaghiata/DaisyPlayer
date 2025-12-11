from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QVBoxLayout, QPushButton

assets_path = 'app/assets'

class LeftMenu(QVBoxLayout):
    def __init__(self, right_menu):
        super().__init__()

        self.right_menu = right_menu

        button_home= QPushButton('Acasa')
        button_home.setIcon(QIcon(f"{assets_path}/icons/home.png"))
        button_home.setIconSize(QSize(30,30))

        button_settings=QPushButton('Setari')
        button_settings.setIcon(QIcon(f"{assets_path}/icons/setting.png"))
        button_settings.setIconSize(QSize(30,30))

        button_playlist=QPushButton('Albume')
        button_playlist.setIcon(QIcon(f"{assets_path}/icons/playlist.png"))
        button_playlist.setIconSize(QSize(30,30))

        button_home.clicked.connect(self.right_menu.set_home)
        button_playlist.clicked.connect(self.right_menu.set_playlists)

        self.addWidget(button_home)
        self.addWidget(button_settings)
        self.addWidget(button_playlist)
        self.addStretch()





