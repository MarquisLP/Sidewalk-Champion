from enum import Enum


class StateIDs(Enum):
    """An enum containing names for each of the game states, as they
    are listed in order within GameStateManager's state_list.
    """
    TITLE = 0
    SETTINGS = 1
    SELECT_CHARACTER = 2
    SELECT_STAGE = 3
    BATTLE = 4
    SHUT_DOWN = 5

