import os

import pygame

os.add_dll_directory(r'C:\Users\apple\OneDrive\문서\GitHub\Jang-Gi-the-board-game\c_incubator\bin')

from python_client.client_storage import ClientStorage
from python_client.graphics_manager import GraphicsManager
from python_client.input_manager import InputManager
from python_client.sound_manager import SoundManager


class PythonClient:
    def __init__(self):
        self.is_game_running: bool = True

        # os.environ['SDL_VIDEO_WINDOW_POS'] = '450,100'
        pygame.init()
        self.client_storage = ClientStorage()
        self.client_storage.set_component(
            GraphicsManager(client_storage=self.client_storage)
        )
        self.client_storage.set_component(
            InputManager(client_storage=self.client_storage)
        )
        self.client_storage.set_component(
            SoundManager(client_storage=self.client_storage, default_music_name='battle')
        )

    def run(self):
        grp_mng: GraphicsManager = self.client_storage.get_component(GraphicsManager)
        ipt_mng: InputManager = self.client_storage.get_component(InputManager)
        snd_mng: SoundManager = self.client_storage.get_component(SoundManager)
        while self.is_game_running:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    self.is_game_running = False
                elif e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                    self.is_game_running = False
                elif e.type == snd_mng.music_end_event_code:
                    snd_mng.music_end_callback()
                else:
                    ipt_mng.process_event(e)
            grp_mng.draw()
            snd_mng.tick()
            pygame.display.flip()
        pygame.quit()


if __name__ == '__main__':
    PythonClient().run()
