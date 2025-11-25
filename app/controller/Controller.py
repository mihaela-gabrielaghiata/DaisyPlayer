from app.services.PlayerService import PlayerService
from PySide6.QtWidgets import QSlider, QPushButton
from PySide6.QtGui import QIcon

class Controller:
    _instance = None

    @staticmethod
    def get_instance():
        if Controller._instance is None:
            Controller()
        return Controller._instance

    def __init__(self):
        if Controller._instance is not None:
            raise Exception("Singleton – use get_instance()")
        Controller._instance = self

        self.player_service = PlayerService.get_instance()
        self.play_ico = QIcon('app/assets/icons/play.png')
        self.pause_ico = QIcon('app/assets/icons/pause.png')
        self.state = 'play'

    def toggle_play(self, btn: QPushButton):
        self.player_service.toggle_play()
        if self.state == 'play':
            self.state = 'pause'
            btn.setIcon(self.pause_ico)
        else:
            self.state = 'play'
            btn.setIcon(self.play_ico)

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
    
    def set_song_position(self, position):     
        if self.slider and self.slider.isSliderDown() == False:
            self.slider.blockSignals(True)
            self.slider.setValue(int(position * self.slider.maximum()))
            self.slider.blockSignals(False) 
