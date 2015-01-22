"""This module contains global constants that are used throughout the
project.

Module Constants:
    SCREEN_SIZE     A tuple containing the width and height of the game
                    screen, in pixels and with a 1x scale factor.
    FULL_SCALE      An integer for the magnification factor that will cause
                    the game to toggle fullscreen display.
    FRAME_RATE      How many times the graphics and processes are
                    updated each second. The game uses a universal
                    'frame' unit to measure time; it is equivalent
                    to (1/FRAME_RATE) seconds.
    INPUT_NAMES     A tuple containing all of the names for the possible
                    input 'buttons' in the game. Each one is bound to a
                    different key for each player.
    DEFAULT_ACTIONS A tuple of Strings, containing the names of all
                    Actions that every character should have, such as
                    walking, blocking, and jumping.
"""
SCREEN_SIZE = (384, 226)
FULL_SCALE = 3
FRAME_RATE = 60.0
INPUT_NAMES = ("up", "back", "down", "forward", "light_punch",
               "medium_punch", "heavy_punch", "light_kick",
               "medium_kick", "heavy_kick", "start", "cancel")
DEFAULT_ACTIONS = ('intro',
                   'stand',
                   'walk',
                   'crouch_down',
                   'crouching_idle',
                   'jump_up',
                   'jump_forward',
                   'jump_back',
                   'block_standing',
                   'block_high',
                   'block_low',
                   'standing_recoil',
                   'crouching_recoil',
                   'jumping_recoil',
                   'tripped',
                   'launched',
                   'falling',
                   'knockdown',
                   'recover',
                   'dizzy',
                   'chip_ko',
                   'victory')