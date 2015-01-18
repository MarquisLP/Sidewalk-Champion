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
        """Begin fading in the State Surface from black.

        This will set the State's Surface transparency to 0, in order
        to start the fade-in with a black screen.

        Args:
            state_surf: A Surface containing all of a Game State's
                graphical components.
        """
        state_surf.set_alpha(0)
        self.is_running = True
