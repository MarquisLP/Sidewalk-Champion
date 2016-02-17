from pygame.mixer import Sound
from customize.select_screens_sfx import *


class SelectStateSFX(object):
    """Plays sound effects that are used by both the Character Select
    State and the Stage Select State.

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
    def __init__(self, channel):
        """Declare and initialize instance variables.

        Args:
            channel: A PyGame Channel that will be used to play the
                Sounds.
        """
        self.channel = channel
        self.scroll = Sound(SCROLL_PATH)
        self.confirm = Sound(CONFIRM_PATH)
        self.cancel = Sound(CANCEL_PATH)
        self.no_confirm = Sound(NO_CONFIRM_PATH)

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

