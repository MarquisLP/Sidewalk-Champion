from pygame.mixer import Sound


class SelectStateSFX(object):
    """Plays sound effects that are used by both the Character Select
    State and the Stage Select State.

    Class Constants:
        SCROLL_PATH: A String for the file path to the scroll items
            sound effect.
        CONFIRM_PATH: A String for the file path to the confirm choice
            sound effect.
        CANCEL_PATH: A String for the file path to the cancel selection sound
            effect.
        NO_CONFIRM_PATH: A String for the file path to the cannot confirm sound
            effect.

    Attributes:
        channel: A PyGame Channel where all of the sounds will be
            played.
        scroll: A PyGame Sound that plays when the players scroll
            through the list of available options.
        confirm: A PyGame Sound that plays when the players confirm a
            choice.
        cancel: A PyGame Sound that plays when the players cancel a choice or
            exit the State entirely.
        no_confirm: A PyGame Sound that plays when the players attempt to
            confirm when no choices are available, such as when no characters
            or stages could be loaded.
    """
    SCROLL_PATH = 'audio/scroll_char_stage.ogg'
    CONFIRM_PATH = 'audio/confirm.wav'
    CANCEL_PATH = 'audio/cancel.wav'
    NO_CONFIRM_PATH = 'audio/invalid.wav'

    def __init__(self, channel):
        """Declare and initialize instance variables.

        Args:
            channel: A PyGame Channel that will be used to play the
                Sounds.
        """
        self.channel = channel
        self.scroll = Sound(self.SCROLL_PATH)
        self.confirm = Sound(self.CONFIRM_PATH)
        self.cancel = Sound(self.CANCEL_PATH)
        self.no_confirm = Sound(self.NO_CONFIRM_PATH)

    def play_scroll(self):
        """Play the 'scroll items' sound effect."""
        self.channel.play(self.scroll)

    def play_confirm(self):
        """Play the 'confirm choice' sound effect."""
        self.channel.play(self.confirm)

    def play_cancel(self):
        """Play the 'cancel selection' sound effect."""
        self.channel.play(self.cancel)

    def play_no_confirm(self):
        """Play the 'cannot confirm choice' sound effect."""
        self.channel.play(self.no_confirm)

