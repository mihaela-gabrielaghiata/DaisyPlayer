from app.services.PlayerService import PlayerService
from app.services.PlaylistService import PlaylistService
from PySide6.QtWidgets import QSlider, QPushButton, QLabel
from PySide6.QtGui import QIcon
from PySide6.QtMultimedia import QMediaMetaData

class Controller:
    _instance = None

    @staticmethod
    def get_instance():
        if Controller._instance is None:
            Controller()
        return Controller._instance

    def __init__(self):
        if Controller._instance is not None:
            raise Exception("Singleton - use get_instance()")
        Controller._instance = self

        self.player_service = PlayerService.get_instance()
        self.playlist_service = PlaylistService.get_instance()
        self.play_ico = QIcon('app/assets/icons/play.png')
        self.pause_ico = QIcon('app/assets/icons/pause.png')
        self.state = 'play'

    def get_songs(self):
        return self.player_service.get_songs()
    
    def set_queued_songs(self, s: list):
        self.player_service.set_queued_songs(s)

    def toggle_play(self):
        self.player_service.toggle_play()

    def pause(self):
        self.player_service.pause()

    def next_song(self):
        self.player_service.next_song()

    def prev_song(self):
        self.player_service.prev_song()

    def play_song_by_name(self, name):
        self.player_service.play(name)

    def get_song_list(self):
        return self.player_service.get_songs()
    
    def seek_by_percent(self, percent: float):
        self.player_service.seek_by_percent(percent)

    def set_song_slider(self, slider: QSlider):
        self.slider = slider

    def set_play_button(self, btn: QPushButton):
        self.play_button = btn
    
    def update_play_button(self, state: str):
        self.state = state
        if self.state == 'play':
            self.play_button.setIcon(self.pause_ico)
        elif self.state == 'pause':
            self.play_button.setIcon(self.play_ico)
    
    def set_song_position(self, position):     
        if self.slider and self.slider.isSliderDown() == False:
            self.slider.blockSignals(True)
            self.slider.setValue(int(position * self.slider.maximum()))
            self.slider.blockSignals(False) 

    def set_volume(self, volume: int):
        self.player_service.set_volume(volume)

    def toggle_volume(self, check: bool):
        self.player_service.toggle_volume(check)

    def set_repeat(self, repeat: bool):
        self.player_service.set_repeat(repeat)

    def toggle_shuffle(self, shuffle: bool):
        if shuffle:
            self.player_service.shuffle_songs()
        else:
            self.player_service.unshuffle_songs()

    def set_music_label(self, label: QLabel):
        self.music_label = label

    def update_current_song_display(self):
        data:QMediaMetaData = self.player_service.get_current_song_metadata()
        text = ""
        title = QMediaMetaData.Key.Title
        artist = QMediaMetaData.Key.ContributingArtist

        if data.value(title):
            text += f"<div>{data.stringValue(title)}</div>"
            if data.value(artist):
                color = self.music_label.palette().color(self.music_label.foregroundRole())
                text += f"\n<div style=\'color: rgba({color.red()}, {color.green()}, {color.blue()}, 150);\'>Artist: {data.stringValue(artist)}</div>"
        else:
            text += self.player_service.get_current_song_file_name()

        if self.music_label:
            self.music_label.setText(text)
        else:
            print("\n")
            print(text)
            print("\n")

    def get_playlists(self):
        return self.playlist_service.get_playlists()
    
    def is_favorite(self, song_name: str) -> bool:
        return self.playlist_service.is_favorite(song_name)
    
    def toggle_favorite(self, song_path: str, add: bool):
        print(add)
        if add:
            self.playlist_service.add_to_favorites(song_path)
        else:
            self.playlist_service.remove_from_favorites(song_path)
    
    def add_song_to_playlist(self, song_path: str, playlist_name: str):
        self.playlist_service.add_song_to_playlist(song_path, playlist_name)

    def create_playlist(self, name: str):
        self.playlist_service.create_playlist(name)

    def delete_playlist(self, name: str):
        self.playlist_service.delete_playlist(name)
        
    def set_right_menu(self, right_menu):
        self.right_menu = right_menu

    def show_waveform(self):
        self.right_menu.set_waveform()

    def download_song_from_url(self, url: str):
        self.player_service.download_song_from_url(url)

    def delete_song(self, song_path: str):
        print("Deleting song:", song_path)
        self.player_service.delete_song(song_path)
        self.right_menu.set_home()
        self.playlist_service.check_playlists()

    def remove_song_from_playlist(self, song_path: str, playlist_name: str):
        print("Removing song from playlist:", song_path, "from", playlist_name)
        self.playlist_service.remove_song_from_playlist(song_path, playlist_name)