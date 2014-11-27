from pygame import draw
from pygame.color import Color
from pygame.font import Font
from pygame.surface import Surface
from pygame.rect import Rect
from lib.globals import SCREEN_SIZE
from lib.game_states.state import State

class SettingsState(State):
    """Handles the game's Settings Screen. The players will be able to
    change several playback options here; these include:
    
    - The screen and window magnification.
    - The visibility of collision boxes during Battle.
    - The key bindings for both players.

    Class Constants:
        BG_PATH             The filepath to this State's background
                            image.
        SETTING_Y_OFFSET    The y-offset of the first Setting text.
        SETTING_DISTANCE    The vertical distance, in pixels, between
                            the text for each Setting.

    Attributes:
        state_pass          The StatePass object that stores info to
                            pass onto other States.
        is_loaded           Set to True if load_state() has already
                            been called for this object.       
        state_surface       All Graphics in this State will be drawn
                            onto this PyGame Surface.
        exact_offset        A pair of floats that represent the
                            coordinates of the upper-left point of
                            state_surface relative to the screen.
                            However, graphics can only be drawn in
                            whole pixels, so the coordinates will
                            first need to be converted to integer. Use
                            screen_offset() for this purpose.
        is_intro_on         Set to True if the intro animation for this
                            State is currently being shown.
        is_accepting_input  Set to True if the State object should
                            respond to player input. If False, all
                            input will be ignored.
        settings_list       A List of all the modifiable Settings
                            objects on this screen. They are all named
                            via the SettingNames enum.
        key_binding_list    A KeyBindingList object that contains all
                            of the players' key binding information.
        active_setting      The index of the currently-selected setting
                            within settings_list.
    """
    BG_PATH = 'images/settings_back.png'
    SETTING_Y_OFFSET = 17
    SETTING_DISTANCE = 20

    # Initialization
    def __init__(self, state_manager, state_pass):
        """Declare and initialize instance variables.

        Keyword arguments:
            state_pass      The StatePass object that will be
                            passed between all States.
        """
        super(SettingsState, self).__init__(state_manager, state_pass)
        self.settings_list = []
        self.create_all_settings()
        self.active_setting = 0

    def create_all_settings(self):
        """Create all Settings and add them to settings_list."""
        scale_setting = Setting('Window Scale', self.SETTING_Y_OFFSET,
                                '1x', '2x')
        collision_display_setting = Setting('Collision Box Display',
            self.SETTING_Y_OFFSET + self.SETTING_DISTANCE, 'ON', 'OFF')
        player_binding_setting = Setting('Set Key Bindings for',
            self.SETTING_Y_OFFSET + (2 * self.SETTING_DISTANCE), 'P1', 'P2')
        self.key_binding_list = KeyBindingList()

        self.settings_list.append(scale_setting)
        self.settings_list.append(collision_display_setting)

    # Player Input
    def get_player_input(self, event):
        """Read input from the players and respond to it.
        
        Keyword arguments:
            event       The PyGame KEYDOWN event. It stores the ASCII
                        code for any keys that were pressed.
        """
        key_name = pygame.key.name(event.key)
        input_name = self.get_input_name(key_name)

        if input_name in ['up', 'down']:
            self.cycle_settings(input_name)

    def get_input_name(self, key_name):
        """Check to see if the given key name matches any of the key
        bindings for either Player, and return the name of the
        matching input button. (e.g. 'forward', 'start')
        Return an empty string if no matches are found.

        Keyword arguments:
            key_name        The name of the key that was pressed.
        """
        for i in range(0, len(self.player1_keys)):
            if key_name == self.player1_keys.values()[i]:
                return self.player1_keys.keys()[i]

        for i in range(0, len(self.player2_keys)):
            if key_name == self.player2_keys.values()[i]:
                return self.player2_keys.keys()[i]

        return ''

    def cycle_settings(self, input_name):
        """Move selection to the next or previous Setting when the
        players press up or down.
        If the KeyBindingList is currently active, this will scroll
        through the key bindings instead.

        Keyword arguments:
            input_name      The name of the input entered by the
                            players. It should be 'up' or 'down'.
        """
        if self.active_setting != SettingNames.BINDING_LIST:
            if input_name == 'up':
                if self.active_setting == SettingNames.WINDOW_SCALE:
                    self.active_setting = SettingNames.BINDING_LIST
                else:
                    self.active_setting -= 1
            elif input_name == 'down':
                self.active_setting += 1
        else:
            if input_name == 'up':
                if self.key_binding_list.active_binding <= 0:
                    self.key_binding_list.active_binding = 0
                    self.active_setting = SettingNames.BINDING_PLAYER_NUM
                else:
                    self.key_binding_list.move_selection_up()
            elif input_name == 'down':
                if (self.key_binding_list.active_binding
                        >= self.key_binding_list.length() - 1):
                    self.key_binding_list.active_binding = 0
                    self.active_setting = SettingNames.WINDOW_SCALE
                else:
                    self.key_binding_list.move_selection_down()


