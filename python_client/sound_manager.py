from pathlib import Path
from typing import Dict

import pygame.mixer

from python_client.client_storage import ClientStorage


class SoundManager:
    music_resources_path = Path('resources/snd/musics')
    music_resources: Dict[str, Path] = {
        'battle': music_resources_path / 'battle.mp3',
        'battle_lean_to_win': music_resources_path / 'battle_lean_to_win.mp3',
        'battle_lean_to_lose': music_resources_path / 'battle_lean_to_lose.mp3',
    }

    def __init__(self, client_storage: ClientStorage, default_music_name: str):
        self.client_storage = client_storage
        self.music_queue = list()
        self.music_queue.append(default_music_name)
        self.music_end_event_code = pygame.USEREVENT + 1
        pygame.mixer.init()
        pygame.mixer.music.load(self.get_music_file_path_by_name(default_music_name))
        pygame.mixer.music.play(loops=-1)
        pygame.mixer.music.set_endevent(self.music_end_event_code)

    def get_music_file_path_by_name(self, music_name: str) -> Path:
        return self.music_resources[music_name]

    def tick(self):
        if len(self.music_queue) > 1:
            self.music_queue.pop(0)
            pygame.mixer.music.fadeout(1500)

    def music_end_callback(self):
        pygame.mixer.music.load(self.get_music_file_path_by_name(self.current_music_name))
        pygame.mixer.music.play(loops=-1)

    @property
    def current_music_name(self) -> str:
        return self.music_queue[0]
