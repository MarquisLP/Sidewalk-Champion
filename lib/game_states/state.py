from pygame.surface import Surface
from customize.globals import SCREEN_SIZE
from lib.custom_data.character_data import *
from exceptions import NotImplementedError
from __builtin__ import False


class State(object):
    """An abstract class that all Game States are derived from.

    A 'State' represents one of the many different screens that make up
    the game: Title Screen, Settings Screen, Battle Screen, etc.
    At its core, game processing consists of running the main game loop
    and updating the appropriate State on each iteration.
    Each State is essentially its own program with its own unique
    methods and attributes. Any data that needs to be shared between
    States is stored within a single StatePass object, which all States
    will reference.

    Attributes:
        state_manager: The GameStateManager object that manages and
            updates this State.
        state_pass: The StatePass object that stores data to pass onto
            other States.
        state_surface: All graphics in this State will be drawn
             onto this PyGame Surface.
        exact_offset: A tuple of floats that represent the coordinates
            of the upper-left corner of state_surface relative to the
            screen.
            However, graphics can only be drawn in whole pixels,
            so the coordinates will first need to be rounded and
            converted to integer values. Use the screen_offset() method
            to obtain drawing-friendly coordinates.
        is_accepting_input: A Boolean indicating whether this State is
            currently responding to player input.
    """
    def __init__(self, state_manager, state_pass):
        """Declare and initialize instance variables.

        state_manager       The GameStateManager object that manages
                            and updates this State.
        state_pass          The StatePass object that stores info to
                            pass onto other States.
        """
        self.state_pass = state_pass
        self.state_manager = state_manager
        self.state_surface = Surface(SCREEN_SIZE).convert()
        self.state_surface.set_alpha(255)
        self.exact_offset = (0.0, 0.0)
        self.is_accepting_input = True

    def load_state(self):
        """Use the information passed on from the parameters to set up
        the Game State and prepare it for use.
        """
        raise NotImplementedError

    def reset_state(self):
        """Reset the State to how it would look if it were loaded for
        the first time.
        """
        raise NotImplementedError

    def animate_intro(self, time):
        """Update the State's intro animation. This can be a fade-in,
        slide-in, or what-have-you.

        Keyword arguments:
            time    The time, in seconds, elapsed since the last
                    update. This can be used when moving objects,
                    which have their speeds set a rate measured in
                    pixels/second.
        """
        raise NotImplementedError

    def animate_exit(self, time):
        """Update the State's exiting animation. This can be a fade-out
        slide-out, or what-have-you.

        Keyword arguments:
            time    The time, in seconds, elapsed since the last
                    update. This can be used when moving objects,
                    which have their speeds set a rate measured in
                    pixels/second.
        """
        raise NotImplementedError

    def update_state(self, time):
        """Update all processes within the State.

        Keyword arguments:
            time    The time, in seconds, elapsed since the last
                    update. This can be used when moving objects,
                    which have their speeds set a rate measured in
                    pixels/second.
        """
        raise NotImplementedError

    def change_state(self, state_id):
        """Remove this State from the stack and switch processing to another
        State.

        Keyword arguments:
            state_id        The ID of the next State to run. For
                            reference, use the StateIDs enum class
                            within the state_ids module.
        """
        self.state_manager.change_state(state_id)

    def push_new_state(self, state_id):
        """Call another State to update and draw 'on top' of this one.

        This State will be left on the stack and if it is still visible on-
        screen, it will continue to be updated and drawn in addition to the
        new State.

        Keyword arguments:
            state_id        The ID of the next State to run. For
                            reference, use the StateIDs enum class
                            within the state_ids module.
        """
        self.state_manager.push_state(state_id)

    def discard_state(self):
        """Pop this State off the top of stack and switch processing the State
        that was active before it.

        Be careful not to call this method if this State is the only one on
        the stack - weird things may happen.
        """
        self.state_manager.pop_top_state()

    def get_last_state_id(self):
        """Return the index of the State that was active before this
        one.
        """
        return self.state_manager.previous_state_id

    def get_player_input(self, event):
        """Read input from the players and respond to it.

        Keyword arguments:
            event       The PyGame KEYDOWN event. It stores the ASCII
                        code for any keys that were pressed.
        """
        raise NotImplementedError

    def screen_offset(self):
        """Convert exact_offset into a tuple of integers and return
        it.
        """
        offset = (int(self.exact_offset[0]), int(self.exact_offset[1]))
        return offset

    def draw_state(self):
        """Draw all graphics within the State onto the screen."""
        raise NotImplementedError


