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

        self.setObjectName('RightMenu')
        self.controller = Controller.get_instance()
        self.set_home()

    def set_home(self):
        self.clear_layout()

        self.playlist_widget = QListWidget()
        self.playlist_widget.setObjectName("PlaylistWidget")

        songs = self.controller.get_songs()

        for title, path in songs:
            item = QListWidgetItem()
            widget = SongItem(title, path)

            item.setSizeHint(widget.sizeHint())
            self.playlist_widget.addItem(item)
            self.playlist_widget.setItemWidget(item, widget)

        self.addWidget(self.playlist_widget)
    
    def clear_layout(self):
        while self.count():
            child = self.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
    
    def set_playlists(self):
        self.clear_layout()

        self.playlist_widget = QListWidget()
        self.playlist_widget.setObjectName("PlaylistWidget")

        playlists = self.controller.get_playlists()

        for playlist in playlists:
            item = QListWidgetItem()
            widget = PlaylistItem(playlist.name, playlist.song_count, playlist.total_duration)

            item.setSizeHint(widget.sizeHint())
            self.playlist_widget.addItem(item)
            self.playlist_widget.setItemWidget(item, widget)

        self.addWidget(self.playlist_widget)


class SongItem(QWidget):
    def __init__(self, title, path):
        super().__init__()

        self.setObjectName("SongItem")

        self.title = title
        self.path = path

        layout = QHBoxLayout(self)

        self.label = QLabel(title)
        layout.addWidget(self.label)

        self.controller = Controller.get_instance()

    def mousePressEvent(self, event):
        self.controller.play_song_by_name(self.title)

class PlaylistItem(QWidget):
    def __init__(self, name, song_count, total_duration):
        super().__init__()

        self.setObjectName("PlaylistItem")

        self.name = name
        self.song_count = song_count
        self.total_duration = total_duration

        layout = QHBoxLayout(self)

        self.label = QLabel(f"{name} ({song_count} songs):      {total_duration} min")
        layout.addWidget(self.label)
    

