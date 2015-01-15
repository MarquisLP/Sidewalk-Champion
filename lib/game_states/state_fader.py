class StateFader(object):
    """Fades a State Surface in and out from black.

    When fading out, the next Game State will automatically take over game
    processing once the fade finishes.

    Class Constants:
        FADE_RATE: An integer for the amount of alpha transparency gained or
            lost by the State Surface during each update cycle.

    Attributes:
        next_state: An integer for the ID of the next Game State to go to after
            a fade-out. See the StateIDs enum for possible values.
            If this attribute is set to None, it will be assumed that a fade-in
            is meant to play, rather than a fade-out.
        change_state: A method that will remove the current Game State from the
            State stack and switch game processing over to a new State.
        is_running: A Boolean indicating whether the fade is still running.
    """
    FADE_RATE = 7
