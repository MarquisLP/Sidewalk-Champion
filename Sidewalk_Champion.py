"""
* ************************************************
* Sidewalk Champion - A Customizable Fighting Game
* Author:           Mark Padilla
* Created:          3 May 2014
* Last Updated:     20 August 2014
* ************************************************
"""
import os
import pygame
from pygame.locals import *
from lib.custom_data.character_loader import CharacterLoader
from lib.custom_data.settings_manager import SettingsManager
from lib.game_states.game_state_manager import *
from lib.globals import SCREEN_SIZE
pygame.init()
pygame.mixer.init(44100)

def check_pygame_modules():
    success = True

    if pygame.display.get_init == False:
        success = False
    if pygame.font.get_init() == False:
        success = False
    if pygame.mixer.get_init() == False:
        success = False

    return success

# Do some necessary checks and load external data while the game starts up.
if check_pygame_modules() == True:
    char_loader = CharacterLoader()
    settings_loader = SettingsManager()
    all_characters = char_loader.load_all_characters()
    all_stages = []
    settings = settings_loader.load_settings()

    # We don't need these objects once they've finished loading data.
    del(char_loader)
    del(settings_loader)

    screen = pygame.display.set_mode((SCREEN_SIZE[0] * settings.screen_scale,
                                      SCREEN_SIZE[1] * settings.screen_scale))
    pygame.display.set_caption('Sidewalk Champion')
    clock = pygame.time.Clock()

    state_manager = GameStateManager(screen, clock, all_characters,
                                     all_stages, settings)
    state_manager.run_game()
else:
    pygame.quit()