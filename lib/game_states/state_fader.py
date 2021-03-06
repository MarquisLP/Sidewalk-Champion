import pygame.mixer
from customize.screen_transitions import *


class StateFader(object):
    """Fades a State Surface in and out from complete transparency.

    If the State Surface is the only one on the active State stack,
    this will create a fade-in or fade-out-to-black effect, due to a black
    background being drawn beneath all Game States.

    When fading out, the next Game State will automatically take over
    game processing once the fade finishes.

    Attributes:
        next_state: An integer for the ID of the next Game State to go
            to after a fade-out. See the StateIDs enum for possible
            values.
            If this attribute is set to None, it will be assumed that a
            fade-in is meant to play, rather than a fade-out.
        change_state: A method that will remove the current Game State
            from the State stack and switch game processing over to a
            new State.
        is_running: A Boolean indicating whether the fade is still
            running.
    """
    def __init__(self, change_state):
        """Declare and initialize instance variables.

        Args:
            change_state: A method that changes game processing to a new
                Game States, specified by the ID passed to the method's
                args.
        """
        self.next_state = None
        self.change_state = change_state
        self.is_running = False

    def start_fade_in(self, state_surf):
        """Begin fading in the State Surface.

        This will set the State's Surface transparency to 0, in order
        to start the fade-in with a black screen.

        Args:
            state_surf: A Surface containing all of a Game State's
                graphical components.
        """
        state_surf.set_alpha(0)
        self.is_running = True

    def start_fade_out(self, next_state):
        """Begin fading out the State Surface.

        If music is playing, it will begin fading out.

        Args:
            next_state: The ID of the next Game State to run once the
                fade finishes. For possible values, see the StateIDs
                enum.
        """
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.fadeout(MUSIC_FADEOUT_TIME)
        self.next_state = next_state
        self.is_running = True

    def update(self, time, state_surf):
        """Update the fade-in or fade-out.

        Args:
            time: A float for the time elapsed, in seconds, since the
                last update cycle.
            state_surf: A Surface containing all of a Game State's
                graphical components.
        """
        if self.next_state is None:
            self.fade_in_state(time, state_surf)
        else:
            self.fade_out_state(time, state_surf)

    def fade_in_state(self, time, state_surf):
        """Fade in a Game State's Surface.

        The fade will end once the Surface is completely opaque.

        Args:
            time: A float for the time elapsed, in seconds, since the
                last update cycle.
            state_surf: A Surface containing all of a Game State's
                graphical components.
        """
        old_alpha = state_surf.get_alpha()
        if old_alpha >= 255:
            self.is_running = False
        else:
            state_surf.set_alpha(old_alpha + (FADE_SPEED * time))

    def fade_out_state(self, time, state_surf):
        """Fade out a Game State's Surface.

        The fade will end once the Surface is completely transparent.
        Once this happens, the game will switch to the next Game State.

        Args:
            time: A float for the time elapsed, in seconds, since the
                last update cycle.
            state_surf: A Surface containing all of a Game State's
                graphical components.
        """
        old_alpha = state_surf.get_alpha()
        if old_alpha <= 0:
            self.is_running = False
            self.change_state(self.next_state)
        else:
            state_surf.set_alpha(old_alpha - (FADE_SPEED * time))
