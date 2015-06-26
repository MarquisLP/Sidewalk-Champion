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
        preview (String): The file path to the image preview of the
            Stage that will be displayed when it is selected on the
            Stage Select screen.
        thumbnail (String): The file path to the selection thumbnail for
            the Stage on the Stage Select screen.
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
        self.preview = ''
        self.thumbnail = ''
        self.background = None
        self.parallax = None
        self.front_props = []
        self.back_props = []
        self.x_offset = 0
        self.ground_level = 0
        self.music = ''


class Background(object):
    """A data class storing information about a Stage's backdrop.

    Attributes:
        spritesheet_path (String): The file path to the backdrop
            animation sprite sheet.
        num_of_frames (int): The number of frames in the backdrop
            animation.
        frame_duration (int): The duration, in update cycles, that
            each animation frame will be displayed for.
    """
    def __init__(self):
        """Declare and initialize instance variables."""
        self.spritesheet_path = ''
        self.num_of_frames = 0
        self.frame_duration = 0


class Parallax(object):
        """A data class storing information about a Stage's parallax
        image, which is drawn beneath the backdrop and does not move
        when the screen scrolls.

        Attributes:
            spritesheet_path (String): The file path to the parallax
                animation sprite sheet.
            x_offset (int): The horizontal displacement, in pixels, of
                the parallax image from the top-left corner of the
                backdrop.
            y_offset (int): The vertical displacement, in pixels, of
                the parallax image from the top-left corner of the
                backdrop.
            num_of_frames (int): The number of frames in the parallax
                animation.
            frame_duration (int): The duration, in update cycles, that
                each animation frame will be displayed for.
        """
        def __init__(self):
            """Declare and initialize instance variables."""
            self.spritesheet_path = ''
            self.x_offset = 0
            self.y_offset = 0
            self.num_of_frames = 0
            self.frame_duration = 0


class FrontProp(object):
        """A data class storing information about one of the Stage's
        front props, which are drawn in the foreground above the
        fighters.

        Attributes:
            spritesheet_path (String): The file path to the front prop's
                animation sprite sheet.
            x_offset (int): The horizontal displacement, in pixels, of
                the front prop from the top-left corner of the backdrop.
            y_offset (int): The vertical displacement, in pixels, of
                the front prop from the top-left corner of the backdrop.
            num_of_frames (int): The number of frames in the front prop
                animation.
            frame_duration (int): The duration, in update cycles, that
                each animation frame will be displayed for.
        """
        def __init__(self):
            """Declare and initialize instance variables."""
            self.spritesheet_path = ''
            self.x_offset = 0
            self.y_offset = 0
            self.num_of_frames = 0
            self.frame_duration = 0


class BackProp(object):
        """A data class storing information about one of the Stage's
        back props, which are drawn over the backdrop and behind the
        fighters.

        Attributes:
            spritesheet_path (String): The file path to the back prop's
                animation sprite sheet.
            x_offset (int): The horizontal displacement, in pixels, of
                the back prop from the top-left corner of the backdrop.
            y_offset (int): The vertical displacement, in pixels, of
                the back prop from the top-left corner of the backdrop.
            num_of_frames (int): The number of frames in the back prop
                animation. Note that a back prop should be animated
                (i.e. possessing at least 2 frames), otherwise it may
                as well be edited into the Background image file.
            frame_duration (int): The duration, in update cycles, that
                each animation frame will be displayed for.
        """
        def __init__(self):
            """Declare and initialize instance variables."""
            self.spritesheet_path = ''
            self.x_offset = 0
            self.y_offset = 0
            self.num_of_frames = 0
            self.frame_duration = 0
