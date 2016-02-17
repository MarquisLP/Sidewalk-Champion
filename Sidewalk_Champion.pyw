"""
* ************************************************
* Sidewalk Champion - A Customizable Fighting Game
* Author:           Mark Padilla
* Created:          3 May 2014
* Last Updated:     28 August 2015
* ************************************************
"""
import os
import pygame
from pygame.locals import *
from lib.custom_data.settings_manager import load_settings
from lib.game_states.game_state_manager import *
from customize.globals import SCREEN_SIZE
from customize.globals import FULL_SCALE
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
    state_manager = GameStateManager()
    state_manager.run_game()
else:
    pygame.quit()