class SettingNames(object):
    """An enum that labels each of the selectable Settings within
    SettingsState's settings_list."""
    WINDOW_SCALE = 0
    COLLISION_BOX_DISPLAY = 1
    BINDING_PLAYER_NUM = 2
    BINDING_LIST = 3


class Setting(object):
    """Represents one of the options on the Settings Screen that
    the players can select and modify.

    Class Constants:
        FONT_PATH           The filepath to the font file that will be
                            used for rendering text.
        FONT_SIZE           The font size of all Settings text.
        TEXT_COLOR          A tuple of RGBA values that represent the
                            color used in rendering text.
        UNDERLINE_SIZE      The thickness of all underlines, in pixels.
        UNDERLINE_COLOR     A tuple of RGBA values that represent the
                            color used in rendering underlines.
        SETTING_X_OFFSET    The x-coordinate of the top-left point of
                            all Settings texts relative to the screen.
                            This is a constant because all Settings
                            should line up as a column on-screen.
        OPTION_X_OFFSET     The x-coordinate of the top-left point of
                            the first option within every Setting.
                            Like the Setting texts, the first options
                            should all line up as a column.
        OPTION_DISTANCE     The horizontal distance, in pixels, between
                            each option for a given Setting.

    Attributes:
        text                The text String that will describe this
                            option on-screen. (e.g. 'Window Scale'.)
        settings_font       The PyGame Font used for rendering text.
        text_surf           The PyGame Surface where the text is drawn.
        y_offset            The y-coordinate of the top-left corner
                            relative to the screen for text_surf and
                            each Surface within option_surfs.
        options_text        A List of the possible options for this
                            Setting, represented as Strings.
                            For example, the 'Collision Box Display'
                            Settings can have 'ON' and 'OFF' as its
                            options.
        option_surfs        A List of Surfaces where the respective
                            options have their text rendered.
        active_option       The index of the currently-selected
                            option within options_text and
                            option_surfs.
    """
    FONT_PATH = 'fonts/corbel.ttf'
    FONT_SIZE = 14
    TEXT_COLOR = (204, 204, 204, 255)
    UNDERLINE_SIZE = 4
    UNDERLINE_COLOR = (30, 30, 30, 255)
    SETTING_X_OFFSET = 20
    OPTION_X_OFFSET = 210
    OPTION_DISTANCE = 20

    # Initialization
    def __init__(self, text, y_offset, *options):
        """Declare and initialize instance variables.

        Keyword arguments:
            text        The name of the Setting.
            y_offset    The y-coordinate of the top-left corner of
                        the text Surface relative to the screen.
            options     A tuple containing all of the selectable
                        option text for this Setting.
        """
        self.settings_font = Font(self.FONT_PATH, self.FONT_SIZE)
        self.text = text
        self.text_surf = self.render_text(text)
        self.y_offset = y_offset
        self.options_text = []
        self.option_surfs = []
        self.active_option = 0

        for option in options:
            self.add_option(option)

    def render_text(self, text):
        """Draw the specified text onto a new Surface and return it.

        Keyword arguments:
            text        The text that will be rendered.
        """
        new_surf = self.settings_font.render(text, True,
                                             Color(self.TEXT_COLOR))
        return new_surf

    def add_option(self, text):
        """Add a new option to this Setting. This will add entries to
        options_text and option_surfs.
        
        Keyword arguments:
            text        The text String that describes this option.
        """
        self.options_text.append(text)

        option_surf = self.render_text(text)
        self.option_surfs.append(option_surf)

    # Modification
    def underline_text(self, surf):
        """Re-render the specified text Surface with an underline
        beneath it and return it as a new Surface.

        Keyword arguments:
            surf        The text Surface that will be underlined.
        """
        new_surf = Surface((surf.get_width(),
                            surf.get_height() + self.UNDERLINE_SIZE))

        # Draw the underline onto a new Surface.
        line_rect = Rect(0, new_surf.get_height - self.UNDERLINE_SIZE + 1,
                         new_surf.get_width(), self.UNDERLINE_SIZE)
        draw.rect(new_surf, Color(self.UNDERLINE_COLOR), line_rect)

        # Re-draw the text on top of the underline.
        new_surf.blit(surf, (0, 0))

        return new_surf

    def underline_setting_text(self):
        """Underline text_surf for this Setting."""
        self.text_surf = self.underline_text(self.text_surf)

    def remove_setting_underline(self):
        """Redraw this Setting's text_surf without an underline."""
        self.text_surf = self.render_text(self.text)

    def remove_underline_in_all_options(self):
        """Redraw all of the option text for this Setting without any
        underlines.
        """
        for i in range(0, len(self.option_surfs)):
            self.option_surfs[i] = self.render_text(self.options_text[i])

    def change_selected_option(self, is_cycling_forward):
        """Change the currently-selected option by moving to the next
        option in forwards or backwards order.

        Keyword arguments:
            is_cycling_forward      Set to True if the next option to
                                    the right will be selected. False
                                    will select the option to the left.
        """
        if is_cycling_forward:
            self.active_option += 1
        else:
            self.active_option -= 1

        # Wrap around to the first or last option when needed.
        if self.active_option < 0:
            self.active_option = len(self.options_text) - 1
        elif self.active_option > len(self.options_text) - 1:
            self.active_option = 0

        self.remove_underline_in_all_options()
        # Underline the selected option.
        active_surf = self.option_surfs[self.active_option]
        self.option_surfs[self.active_option] = self.underline_text(
            active_surf)

    # Drawing
    def draw(self, surf):
        """Draw this Setting and its options onto the specified
        Surface.

        Keyword arguments:
            surf        The Surface that the text will be drawn onto.
        """
        self.draw_all_options(surf)

    def draw_all_options(self, surf):
        """Draw all options for this Setting onto the specified
        Surface.

         Keyword arguments:
            surf        The Surface that the text will be drawn onto.
        """
        # This will keep track of the current option's x-offset
        # in relation to the first option's left edge.
        current_x_offset = 0

        for option in self.option_surfs:
            surf_width = surf.get_width()
            surf_height = surf.get_height()
            option_rect = Rect(self.OPTION_X_OFFSET + current_x_offset,
                               self.y_offset, surf_width, surf_height)

            surf.blit(option, option_rect)

            # The next option will be positioned based on the current
            # option's width.
            current_x_offset += surf_width + self.OPTION_DISTANCE


