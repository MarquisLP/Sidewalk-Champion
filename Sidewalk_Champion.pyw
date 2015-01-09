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
from lib.custom_data.settings_manager import SettingsManager
from lib.game_states.game_state_manager import *
from lib.globals import SCREEN_SIZE
from lib.globals import FULL_SCALE
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()

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
    settings_loader = SettingsManager()
    settings = settings_loader.load_settings()

    # We don't need the SettingsManager once it's finished loading data.
    del(settings_loader)

    display_flags = 0
    if settings.screen_scale == FULL_SCALE:
        display_flags = pygame.FULLSCREEN | pygame.HWSURFACE
    screen = pygame.display.set_mode((SCREEN_SIZE[0] * settings.screen_scale,
                                      SCREEN_SIZE[1] * settings.screen_scale),
                                     display_flags)
    pygame.display.set_caption('Sidewalk Champion')
    clock = pygame.time.Clock()

    state_manager = GameStateManager(screen, clock, settings)
    state_manager.run_game()
else:
    pygame.quit()
