import os
from PySide6.QtWidgets import (
    QVBoxLayout, QLabel, QPushButton, QFrame, QHBoxLayout,
    QListWidget, QWidget, QListWidgetItem
)
from app.controller.Controller import Controller
from app.services.PlayerService import PlayerService

assets_path = 'app/assets'

class RightMenu(QVBoxLayout):
    def __init__(self):
        super().__init__()
        self.media_player = PlayerService.get_instance()
        self.set_home()

    def set_home(self):
        self.playlist_widget = QListWidget()
        songs = self.media_player.get_songs()

        for title, path in songs:
            item = QListWidgetItem()
            widget = SongItem(title, path)

            item.setSizeHint(widget.sizeHint())
            self.playlist_widget.addItem(item)
            self.playlist_widget.setItemWidget(item, widget)

        self.addWidget(self.playlist_widget)


class SongItem(QWidget):
    def __init__(self, title, path):
        super().__init__()

        self.title = title
        self.path = path

        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 5, 10, 5)

        self.label = QLabel(title)
        layout.addWidget(self.label)

        self.controller = Controller.get_instance()

    def mousePressEvent(self, event):
        self.controller.play_song_by_name(self.title)
    

