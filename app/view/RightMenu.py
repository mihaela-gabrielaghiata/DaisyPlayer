import os
from PySide6.QtWidgets import (
    QVBoxLayout, QLabel, QPushButton, QFrame, QHBoxLayout,
    QListWidget, QWidget, QListWidgetItem, QCheckBox, QApplication, QSizePolicy, QDialog,
    QLineEdit
)
from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QIcon
from app.controller.Controller import Controller
from app.services.PlayerService import PlayerService

assets_path = 'app/assets'

class RightMenu(QWidget):
    def __init__(self):
        super().__init__()

        self.setAttribute(Qt.WA_StyledBackground, True)

        self.setObjectName('RightMenuWidget')
        self.controller = Controller.get_instance()
        self.controller.set_right_menu(self)
        self.layout = QVBoxLayout(self)
        self.set_home()
        self.theme = 'light'
        

    def set_home(self):
        self.clear_layout()

        self.playlist_widget = QListWidget()
        self.playlist_widget.setObjectName("PlaylistWidget")

        songs = self.controller.get_songs()
        self.controller.set_queued_songs(songs)

        self.download_widget = DownloadSongItem()
        self.download_widget.download_btn.clicked.connect(lambda: self.download_song(self.download_widget.input_link.text()))

        for title, path in songs:
            item = QListWidgetItem()
            widget = SongItem(title, path)

            item.setSizeHint(widget.sizeHint())
            self.playlist_widget.addItem(item)
            self.playlist_widget.setItemWidget(item, widget)

        self.label = QLabel("Toate melodiile")
        self.label.setObjectName("Title")

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.download_widget)
        self.layout.addWidget(self.playlist_widget)
    
    def download_song(self, url: str):
        self.controller.download_song_from_url(url)
        self.set_home()
    
    def clear_layout(self):
        self.delete_layout_recursively(self.layout)

    def delete_layout_recursively(self, layout):
        if layout is not None:
            while layout.count():
                child = layout.takeAt(0)
                if child.widget() is not None:
                    child.widget().deleteLater()
                elif child.layout() is not None:
                    self.delete_layout_recursively(child.layout())

    def set_playlists(self):
        self.clear_layout()

        self.playlist_widget = QListWidget()
        self.playlist_widget.setObjectName("PlaylistWidget")

        playlists = self.controller.get_playlists()

        for idx, playlist in enumerate(playlists):
            item = QListWidgetItem()
            widget = PlaylistItem(playlist)
            widget.handle_function = self.set_playlist_songs

            item.setSizeHint(widget.sizeHint())
            self.playlist_widget.addItem(item)
            self.playlist_widget.setItemWidget(item, widget)

        self.label = QLabel("Albume")
        self.label.setObjectName("Title")

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.playlist_widget)

    def set_playlist_songs(self, playlist):
        self.clear_layout()

        self.playlist_widget = QListWidget()
        self.playlist_widget.setObjectName("PlaylistWidget")

        print(playlist.songs)
        self.controller.set_queued_songs(playlist.songs)

        for song, path in playlist.songs:
            item = QListWidgetItem()
            widget = SongItem(song, path, playlist.name)

            item.setSizeHint(widget.sizeHint())
            self.playlist_widget.addItem(item)
            self.playlist_widget.setItemWidget(item, widget)

        self.label = QLabel(f"{playlist.name}")
        self.label.setObjectName("Title")

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.playlist_widget)

    def set_settings(self):
        self.clear_layout()
        
        title = QLabel("Settings")
        title.setObjectName("Title")
        
        
        row = QHBoxLayout()
        label = QLabel("Dark Mode")
        label.setObjectName("SettingsLabel")
        checkbox = QCheckBox()
        checkbox.setObjectName("SettingsCheckbox")
        if self.theme == 'dark':
            checkbox.setChecked(True)
        checkbox.stateChanged.connect(lambda state: self.set_app_theme(state == 2))

        row.addWidget(label)
        row.addWidget(checkbox)
        row.addStretch()

        self.layout.addWidget(title)
        self.layout.addLayout(row)
        self.layout.addStretch()

    def set_waveform(self):
        self.clear_layout()
        

    def set_app_theme(self, dark_mode: bool):
        app = QApplication.instance()
        if dark_mode:
            with open('app/view/stiluri/StyleDark.qss', 'r') as f:
                app.setStyleSheet(f.read())
                self.theme = 'dark'
        else:
            with open('app/view/stiluri/StyleLight.qss', 'r') as f:
                app.setStyleSheet(f.read())
                self.theme = 'light'


class DownloadSongItem(QWidget):
    def __init__(self):
        super().__init__()

        self.setObjectName("DownloadSongItem")
        self.setMaximumHeight(50)

        self.controller = Controller.get_instance()

        layout = QHBoxLayout(self)

        self.label = QLabel("Link: ")
        self.label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.input_link = QLineEdit()
        self.input_link.setPlaceholderText("Enter song URL")
        self.input_link.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.download_btn = QPushButton("Download")

        layout.addWidget(self.label)
        layout.addWidget(self.input_link)
        layout.addWidget(self.download_btn)

