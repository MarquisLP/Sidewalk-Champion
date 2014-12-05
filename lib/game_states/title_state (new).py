import sys
from __builtin__ import range
import pygame
from pygame.locals import *
from pygame.mixer import Sound
from lib.globals import SCREEN_SIZE
from lib.globals import FRAME_RATE
from lib.graphics import Animation
from lib.game_states.state import *
from lib.game_states.state_ids import StateIDs


class Option(object):
    """An option that the players can select within the Title State.

    It is represented by a text name on the screen, which can be
    recolored or hidden to indicate player selection or confirmation.

    Class Constants:
        NORMAL_COLOR: A String name for the regular color of Option
            text.
        HIGHLIGHT_COLOR: A String name for the color of Option text
            when it is highlighted by the users.
        FONT_PATH: A String for the file path to the font file that
            will be used in rendering graphical text for Options.
        FONT_SIZE: An integer size of the font used in rendering Option
            text.

    Attributes:
        text: The text String that describes this Option. It will be
            written on the screen.
        is_visible: A Boolean indicating whether the text will be
            drawn onto its parent Surface.
        font: The PyGame Font object that stores the font used in
            rendering text.
        surf: The text graphic will be rendered onto this PyGame
            Surface.
    """
    NORMAL_COLOR = 'white'
    HIGHLIGHT_COLOR = 'dark gray'
    FONT_PATH = 'fonts/fighting-spirit-TBS.ttf'
    FONT_SIZE = 18

    def __init__(self):
        pass
