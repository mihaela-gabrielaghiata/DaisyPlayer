from app.services.PlayerService import PlayerService
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
        self.play_ico = QIcon('app/assets/icons/play.png')
        self.pause_ico = QIcon('app/assets/icons/pause.png')
        self.state = 'play'

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
