from pygame.mixer import Sound

class SelectStateSFX(object):
    """Plays sound effects that are used by both the Character Select
    State and the Stage Select State.

    Class Constants:
        SCROLL_PATH: A String for the file path to the scroll items
            sound effect.
        CONFIRM_PATH: A String for the file path to the confirm choice
            sound effect.

    Attributes:
        channel: A PyGame Channel where all of the sounds will be
            played.
        scroll: A PyGame Sound that plays when the players scroll
            through the list of available options.
        confirm: A PyGame Sound that plays when the players confirm a
            choice.
    """
    SCROLL_PATH = 'audio/scroll_char_stage.ogg'
    CONFIRM_PATH = 'confirm.wav'

    def __init__(self, channel):
        """Declare and initialize instance variables.

        Args:
            channel: A PyGame Channel that will be used to play the
                Sounds.
        """
        self.channel = channel
        self.scroll = Sound(self.SCROLL_PATH)
        self.confirm = Sound(self.CONFIRM_PATH)
