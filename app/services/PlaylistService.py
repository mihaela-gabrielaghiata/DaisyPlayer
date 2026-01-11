import os
import json
from datetime import datetime
from typing import List, Dict, Optional
from mutagen.mp3 import MP3
from app.controller import Controller


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
        self.fav_index = -1
        self.load_playlists()

    def load_playlists(self):
        self.playlists = []
        for filename in os.listdir(self.playlists_dir):
            if filename.endswith('.json'):
                path = os.path.join(self.playlists_dir, filename)
                self.playlists.append(Playlist(path))
                if self.playlists[-1].name == 'Favorite':
                    self.fav_index = len(self.playlists) - 1
    
    def get_playlists(self):
        return self.playlists
    
    def add_to_favorites(self, song_path: str):
        if self.fav_index == -1:
            data = {
                'name': 'Favorite',
                'song_count': 0,
                'total_duration': 0,
                'songs': []
            }
            fav_path = os.path.join(self.playlists_dir, 'favorite.json')
            with open(fav_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)
            self.playlists.append(Playlist(fav_path))
            self.fav_index = len(self.playlists) - 1
        self.playlists[self.fav_index].add_song(song_path)

    def is_favorite(self, song_name: str) -> bool:
        if self.fav_index == -1:
            return False
        fav_playlist = self.playlists[self.fav_index]
        for title, path in fav_playlist.songs:
            if title == song_name:
                return True
        return False
    
    def remove_from_favorites(self, song_name: str):
        if self.fav_index == -1:
            return
        self.playlists[self.fav_index].remove_song(song_name)

    def create_playlist(self, name: str):
        filename = f"{name.lower().replace(' ', '_')}.json"
        path = os.path.join(self.playlists_dir, filename)
        data = {
            'name': name,
            'song_count': 0,
            'total_duration': 0,
            'songs': []
        }
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
        self.playlists.append(Playlist(path))
    
    def delete_playlist(self, name: str):
        for playlist in self.playlists:
            if playlist.name == name:
                os.remove(playlist.path)
                self.playlists.remove(playlist)
                break

    def add_song_to_playlist(self, song_path: str, playlist_name: str):
        for playlist in self.playlists:
            if playlist.name == playlist_name:
                playlist.add_song(song_path)
                break
    
    def remove_song_from_playlist(self, song_path: str, playlist_name: str):
        for playlist in self.playlists:
            if playlist.name == playlist_name:
                playlist.remove_song(song_path)
                break

    def check_playlists(self):
        for playlist in self.playlists:
            playlist.check_songs()

class Playlist:
    def __init__(self, path: str):
        self.path = path
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        self.name = data.get('name', 'Unknown Playlist')
        self.song_count = data.get('song_count', 0)
        self.total_duration = data.get('total_duration', 0)
        self.songs = list(map(lambda song: (os.path.basename(song), song), data.get('songs', [])))
        self.need_check = False
        self.check_songs()

    def check_songs(self):
        controller = Controller.Controller.get_instance()
        all_songs = controller.get_songs()
        for title, path in self.songs:
            if not any(s[1] == path for s in all_songs):
                self.remove_song(path)

    def add_song(self, song_path: str):
        self.songs.append((os.path.basename(song_path), song_path))
        self.song_count += 1
        self.total_duration += self.get_song_duration(song_path)
        self.save()

    def remove_song(self, song_path: str):
        for title, path in self.songs:
            if path == song_path:
                self.total_duration -= self.get_song_duration(path)
                self.songs.remove((title, path))
                self.song_count -= 1
                self.save()
                break

    def get_song_duration(self, song_path: str):
        try:
            audio = MP3(song_path)
            return int(audio.info.length)
        except:
            self.need_check = True
            return 0

    def save(self):
        if self.need_check:
            self.need_check = False
            self.total_duration = 0
            for title, path in self.songs:
                try:
                    audio = MP3(path)
                    self.total_duration += int(audio.info.length)
                except:
                    continue
        data = {
            'name': self.name,
            'song_count': self.song_count,
            'total_duration': self.total_duration,
            'songs': [song[1] for song in self.songs]
        }
        with open(self.path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)

    
