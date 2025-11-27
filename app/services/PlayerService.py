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
            raise Exception("Singleton - use get_instance()")
        PlayerService._instance = self

        from app.controller.Controller import Controller
        self.controller = Controller.get_instance()

        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.audio_output.setVolume(0.5)
        self.player.setAudioOutput(self.audio_output)

        self.player.positionChanged.connect(lambda v: self.controller.set_song_position(v / self.player.duration() if self.player.duration() > 0 else 0))
        self.player.metaDataChanged.connect(self.controller.update_current_song_display)
        self.player.mediaStatusChanged.connect(lambda status: self.controller.next_song() if status == QMediaPlayer.MediaStatus.EndOfMedia and self.player.loops() != QMediaPlayer.Infinite else None)
        
        self.music_path = 'local_music/'
        self.current_song = -1
        self.songs = []
        self.load_songs()
        self.queued_songs = self.songs.copy()

    def load_songs(self):
        allowed = (".mp3",)
        self.songs = []
        if not os.path.exists(self.music_path):
            os.makedirs(self.music_path)

        for file in os.listdir(self.music_path):
            if file.lower().endswith(allowed):
                full_path = os.path.join(self.music_path, file)
                self.songs.append((file, full_path))

    def get_songs(self):
        return self.songs
    
    def get_current_song_metadata(self):
        if self.player.source().isEmpty() == False and self.current_song != -1:
            return self.player.metaData()
    
    def get_current_song_file_name(self):
        if self.player.source().isEmpty() == False and self.current_song != -1:
            return self.queued_songs[self.current_song][0]

    def play(self, name = None):
        if name is None:
            if self.player.source().isEmpty() == False:
                self.player.play()
            else:
                if self.current_song == -1 and len(self.queued_songs) > 0:
                    self.current_song = 0
                song_path = self.queued_songs[self.current_song][1]
                self.player.setSource(QUrl.fromLocalFile(song_path))
                self.player.play()
        else:
            for idx, song in enumerate(self.queued_songs):
                if song[0] == name:
                    self.current_song = idx
                    self.player.setSource(QUrl.fromLocalFile(song[1]))
                    self.player.play()
        self.controller.update_play_button('play')

    def pause(self):
        self.player.pause()
        self.controller.update_play_button('pause')


    def is_playing(self):
        return self.player.playbackState() == QMediaPlayer.PlayingState

    def toggle_play(self):
        if self.is_playing():
            self.pause()
        else:
            self.play()

    def next_song(self):
        if len(self.queued_songs) == 0:
            return
        if self.current_song == -1:
            self.current_song = 0
        else:
            self.current_song = (self.current_song + 1) % len(self.queued_songs)
        if self.current_song >= 0 and self.current_song < len(self.queued_songs):
            song_path = self.queued_songs[self.current_song][1]
            self.player.setSource(QUrl.fromLocalFile(os.path.abspath(song_path)))
            self.play()

    def prev_song(self):
        if len(self.queued_songs) == 0:
            return
        if self.current_song == -1:
            self.current_song = 0
        else:
            self.current_song = (self.current_song - 1) % len(self.queued_songs)
        if self.current_song >= 0 and self.current_song < len(self.queued_songs):
            song_path = self.queued_songs[self.current_song][1]
            self.player.setSource(QUrl.fromLocalFile(os.path.abspath(song_path)))
            self.play()

    def seek_by_percent(self, percent: float):
        if self.player.isSeekable():
            self.player.blockSignals(True)
            self.player.setPosition(int(percent * self.player.duration()))
            self.player.blockSignals(False)

    def set_volume(self, volume: int):
        self.audio_output.setVolume(volume / 100.0)

    def toggle_volume(self, check: bool):
        self.audio_output.setMuted(check)

    def set_repeat(self, repeat: bool):
        self.player.setLoops(QMediaPlayer.Infinite if repeat else QMediaPlayer.Loops(1))

    def shuffle_songs(self):
        import random
        temp = self.queued_songs[self.current_song] if self.current_song != -1 else None
        if temp:
            self.queued_songs.remove(temp)
            random.shuffle(self.queued_songs)
            self.queued_songs.insert(0, temp)
        else:
            random.shuffle(self.queued_songs)
        self.current_song = 0

    def unshuffle_songs(self):
        temp = self.queued_songs[self.current_song] if self.current_song != -1 else None
        self.queued_songs = self.songs.copy()
        if temp:
            self.current_song = self.queued_songs.index(temp)
        else:
            self.current_song = 0