class KeyBindingList(object):
    """Contains a list of key bindings that can be scrolled through
    and edited by the players.
    
    Class Constants:
        X_OFFSET        The x-coordinate of the top left corner of the
                        KeyBindingList relative to the screen.
        Y_OFFSET        The y-coordinate of the top left corner of the
                        KeyBindingList relative to the screen.
        LINE_DISTANCE   The vertical distance, in pixels, between each
                        line of key binding text.
        MAX_LINE        The maximum number of key bindings that will be
                        shown on the screen at a time.

    Attributes:
        binding_list
        active_binding
        binding_surf
        is_remapping
    """
    X_OFFSET = 0
    Y_OFFSET = 0
    LINE_DISTANCE = 5
    MAX_LINE = 3

    # Initialization
    def __init__(self):
        self.binding_list = []
        self.active_binding = 0
        self.binding_surf = Surface(SCREEN_SIZE)
        self.is_remapping = False

    def create_binding_list(self):
        pass

    # Selection
    def move_selection_up(self):
        """Select the previous key binding."""
        self.active_binding -= 1

    def move_selection_down(self):
        """Select the next key binding."""
        self.active_binding -= 1

    # Drawing
    def draw(self, surf):
        """Draw the key binding list onto the specified Surface.
        
        Keyword arguments:
            surf
        """
        pass

    def draw_bindings(self, surf):
        pass

    # Other
    def length(self):
        """Returns the number of items in binding_list."""
        return len(self.binding_list)


class KeyBinding(object):
    """Represents one of the input buttons for the game, as well as the
    key mapping of that button for each player.

    Attributes:
        input_name      The name of the input button.
                        (e.g. up, start, light punch.)
        player1_key     The name of the key that Player 1 mapped this
                        button to.
        player2_key     The name of the key that Player 1 mapped this
                        button to.
    """

    def __init__(self, input_name, player1_key, player2_key):
        """Declare and initialize instance variables.

        Keyword arguments:
            input_name      The name of the input button.
                            (e.g. up, start, light punch.)
            player1_key     The name of the key that Player 1 mapped this
                            button to.
            player2_key     The name of the key that Player 1 mapped this
                            button to.  
        """
        self.input_name = input_name
        self.player1_key = player1_key
        self.player2_key = player2_key