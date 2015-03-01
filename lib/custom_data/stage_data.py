"""This module contains classes for storing Stage information to be used
by the game engine.

Note that all classes in this module are read-only and should not have
their data modified after being instantiated.
"""


class StageData(object):
    """A data class that stores all of the required information about
    a battle stage.

    This data is retrieved from external XML files, which are read via
    functions within the stage_loader module.

    Attributes:
        name (String): The name of the Stage.
        subtitle (String): A tagline that appears below the Stage name
            in the Stage Select Screen.
        background (String): The file path to the backdrop image for
            this Stage.
        parallax (String): An optional file path that specifies another
            image drawn beneath the background. Unlike the latter, it
            will not be scrolled in order to give the scene a "layered"
            visual effect.
        x_offset (int): The horizontal displacement of the top-left
            corner of the screen relative to the background when the
            match starts.
        ground_level (int): The row of pixels on the background that
            specify where the characters' feet will touch while
            grounded.
        music (String): The file path to the audio file that will play
            as music while battling on this Stage.
    """
    def __init__(self):
        """Declare and initialize instance variables."""
        self.name = ''
        self.subtitle = ''
        self.background = ''
        self.parallax = ''
        self.x_offset = 0
        self.ground_level = 0
        self.music = ''
