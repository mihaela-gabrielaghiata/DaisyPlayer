import os
from PySide6.QtWidgets import (
    QVBoxLayout, QLabel, QPushButton, QFrame, QHBoxLayout,
    QListWidget, QWidget, QListWidgetItem
)

assets_path = 'app/assets'

class RightMenu(QVBoxLayout):
    def __init__(self):
        super().__init__()
        self.music_path = 'local_music/'
        self.set_home()

    def load_songs(self):
        allowed = (".mp3",)
        songs = []

        for file in os.listdir(self.music_path):
            if file.lower().endswith(allowed):
                full_path = os.path.join(self.music_path, file)
                songs.append((file, full_path))

        return songs

    def set_home(self):
        self.playlist_widget = QListWidget()
        songs = self.load_songs()

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
