"""This module contains the StatePass class which defines the data
object that will be passed between Game States.
"""
from pygame.mixer import Channel
from lib.custom_data.settings_data import SettingsData


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
        character_one: The integer line index for for player one's
            character within the character list. Setting this to None
            means no character has been chosen yet.
        character_two: The integer line index for for player two's
            character within the character list. Setting this to None
            means no character has been chosen yet.
        stage: The integer line index for the chosen battle Stage within
            the stage list.  Setting this to None means no Stage has
            been chosen yet.
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
        self.character_one = None
        self.character_two = None
        self.stage = None
        self.battle_rounds = 3
        self.time_limit = 99
        self.settings = settings_data

