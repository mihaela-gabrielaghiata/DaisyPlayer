from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtCore import QUrl
import os

class PlayerService:
    _instance = None

    @staticmethod
    def get_instance():
        if PlayerService._instance is None:
            PlayerService()
        return PlayerService._instance

    def __init__(self):
        if PlayerService._instance is not None:
            raise Exception("Singleton – folosește get_instance()!")
        PlayerService._instance = self

        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.player.setAudioOutput(self.audio_output)

        self.music_path = 'local_music/'
        self.current_song = -1
        self.songs = []
        self.load_songs()

    def load_songs(self):
        allowed = (".mp3",)
        self.songs = []
        if not os.path.exists(self.music_path):
            os.makedirs(self.music_path)

        for file in os.listdir(self.music_path):
            if file.lower().endswith(allowed):
                full_path = os.path.join(self.music_path, file)
                self.songs.append((file, full_path))
        
        if len(self.songs) > 0:
            self.current_song = 0

    def get_songs(self):
        return self.songs

    def play_song(self, name = None):
        if name is None:
            if self.current_song == -1 and len(self.songs) > 0:
                self.current_song = 0
            if self.current_song != -1:
                song_path = self.songs[self.current_song][1]
                self.player.setSource(QUrl.fromLocalFile(song_path))
                self.player.play()
        else:
            for idx, song in enumerate(self.songs):
                if song[0] == name:
                    self.current_song = idx
                    self.player.setSource(QUrl.fromLocalFile(song[1]))
                    self.player.play()

    def pause(self):
        try:
            self.player.pause()
        except Exception:
            pass

    def is_playing(self):
        try:
            return self.player.playbackState() == QMediaPlayer.PlayingState
        except Exception:
            return False

    def toggle_play(self):
        if self.is_playing():
            self.pause()
        else:
            self.play_song()

    def next_song(self):
        if len(self.songs) == 0:
            return
        if self.current_song == -1:
            self.current_song = 0
        else:
            self.current_song = (self.current_song + 1) % len(self.songs)
        self.play_song()

    def prev_song(self):
        if len(self.songs) == 0:
            return
        if self.current_song == -1:
            self.current_song = 0
        else:
            self.current_song = (self.current_song - 1) % len(self.songs)
        self.play_song()

    def seek_by_percent(self, percent: float):
        dur = self.player.duration()
        ms = int(dur * (max(0.0, min(100.0, percent)) / 100.0))
        self.player.setPosition(ms)
