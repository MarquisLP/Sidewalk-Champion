class SettingsData(object):
    """Stores options for game playback that can be modified by the
    players in the Settings screen.

    Attributes
        screen_scale        The window and all Graphics will be
                            magnified by this scale. This can be either 1, 2,
                            or 3; any other value will default to 1.
        show_box_display    Set to True if collision boxes are
                            displayed over the characters in battle.
        player1_keys        The key-binding Dictionary for player 1's
                            input buttons.
        player2_keys        The key-binding Dictionary for player 1's
                            input buttons.
    """
    def __init__(self):
        self.screen_scale = 2
        self.show_box_display = False
        self.player1_keys = self.default_p1_keys_dict()
        self.player2_keys = self.default_p2_keys_dict()

    def default_p1_keys_dict(self):
        """Return a key input dict with the default bindings for player 1.
        """
        bindings = {'up' : 'w',
                    'back' : 'a',
                    'down' : 's',
                    'forward' : 'd',
                    'light_punch' : 'r',
                    'medium_punch' : 't',
                    'heavy_punch' : 'y',
                    'light_kick' : 'f',
                    'medium_kick' : 'g',
                    'heavy_kick' : 'h',
                    'start' : 'left ctrl',
                    'cancel' : 'escape'}

        return bindings

    def default_p2_keys_dict(self):
        """Return a key input dict with the default bindings for player 2.
        """
        bindings = {'up' : 'up',
                    'back' : 'left',
                    'down' : 'down',
                    'forward' : 'right',
                    'light_punch' : '[7]',
                    'medium_punch' : '[8]',
                    'heavy_punch' : '[9]',
                    'light_kick' : '[4]',
                    'medium_kick' : '[5]',
                    'heavy_kick' : '[6]',
                    'start' : 'return',
                    'cancel' : 'backspace'}

        return bindings
