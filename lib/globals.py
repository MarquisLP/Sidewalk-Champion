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
    INPUT_NAMES     A list containing all of the names for the possible
                    input 'buttons' in the game. Each one is bound to a
                    different key for each player.
"""
SCREEN_SIZE = (384, 226)
FULL_SCALE = 3
FRAME_RATE = 60.0
INPUT_NAMES = ["up", "back", "down", "forward", "light_punch",
               "medium_punch", "heavy_punch", "light_kick",
               "medium_kick", "heavy_kick", "start", "cancel"]
