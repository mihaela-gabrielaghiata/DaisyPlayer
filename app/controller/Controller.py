from app.services.PlayerService import PlayerService

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

    def toggle_play(self):
        self.player_service.toggle_play()

    def pause(self):
        self.player_service.pause()

    def next_song(self):
        self.player_service.next_song()

    def prev_song(self):
        self.player_service.prev_song()

    def play_song_by_name(self, name):
        self.player_service.play_song(name)

    def get_song_list(self):
        return self.player_service.get_songs()
    
    def seek_by_percent(self, percent: float):
        player = getattr(self.player_service, 'player', None)
        if player is None:
            return
        dur = player.duration()
        if not dur or dur <= 0:
            return  # media not ready; ignore
        percent = max(0.0, min(100.0, float(percent)))
        target_ms = int(dur * (percent / 100.0))
        player.setPosition(target_ms)