class SongItem(QWidget):
    def __init__(self, title, path, playlist_name=None):
        super().__init__()

        self.setObjectName("SongItem")

        self.controller = Controller.get_instance()

        self.title = title
        self.path = path

        layout = QHBoxLayout(self)

        self.label = QLabel(title)
        self.label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.favorite_btn = QPushButton()
        self.favorite_btn.setToolTip("Add/Remove from Favorites")
        self.favorite_btn.setIcon(QIcon(f"{assets_path}/icons/unfavorite.png"))
        self.favorite_btn.setIconSize(QSize(20,20))
        self.favorite_btn.setCheckable(True)
        self.favorite_btn.setChecked(self.controller.is_favorite(title))
        if self.favorite_btn.isChecked():
            self.favorite_btn.setIcon(QIcon(f"{assets_path}/icons/favorite.png"))
        self.favorite_btn.toggled.connect(lambda checked: self.favorite_btn.setIcon(
            QIcon(f"{assets_path}/icons/favorite.png") if checked else QIcon(f"{assets_path}/icons/unfavorite.png")
        ))
        self.favorite_btn.toggled.connect(lambda checked: self.controller.toggle_favorite(path, checked))

        self.add_to_playlist_btn = QPushButton()
        self.add_to_playlist_btn.setToolTip("Add to Playlist")
        self.add_to_playlist_btn.setIcon(QIcon(f"{assets_path}/icons/add-to-playlist.png"))
        self.add_to_playlist_btn.setIconSize(QSize(20,20))
        self.add_to_playlist_btn.clicked.connect(self.select_playlist)

        self.delete_btn = QPushButton()
        self.delete_btn.setToolTip("Delete Playlist")
        self.delete_btn.setIcon(QIcon(f"{assets_path}/icons/delete.png"))
        self.delete_btn.setIconSize(QSize(20,20))
        if playlist_name is None:
            self.delete_btn.clicked.connect(lambda :self.controller.delete_song(self.path))
        else:
            self.delete_btn.clicked.connect(lambda :self.controller.remove_song_from_playlist(self.path, playlist_name))

        layout.addWidget(self.label)
        layout.addWidget(self.favorite_btn)
        layout.addWidget(self.add_to_playlist_btn)
        layout.addWidget(self.delete_btn)

    def mousePressEvent(self, event):
        self.controller.play_song_by_name(self.title)

    def select_playlist(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Select playlist")
        dialog.setModal(True)
        dialog.resize(300, 200)

        layout = QVBoxLayout(dialog)

        playlists = self.controller.get_playlists()
        for playlist in playlists:
            btn = QPushButton(playlist.name)
            btn.clicked.connect(lambda checked, p=playlist: self.controller.add_song_to_playlist(self.path, p.name))
            btn.clicked.connect(dialog.accept)
            layout.addWidget(btn)

        layout.addWidget(QLabel("Create new playlist"))
        
        new_playlist_input = QLineEdit()
        new_playlist_input.setPlaceholderText("Playlist name")
        layout.addWidget(new_playlist_input)

        def on_create_clicked():
            self.controller.create_playlist(new_playlist_input.text())
            self.controller.add_song_to_playlist(self.path, new_playlist_input.text())
            dialog.accept()

        create_btn = QPushButton("Create")
        create_btn.clicked.connect(on_create_clicked)
        layout.addWidget(create_btn)

        dialog.setLayout(layout)

        dialog.exec()

class PlaylistItem(QWidget):
    def __init__(self, playlist):
        super().__init__()

        self.setObjectName("PlaylistItem")

        self.controller = Controller.get_instance()

        self.playlist = playlist
        self.name = playlist.name
        self.song_count = playlist.song_count
        self.total_duration = playlist.total_duration
        self.handle_function = None

        layout = QHBoxLayout(self)

        self.label = QLabel(f"{self.name} ({self.song_count} songs):      {self.total_duration//60}:{self.total_duration%60:02}")
        self.label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        self.delete_btn = QPushButton()
        self.delete_btn.setToolTip("Delete Playlist")
        self.delete_btn.setIcon(QIcon(f"{assets_path}/icons/delete.png"))
        self.delete_btn.setIconSize(QSize(20,20))
        self.delete_btn.clicked.connect(self.delete_playlist)

        layout.addWidget(self.label)
        layout.addWidget(self.delete_btn)

    def delete_playlist(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Select playlist")
        dialog.setModal(True)
        dialog.resize(300, 100)

        layout = QVBoxLayout(dialog)

        label = QLabel(f"Are you sure you want to delete playlist '{self.name}'?")

        layout_btns = QHBoxLayout()
        accept_btn = QPushButton("Delete")
        accept_btn.clicked.connect(lambda :self.controller.delete_playlist(self.name))
        accept_btn.clicked.connect(dialog.accept)

        decline_btn = QPushButton("Cancel")
        decline_btn.clicked.connect(dialog.reject)

        layout_btns.addWidget(decline_btn)
        layout_btns.addWidget(accept_btn)

        layout.addWidget(label)
        layout.addLayout(layout_btns)

        dialog.setLayout(layout)

        dialog.exec()

    def mousePressEvent(self, event):
        if self.handle_function:
            self.handle_function(self.playlist)