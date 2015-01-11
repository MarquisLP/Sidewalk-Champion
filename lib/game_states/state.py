from pygame.surface import Surface
from pygame.mixer import Channel
from lib.globals import SCREEN_SIZE
from lib.custom_data.character_data import *
from lib.custom_data.settings_data import SettingsData
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
        self.state_surface = Surface(SCREEN_SIZE)
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
        """Call another State for state_manager to display and update.

        Keyword arguments:
            state_id        The index of the next State to run. For
                            reference, use the StateIDs enum class
                            within the state_ids module.
        """
        self.state_manager.change_state(state_id)

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


class StatePass(object):
    """Stores common data that will be passed between Game States.

    All States should have reference to the same, singular StatePass
    object. In this way, when one State modifies the StatePass details,
    the details will automatically be updated for all other States as
    well.

    Attributes:
        announcer_channel: A PyGame Channel for playing announcer voice
            clips.
        ui_channel: A PyGame Channel for playing user interface sound
            effects.
        p1_channel_one: One of the two PyGame Channels that Player 1's
            character can use when playing action sounds.
        p2_channel_two: One of the two PyGame Channels that Player 1's
            character can use when playing action sounds.
        p2_channel_one: One of the two PyGame Channels that Player 2's
            character can use when playing action sounds.
        p2_channel_two: One of the two PyGame Channels that Player 2's
            character can use when playing action sounds.
        character_one: The CharacterData object for player one's
            character.
        character_two: The CharacterData object for player two's
            character.
        stage: The StageData object for the current battle's stage.
        battle_rounds: The number of rounds for the current
            battle. The possible values are 1, 3, and 5.
            Note that setting this to 0 means that Training Mode has
            been selected.
        time_limit: The amount of time, in seconds, allotted to each
            round in the upcoming battle. This can be 30, 60, or 99
            seconds.
            Note that setting this to 0 means that Training Mode has
            been selected.
        settings_data: A SettingsData object for various options that
            can be set by the players via the Settings Screen.
    """
    def __init__(self, settings_data):
        """Declare and initialize instance variables.

        Keyword arguments:
            settings_data: The SettingsData object that will be
                passed between all States.
        """
        self.announcer_channel = Channel(0)
        self.ui_channel = Channel(1)
        self.p1_channel_one = Channel(2)
        self.p1_channel_two = Channel(3)
        self.p2_channel_one = Channel(4)
        self.p2_channel_two = Channel(5)
        self.character_one = CharacterData()
        self.character_two = CharacterData()
        #self.stage = StageData()
        self.battle_rounds = 3
        self.time_limit = 99
        self.settings = settings_data
