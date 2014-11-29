class SettingsData(object):
    """Stores options for game playback that can be modified by the
    players in the Settings screen.
    
    Attributes
        screen_scale        The window and all Graphics will be
                            magnified by this scale. This can either be
                            1 or 2; any other value will default to 1.
        show_box_display    Set to True if collision boxes are
                            displayed over the characters in battle.
        player1_keys        The key-binding Dictionary for player 1's
                            input buttons.
        player2_keys        The key-binding Dictionary for player 1's
                            input buttons.
    """
    def __init__(self):
        self.screen_scale = 1
        self.show_box_display = False
        self.player1_keys = self.create_blank_keys_dict()
        self.player2_keys = self.create_blank_keys_dict()

    def create_blank_keys_dict(self):
        """Return a Dictionary with all of the input names as keys
        but with blank key-binding values.
        """
        bindings = {'up' : None,
                    'back' : None,
                    'down' : None,
                    'forward' : None,
                    'light_punch' : None,
                    'medium_punch' : None,
                    'heavy_punch' : None,
                    'light_kick' : None,
                    'medium_kick' : None,
                    'heavy_kick' : None,
                    'start' : None,
                    'cancel' : None}

        return bindings