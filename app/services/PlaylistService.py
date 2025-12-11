import os
import json
from datetime import datetime
from typing import List, Dict, Optional


class PlaylistService:
    
    __instance = None
    
    @staticmethod
    def get_instance():
        if PlaylistService.__instance is None:
            PlaylistService()
        return PlaylistService.__instance
    
    def __init__(self):
        if PlaylistService.__instance is not None:
            raise Exception("Singleton - use get_instance()")
        PlaylistService.__instance = self
        
        self.playlists_dir = 'data/playlists/'
        self.playlists = []
        self.load_playlists()

    def load_playlists(self):
        self.playlists = []
        for filename in os.listdir(self.playlists_dir):
            if filename.endswith('.json'):
                path = os.path.join(self.playlists_dir, filename)
                self.playlists.append(Playlist(path))
    
    def get_playlists(self):
        return self.playlists
        
    
class Playlist:
    def __init__(self, path: str):
        self.path = path
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        self.name = data.get('name', 'Unknown Playlist')
        self.song_count = data.get('song_count', 0)
        self.total_duration = data.get('total_duration', 0)
        self.songs = data.get('songs', [])
