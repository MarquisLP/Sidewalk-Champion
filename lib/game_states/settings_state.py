import pygame
from pygame import draw
from pygame.color import Color
from pygame.font import Font
from pygame.surface import Surface
from pygame.mixer import Sound
from lib.globals import SCREEN_SIZE
from lib.globals import INPUT_NAMES
from lib.globals import FRAME_RATE
from lib.graphics import Graphic
from lib.graphics import Animation
from lib.game_states.state import State
from lib.game_states.state import StatePass
from lib.custom_data.settings_manager import SettingsManager
from lib.custom_data.settings_data import SettingsData


class SettingsState(State):
    """The Settings Screen where players can modify certain in-game
    settings as well as their controls.

    This screen is made up of two major components: the upper Settings
    List that contains all of the "toggle-able" settings, and the lower
    Key Bindings List where players can rebind their keyboard controls.

    State flow consists of alternating between these two lists and
    modifying their contained items, as per the players' requests.

    Class Constants:
        BG_PATH: A string containing the file path for the background
            image.
        SLIDE_SFX_PATH: A string containing the file path for the
            slide-in sound effect.

        SCROLL_SFX_PATH: A string containing the file path for the
            scroll list sound effect.
        EXIT_SFX_PATH: A string containing the file path for the
            exit screen sound effect.
        SLIDE_SPEED: An integer that sets the speed at which the State
            Surface will slide, in pixels per second.

    Attributes:
        file_manager: The SettingsManager object that loads and saves
            data to the settings file.
        setting_list: The SettingList object that controls all of
            the available Settings.
        binding_list: The KeyBindingList object that controls all
            the available Key Bindings.
        bg_image: The PyGame image for the Settings Screen background.
        scroll_sound: A PyGame Sound that plays when the players select
            another item in the SettingList or KeyBindingList.
        slide_sound: A PyGame Sound that plays when the screen slides in
            or out of the window.
        is_editing_binding: A Boolean that indicates whether the next
            key press will be saved to the currently-selected Key
            Binding.
        is_leaving_state: A Boolean that indicates whether the game
            is currently in the process of exiting this State and going
            to another State.
    """
    BG_PATH = "images/settings_back.png"
    SLIDE_SFX_PATH = "audio/settings_slide.wav"
    SCROLL_SFX_PATH = "audio/scroll.wav"
    EXIT_SFX_PATH = "audio/cancel.wav"
    SLIDE_SPEED = 1000.0

    # Initialization
    def __init__(self, state_manager, state_pass):
        """Declare and initialize instance variables.

        Args:
            state_manager: The GameStateManager object to which this
                State belongs.
            state_pass: The StatePass object containing info to be
                passed between all Game States.

        @type state_manager: GameStateManager
        @type state_pass: StatePass
        """
        super(SettingsState, self).__init__(state_manager, state_pass)
        p1_bindings = self.state_pass.settings.player1_keys
        p2_bindings = self.state_pass.settings.player2_keys
        self.setting_list = SettingList(p1_bindings, p2_bindings)
        self.binding_list = self.setting_list.binding_list
        self.file_manager = SettingsManager()
        self.bg_image = Graphic(self.BG_PATH, (0.0, 0.0))
        self.slide_sound = Sound(self.SLIDE_SFX_PATH)
        self.scroll_sound = Sound(self.SCROLL_SFX_PATH)
        self.exit_sound = Sound(self.EXIT_SFX_PATH)
        self.is_editing_binding = False
        self.is_leaving_state = False

    def load_state(self):
        """Prepare this State to be run for the first time."""
        loaded = self.state_pass.settings
        scale_setting = self.setting_list.settings[SettingIndex.SCALE]
        display_setting = self.setting_list.settings[SettingIndex.SHOW_BOXES]

        scale_setting.set_selected_option(loaded.screen_scale - 1)
        display_setting.set_selected_option(int(loaded.show_box_display))

        self.reset_state()

    def reset_state(self):
        """Reset this State and prepare its introductory animation."""
        self.state_pass.will_reset_state = False

        scale = self.state_pass.settings.screen_scale
        self.exact_offset = (SCREEN_SIZE[0] * scale, 0.0)
        self.setting_list.set_selected_setting(SettingIndex.SCALE)
        self.binding_list.current_binding = -1

        self.is_accepting_input = False
        self.is_intro_on = True

    # Updating
    def update_state(self, time):
        """Update all processes within this State.

        Args:
            time: The time, in seconds, elapsed since the last
                    update.

        @type time: float
        """
        if self.is_intro_on:
            self.enter_state()
        elif self.is_leaving_state:
            self.leave_state()

        self.draw_state()

    # Sliding Animations
    def enter_state(self):
        """Show the introductory slide animation.

        It will end once the once the screen fills the entire window.
        """
        self.animate_slide()
        if self.exact_offset[0] <= 0.0:
            self.is_accepting_input = True
            self.is_intro_on = False

    def leave_state(self):
        """Leave the Settings Screen.

        First, the screen will slide out of the window. Once it is
        completely out of sight, the animation will end.
        Afterwards, data from this screen will be saved and processing
        will be sent to the previously-active Game State.
        """
        self.animate_slide(is_backwards=True)
        scale = self.state_pass.settings.screen_scale

        if self.exact_offset[0] >= SCREEN_SIZE[0] * scale:
            self.is_leaving_state = False
            self.update_game_settings()
            self.save_settings_to_file()

            self.state_pass.will_reset_state = False
            self.state_pass.enter_transition_on = False

            previous_state = self.state_manager.previous_state_id
            self.state_manager.change_state(previous_state)

    def animate_slide(self, is_backwards=False):
        """Slide the Settings Screen in or out of the game window.

        Args:
            is_backwards: A Boolean indicating whether the State Surface
                should slide out of the window, rather than into it.

        @type is_backwards: bool
        """
        self.draw_previous_state()

        scale = self.state_pass.settings.screen_scale
        distance = (self.SLIDE_SPEED / FRAME_RATE) * scale

        if not is_backwards:
            if self.exact_offset[0] >= SCREEN_SIZE[0] * scale:
                self.state_pass.ui_channel.play(self.slide_sound)

            new_x = self.exact_offset[0] - distance
            self.exact_offset = (new_x, 0.0)
            # Prevent the screen from going past the left edge of the window.
            if self.exact_offset[0] <= 0.0:
                self.exact_offset = (0.0, 0.0)
        else:
            if self.exact_offset[0] <= 0.0:
                self.state_pass.ui_channel.play(self.exit_sound)

            new_x = self.exact_offset[0] + distance
            self.exact_offset = (new_x, 0.0)
            # Prevent the screen from going past the right edge of the window.
            if self.exact_offset[0] >= SCREEN_SIZE[0] * scale:
                self.exact_offset = (SCREEN_SIZE[0] * scale, 0.0)

    def draw_previous_state(self):
        """Draw the previously-active Game State."""
        previous_state = self.state_manager.previous_state_id
        self.state_manager.update_state(previous_state)
        self.state_manager.draw_state(previous_state)

    # Input Handling
    def get_player_input(self, event):
        """Respond to input from the players.

        Args:
            event: The PyGame event that stores the current key input
                data.

        @type event: Event
        """
        if self.is_editing_binding:
            # Change a control.
            new_key = pygame.key.name(event.key)
            self.edit_selected_binding(new_key)
            self.is_editing_binding = False
        else:
            input_name = self.get_key_input(event)
            active_setting = self.setting_list.active_setting

            # Play list scrolling sound effect if applicable.
            if input_name in ['up', 'down', 'back', 'forward']:
                self.state_pass.ui_channel.play(self.scroll_sound)

            # Scroll the list.
            if input_name == 'up':
                self.scroll_selected_list(should_scroll_up=True)
            elif input_name == 'down':
                self.scroll_selected_list()

            # Activate 'Edit Controls' mode.
            if active_setting == SettingIndex.BINDING_LIST:
                if input_name == 'start':
                    self.binding_list.erase_selected_key()
                    self.is_editing_binding = True
            # Edit Setting values.
            elif input_name in ['back', 'forward']:
                if input_name == 'back':
                    self.setting_list.scroll_setting_options(
                        is_backwards=True)
                else:
                    self.setting_list.scroll_setting_options()
                # Change which player's key bindings are displayed
                # if requested.
                active_setting = self.setting_list.active_setting
                if active_setting == SettingIndex.PLAYER_NUM:
                    new_player = self.setting_list.get_binding_player()
                    self.binding_list.change_player(new_player)

            # Leave the Settings Screen.
            if input_name == 'cancel':
                self.update_game_settings()
                self.save_settings_to_file()
                self.is_leaving_state = True

    def get_key_input(self, event):
        """Determine the in-game input from a key press.
        (e.g. The enter key could be player 1's 'start' input.)

        Args:
            event: The PyGame Event that stores the current key
                input data.

        Returns:
            A String containing the name of the input pressed.
            If the key press doesn't match any key bindings, an empty
            String is returned.
        """
        key_name = pygame.key.name(event.key)
        p1_keys = self.state_pass.settings.player1_keys
        p2_keys = self.state_pass.settings.player2_keys

        for input_name in p1_keys.keys():
            if key_name == p1_keys[input_name]:
                return input_name

        for input_name in p2_keys.keys():
            if key_name == p2_keys[input_name]:
                return input_name

        return ''

    def edit_selected_binding(self, new_key):
        """Save a new key binding for the currently-selected input.

        Args:
            new_key: The name of the key that will be bound.
        """
        player_num = self.setting_list.get_binding_player()
        self.binding_list.edit_selected_binding(player_num, new_key,
                                                self.state_pass.ui_channel)

        self.update_key_bindings()

    def update_key_bindings(self):
        """Update the game's current Key Bindings with data from the Key
        Binding List.
        """
        self.state_pass.settings.player1_keys = (
            self.binding_list.get_bindings(1))
        self.state_pass.settings.player2_keys = (
            self.binding_list.get_bindings(2))

    def scroll_selected_list(self, should_scroll_up=False):
        """Scrolls through either the Setting List or the Key Binding
        List based on whichever one is currently selected.

        Args:
            should_scroll_up: A Boolean indicating whether the list
                should be scrolled up instead of down.
        """
        if self.setting_list.active_setting == SettingIndex.BINDING_LIST:
            self.binding_list.scroll_bindings(should_scroll_up)
        else:
            self.setting_list.scroll_selected_setting(should_scroll_up)

    # Saving Setting Data
    def update_game_settings(self):
        """Update the in-game Settings Data with data from the Settings
        List and Key Bindings List.
        """
        new_data = SettingsData()

        new_data.screen_scale = self.setting_list.get_screen_scale()
        new_data.show_box_display = self.setting_list.get_box_display()
        new_data.player1_keys = self.binding_list.get_bindings(1)
        new_data.player2_keys = self.binding_list.get_bindings(2)

        self.state_pass.settings = new_data

    def save_settings_to_file(self):
        """Save all of the Settings information from this State to the
        external settings file.
        """
        saved_data = SettingsData()
        new_data = self.state_pass.settings

        saved_data.screen_scale = new_data.screen_scale
        saved_data.show_box_display = new_data.show_box_display
        saved_data.player1_keys = new_data.player1_keys
        saved_data.player2_keys = new_data.player2_keys

        self.file_manager.save_settings(saved_data)

    # Drawing
    def draw_state(self):
        """Draw all of this State's contained graphics onto the State
        Surface.

        If the State Screen is currently in the process of sliding into
        or out of the window, the previously-active Game State will be
        drawn underneath it until the animation finishes.
        """
        if self.is_intro_on or self.is_leaving_state:
            self.draw_previous_state()

        self.bg_image.draw(self.state_surface)
        self.setting_list.draw(self.state_surface)
        self.binding_list.draw(self.state_surface)


class SettingIndex(object):
    """An enumeration that represents the available Settings within
    the Settings Screen.

    Literals:
        SCALE: The index of the setting that stores the current window
            magnification scale.
        SHOW_BOXES: the index of the Setting that determines whether
            collision boxes should be shown during battle.
        PLAYER_NUM: The index of the Setting that determines which
            player's controls are currently being edited by the Key
            Binding List.
        BINDING_LIST: An additional index that signifies that the
            Key Binding List has focus, rather than the Setting List.
    """
    SCALE = 0
    SHOW_BOXES = 1
    PLAYER_NUM = 2
    BINDING_LIST = 3


class SettingList(object):
    """Contains all of the Setting objects that will be displayed in
    and that can be modified from the Settings Screen.

    Class Constants:
        X: The x-position of the top of the list relative to the game
            screen.
        Y: The y-position of the top of the list relative to the game
            screen.
        SETTING_DISTANCE: The vertical distance between Setting text
            graphics, in pixels.

    Attributes:
        settings: A list containing all of the Settings in this State.
        binding_list: A KeyBindingList that controls all of the Key
            Bindings for both players.
        active_setting: An integer for the index of the currently-
            selected Setting.
    """
    X = 21
    Y = 17
    SETTING_DISTANCE = 15

    # Initialization
    def __init__(self, p1_bindings, p2_bindings):
        """Declare and initialize instance variables.

        @type p1_bindings: dict of (String, String)
        @type p2_bindings: dict of (String, String)
        """
        self.settings = self.create_all_settings()
        self.binding_list = KeyBindingList(self, p1_bindings, p2_bindings)
        self.active_setting = 0

    def create_all_settings(self):
        """Returns a list containing all of the Settings within the
        game's Settings Screen.

        :rtype : list of Setting
        """
        setting_list = []

        scale = Setting(self.X, self.Y, "Window Scale", "1x", "2x", "3x")
        box_display = Setting(self.X,
            self.Y + scale.get_height() + self.SETTING_DISTANCE,
            "Collision Box Display", "ON", "OFF")
        binding_player = Setting(self.X,
            self.Y + (box_display.get_height() * 2) +
            (self.SETTING_DISTANCE * 2),
            "Set Key Bindings for...", "Player 1", "Player 2")

        setting_list.append(scale)
        setting_list.append(box_display)
        setting_list.append(binding_player)

        return setting_list

    # Changing Selection
    def set_selected_setting(self, setting_index):
        """Set the focus to one of the Settings within the list.
        Indexes outside of the list range will automatically default to
        0 (Window Scale).

        Args:
            setting_index   The index of the setting to select, in
                            accordance with settings. See the
                            SettingIndex enum for information.
        """
        if setting_index not in range(0, len(self.settings)):
            setting_index = 0

        if self.active_setting != SettingIndex.BINDING_LIST:
            self.settings[self.active_setting].erase_underline()
        self.active_setting = setting_index
        self.settings[setting_index].add_underline()

    def scroll_selected_setting(self, is_reversed=False):
        """Select the next or previous Setting for modifying.
        If the scroll goes past the boundaries of the Setting List,
        focus will be sent to the KeyBindingList.
        If focus is on the Key Binding list, it will be scrolled
        instead.

        Args:
            is_reversed     If True, the previous Setting will be
                            selected, rather than the next.
        """
        if self.active_setting == SettingIndex.BINDING_LIST:
            self.binding_list.scroll_bindings()
        else:
            if not is_reversed:
                if self.active_setting >= len(self.settings) - 1:
                    # Scrolling past the bottom.
                    self.settings[self.active_setting].erase_underline()
                    self.active_setting = SettingIndex.BINDING_LIST
                    self.binding_list.go_to_list_top()
                else:
                    self.set_selected_setting(self.active_setting + 1)
            else:
                if self.active_setting <= 0:
                    # Scrolling past the top.
                    self.settings[self.active_setting].erase_underline()
                    self.active_setting = SettingIndex.BINDING_LIST
                    self.binding_list.go_to_list_bottom()
                else:
                    self.set_selected_setting(self.active_setting - 1)

    def scroll_setting_options(self, is_backwards=False):
        """Enable the current Setting's next or previous option.

        Args:
            is_backwards    If True, the previous option will be
                            selected, rather than the next.
        """
        self.settings[self.active_setting].scroll_options(is_backwards)

    # Drawing
    def draw(self, parent_surf):
        """Draw all Settings onto the specified Surface.

        Args:
            parent_surf     The Surface onto which the Setting List
                            will be drawn.
        """
        for setting_text in self.settings:
            setting_text.draw(parent_surf)

    # Retrieving Data
    def get_screen_scale(self):
        """Returns the window magnification as chosen through the
        Window Scale Setting.
        """
        scale_setting = self.settings[SettingIndex.SCALE]
        return scale_setting.selected_option + 1

    def get_box_display(self):
        """Returns a Boolean for showing the collision box display or
        not, as chosen through the Show Collision Boxes Setting.
        """
        show_boxes_setting = self.settings[SettingIndex.SHOW_BOXES]
        return bool(show_boxes_setting.selected_option)

    def get_binding_player(self):
        """Return the number of the player whose Key Bindings are
        currently selected for editing.
        """
        player_num_setting = self.settings[SettingIndex.PLAYER_NUM]
        player_num = player_num_setting.selected_option + 1
        return player_num


class Setting(object):
    """One of the Settings on the Settings Screen with selectable
    options.

    Class Constants:
        OPTION_DISTANCE     The horizontal distance, in pixels, between
                            each of the text graphics for options.
        OPTION_X            The x-coordinate for this Setting's first
                            option, relative to the Setting Surface.
        WIDTH               The width, in pixels, for the Setting
                            Surface.
        HEIGHT              The height, in pixels, for the Setting
                            Surface.

    Attributes:
        x                   The x-position for this Setting's Surface,
                            relative to the parent Surface.
        y                   The y-position for this Setting's Surface,
                            relative to the parent Surface.
        selected_option     The index of the currently-enabled option,
                            in accordance with options.
        text                The UnderlineText object that will render
                            and display this Setting's name.
        options             A list of UnderlineText objects that each
                            represent one of the possible options for
                            this Setting.
                            (e.g. "ON", "OFF")
        surf                The Surface onto which this Setting's name
                            and its options will be rendered.
    """
    OPTION_DISTANCE = 20
    OPTION_X = 200

    def __init__(self, x, y, name, *options):
        """Declare and initialize instance variables.

        Args:
            x           The x-position of the Setting text Surface,
                        relative to the parent Surface.
            y           The y-position of the Setting text Surface,
                        relative to the parent Surface.
            name        The text that will describe this Setting
                        on-screen.
            options     Multiple text Strings that will represent each
                        of the available options for this Setting.
                        (e.g. "ON", "OFF")
        """
        self.x = x
        self.y = y
        self.selected_option = 0
        self.text = UnderlineText(self.x, self.y, name)
        self.options = self.create_options(options)
        self.options[0].add_underline()

    def create_options(self, option_strings):
        """Create and return a list of UnderlineText objects that
        represent the available options for this Setting.

        Args:
            option_strings  A list of the text Strings that will
                            describe each option on-screen.
        """
        option_list = []

        new_x = self.OPTION_X
        for i in range(0, len(option_strings)):
            text = option_strings[i]

            new_option = UnderlineText(self.x + new_x, self.y, text)
            option_list.append(new_option)

            # The next option will be drawn OPTION_DISTANCE pixels away
            # from where the last option's Surface ends.
            new_x += option_list[i].get_width() + self.OPTION_DISTANCE
        return option_list

    def set_selected_option(self, option_num):
        """Set the currently-enabled option for this Setting.

         Args:
            option_num: An integer for the index of the desired option.

        Raises:
            An IndexError if option_num is out of bounds with the options
            list.
        """
        if option_num > len(self.options) - 1:
            raise IndexError

        self.options[self.selected_option].erase_underline()
        self.selected_option = option_num
        self.options[self.selected_option].add_underline()

    def scroll_options(self, is_backwards=False):
        """Based on player input, enable the next or previous option
        for this Setting.

        Args:
            is_backwards    If True, then the previous option will
                            be enabled rather than the next.
        """
        # The underlines will also be switched to show which option is
        # now enabled.
        last_option = len(self.options) - 1

        if is_backwards:
            if self.selected_option <= 0:
                self.set_selected_option(last_option)
            else:
                self.set_selected_option(self.selected_option - 1)
        else:
            if self.selected_option >= last_option:
                self.set_selected_option(0)
            else:
                self.set_selected_option(self.selected_option + 1)

    def add_underline(self):
        """Draws an underline underneath the Setting name."""
        self.text.add_underline()

    def erase_underline(self):
        """Re-renders the Setting name without the underline."""
        self.text.erase_underline()

    def get_height(self):
        """Return the height of the Setting name text graphic in
        pixels.
        """
        return self.text.get_height()

    def draw(self, parent_surf):
        """Draw the Setting text and all of its options onto the
        specified Surface.

        Args:
            parent_surf     The Surface onto which this Setting will be
                            drawn.
        """
        # First, draw all of the options onto the parent Surface.
        for option in self.options:
            option.draw(parent_surf)

        # Add in this Setting's name.
        self.text.draw(parent_surf)


class KeyBindingList(object):
    """Contains all of the key bindings for both players, as they will
    be shown on the Settings Screen.
    Due to screen space, only a set number of key bindings will be
    shown at a time. To access the others, this object will scroll
    through them based on the current selection.

    Class Constants:
        X                   The x-position of the main Surface,
                            relative to the parent Surface.
        Y                   The y-position of the main Surface.
                            relative to the parent Surface.
        REMAP_SFX_PATH      A string containing the file path for the
                            key remap sound effect.
        INVALID_SFX_PATH    A string containing the file path for the
                            invalid key sound effect.
        TEXT_DISTANCE       The vertical distance, in pixels, between
                            the top edges of the text graphic for each
                            Key Binding.
        BINDINGS_ON_SCREEN  The number of key bindings that will be
                            shown on-screen at any one time.
        UP_ARROW_PATH       The filepath for the scroll up arrow
                            sprite sheet.
        DOWN_ARROW_PATH     The filepath for the scroll down arrow
                            sprite sheet.
        ARROW_X             The x-position of both arrows on the main
                            Surface.
        UP_ARROW_Y          The y-position of the up arrow on the
                            main Surface.
        DOWN_ARROW_Y        The y-position of the down arrow on the
                            main Surface.
        ARROW_FRAMES        The number of frames in the scroll arrows'
                            sprite sheets.
        ARROW_DURATION      The duration of each frame in the scroll
                            arrows' animations, in pixels per second.

    Attributes:
        setting_list        The SettingList object that controls all
                            other Settings in this game state.
        remap_sound         A PyGame Sound that plays when a key binding
                            is remapped to different key.
        invalid_sound       A PyGame Sound that plays when the game
                            stops the players from remapping a key that
                            is already bound to an input.
        bindings            A list containing all of the KeyBinding
                            objects within the Settings State.
        current_binding     The index of the currently-selected
                            binding, in accordance with bindings.
                            If no items in this list are currently
                            selected, this value will be -1.
        up_arrow            A simple scroll up arrow animation. Will
                            be displayed when the list can be scrolled
                            up to show more bindings.
        down_arrow          A simple scroll down arrow animation. Will
                            be displayed when the list can be scrolled
                            down to show more bindings.
        top_binding         The index of the key binding currently
                            shown
    """
    X = 52
    Y = 115
    REMAP_SFX_PATH = "audio/settings_remap.wav"
    INVALID_SFX_PATH = "audio/invalid.wav"
    TEXT_DISTANCE = 23
    BINDINGS_ON_SCREEN = 4
    UP_ARROW_PATH = "images/settings_arrow_up.png"
    DOWN_ARROW_PATH = "images/settings_arrow_down.png"
    ARROW_X = 125.0
    UP_ARROW_Y = 0.0
    DOWN_ARROW_Y = 86.0
    ARROW_FRAMES = 2
    ARROW_DURATION = 10

    # Initialization
    def __init__(self, setting_list, p1_bindings, p2_bindings):
        """Declare and initialize instance variables.

        Args:
            setting_list    The SettingList object that controls the
                            other Settings on this screen.
            p1_bindings     A dict containing player 1's current key
                            bindings.
            p2_bindings     A dict containing player 2's current key
                            bindings.
        """
        self.setting_list = setting_list
        self.remap_sound = Sound(self.REMAP_SFX_PATH)
        self.invalid_sound = Sound(self.INVALID_SFX_PATH)
        self.bindings = self.load_bindings(p1_bindings, p2_bindings)
        self.current_binding = 0
        self.top_binding = 0
        self.up_arrow = Animation(self.UP_ARROW_PATH,
            (self.X + self.ARROW_X, self.Y + self.UP_ARROW_Y),
            self.ARROW_FRAMES, self.ARROW_DURATION)
        self.down_arrow = Animation(self.DOWN_ARROW_PATH,
            (self.X + self.ARROW_X, self.Y + self.DOWN_ARROW_Y),
            self.ARROW_FRAMES, self.ARROW_DURATION)

    def load_bindings(self, p1_bindings, p2_bindings):
        """Create all KeyBinding objects in a list and return them.

        Args:
            p1_bindings     A dict containing player 1's current key
                            bindings.
            p2_bindings     A dict containing player 2's current key
                            bindings.
        """
        binding_list = []
        text_y = 0

        for input_name in INPUT_NAMES:
            p1_key = p1_bindings[input_name]
            p2_key = p2_bindings[input_name]

            new_binding = KeyBinding(self.X, self.Y + text_y, input_name,
                                     p1_key, p2_key)
            binding_list.append(new_binding)

            # The next Key Binding will be drawn a set distance beneath
            # the previous one.
            text_y += self.TEXT_DISTANCE

        return binding_list

    # Changing Selection
    def set_selected_binding(self, binding_index):
        """Set focus to the KeyBinding of a specified index.

        Args:
            binding_index: The index of the KeyBinding to select, in
                accordance with bindings.

        Raises:
            An IndexError if the new index is out of bounds with the
            Key Binding list.
        """
        if binding_index not in range(0, len(self.bindings)):
            raise IndexError

        self.bindings[self.current_binding].erase_underline()
        self.current_binding = binding_index
        self.bindings[binding_index].add_underline()

    def go_to_list_top(self):
        """Set selection to the first Key Binding."""
        self.set_selected_binding(0)
        self.top_binding = 0
        self.move_binding_display()

    def go_to_list_bottom(self):
        """Set selection to the last Key Binding."""
        last_binding = len(self.bindings) - 1

        self.set_selected_binding(last_binding)
        self.top_binding = last_binding - self.BINDINGS_ON_SCREEN + 1
        self.move_binding_display()

    def scroll_bindings(self, is_reversed=False):
        """Scroll through the available bindings to the next or
        previous one.
        If the scroll exceeds the boundary of the bindings list, focus
        will be sent to the SettingList.

        Args:
            is_reversed     Set to True if the previous binding should
                            be selected, rather than the next.
        """
        if is_reversed == False:
            if self.current_binding >= len(self.bindings) - 1:
                # Scrolling past the bottom.
                self.bindings[self.current_binding].erase_underline()
                self.setting_list.set_selected_setting(SettingIndex.SCALE)
            else:
                self.set_selected_binding(self.current_binding + 1)
                self.scroll_binding_display()
        else:
            if self.current_binding <= 0:
                # Scrolling past the top.
                self.bindings[self.current_binding].erase_underline()
                self.setting_list.set_selected_setting(
                    SettingIndex.PLAYER_NUM)
            else:
                self.set_selected_binding(self.current_binding - 1)
                self.scroll_binding_display()

    def scroll_binding_display(self):
        """Display the next or previous set of Key Bindings based on
        which Binding is currently selected.
        """
        low_binding = self.top_binding + self.BINDINGS_ON_SCREEN - 1

        if self.current_binding > low_binding:
            self.top_binding += 1
            self.move_binding_display()
        elif self.current_binding < self.top_binding:
            self.top_binding -= 1
            self.move_binding_display()

    def move_binding_display(self):
        """Determine which key bindings will be drawn onto the screen
        at present and reposition them appropriately.

        These Bindings will start at the one defined by top_binding,
        and include a number of the following bindings such that the
        screen is always filled a specific number of Bindings.

        Note:
            The number of Key Bindings on the screen at any one time is
            defined by the BINDINGS_ON_SCREEN constant.
        """
        # The top binding can't be lower than the number of bindings
        # needed to fill the screen.
        max_top_binding = len(self.bindings) - self.BINDINGS_ON_SCREEN
        if self.top_binding > max_top_binding:
            self.top_binding = max_top_binding

        bottom_binding = self.top_binding + self.BINDINGS_ON_SCREEN - 1
        new_y = 0
        for index in range(self.top_binding, bottom_binding + 1):
            self.bindings[index].set_y(self.Y + new_y)
            new_y += self.TEXT_DISTANCE

    # Rebinding
    def edit_selected_binding(self, player_num, new_key, channel):
        """Change the value of the currently-selected key binding
        for one of the players.

        If the specified key is already bound, the rebinding operation
        will not be performed.

        Args:
            player_num: Either 1 or 2, for player 1 and 2 respectively.
                Any other value will default to 2.
            new_key: The name of the new key to set in the key binding.
            channel: The PyGame Channel that will be used to play sound
                effects for a successful or unsuccessful key binding.
        """
        if player_num == 1:
            last_key = self.bindings[self.current_binding].p1_binding
        else:
            last_key = self.bindings[self.current_binding].p2_binding

        if self.key_is_bound(new_key) and new_key != last_key:
            # Redraw the name of the key that was previously bound.
            self.bindings[self.current_binding].rebind(player_num, last_key)
            channel.play(self.invalid_sound)
        else:
            self.bindings[self.current_binding].rebind(player_num, new_key)
            channel.play(self.remap_sound)

    def key_is_bound(self, key_name):
        """Determine whether the specified key is already bound to
        one of the player's controls.

        Args:
            key_name: A String for the name of the key that will be
                checked.

        Returns:
            True if the key exists within one of the player's key
            binding dicts; false is returned otherwise.
        """
        bound_keys = []
        for binding in self.bindings:
            bound_keys.append(binding.p1_binding)
            bound_keys.append(binding.p2_binding)

        if key_name in bound_keys:
            return True
        else:
            return False

    def erase_selected_key(self):
        """Erase the key name text for the currently-selected
        Key Binding.
        """
        self.bindings[self.current_binding].erase_key_text()

    # Retrieving Data
    def get_bindings(self, player_num):
        """Return all of the key bindings for player 1 or 2.

        Args:
            player_num      Either 1 or 2, for player 1 and 2
                            respectively.
                            Any other value will default to 2.
        """
        binding_list = dict()

        for binding in self.bindings:
            input_name = binding.input_name

            if player_num == 1:
                key_name = binding.p1_binding
            else:
                key_name = binding.p2_binding

            binding_list[input_name] = key_name

        return binding_list

    # Drawing
    def change_player(self, player_num):
        """Display the key bindings for one of the players.

        Args:
            player_num: An integer of 1 or 2, for player 1 and 2
                respectively. Any other value will default to 2.
        """
        for binding in self.bindings:
            binding.change_player(player_num)

    def draw(self, parent_surf):
        """Draw onto a Surface, four Key Bindings within range of the
        currently-selected one.

        Args:
            parent_surf: The Surface upon which all of the Key Binding
                text will be drawn.

        @type parent_surf: SurfaceType
        """
        for index in range(self.top_binding, self.top_binding +
                self.BINDINGS_ON_SCREEN):
            self.bindings[index].draw(parent_surf)

        self.draw_arrows(parent_surf)

    def draw_arrows(self, parent_surf):
        """Draw the scrolling arrows if appropriate.

        The top arrow will only be drawn if there are more Key Bindings
        above what is currently displayed, and the bottom arrow will
        only be drawn if there are more below it.

        Args:
            parent_surf: The Surface upon which the arrows will be
                drawn.
        """
        if self.top_binding > 0:
            self.up_arrow.draw(parent_surf)
        if self.top_binding + 3 < len(self.bindings) - 1:
            self.down_arrow.draw(parent_surf)


class KeyBinding(object):
    """Stores the keys that both players use for a certain input
    within the game.

    Class Constants:
        TEXT_SPACING    The horizontal distance, in pixels, between each
                        of the UnderlineText objects.
        KEY_TEXT_X      The x-position of the text for the key's name.

    Attributes:
        x               The x-position of the main
        input_name      The name of the in-game input.
                        (e.g. forward, start.)
        p1_binding      The name of the keyboard key binded to
                        player 1's input.
        p2_binding      The name of the keyboard key binded to
                        player 2's input.
        input_text      The UnderlineText object that will render
                        and display the input name.
        key_text        The UnderlineText object that will render
                        and display the current player's binding.
    """
    TEXT_SPACING = 15
    KEY_TEXT_X = 175

    def __init__(self, x, y, input_name, p1_binding, p2_binding):
        self.x = x
        self.y = y
        self.input_name = input_name
        self.p1_binding = p1_binding
        self.p2_binding = p2_binding
        self.input_text = UnderlineText(self.x, self.y,
                                        self.format_input_text(input_name))
        self.key_text = UnderlineText(self.x + self.KEY_TEXT_X, self.y,
                                      p1_binding)

    def format_input_text(self, xml_string):
        """Convert an input name read from an XML file into a word
        or words with spaces and proper capitalization.

        Args:
            xml_string: The String read from an XML Element. It should
                describe one of the possible in-game inputs.
                (e.g. 'forward', 'start', 'light_punch')

        Returns:
            A String with spaces between words, which have been
            capitalized.

        @type xml_string: String
        """
        new_string = xml_string.replace('_', ' ')
        new_string = new_string.title()
        return new_string

    def rebind(self, player_num, new_key):
        """Change the binding key for the specified player.

        Args:
            player_num      Either 1 or 2, for Player 1 and 2
                            respectively. Any other value will
                            default to Player 2.
            new_key         The name of the new key that will
                            be bound to this input.
        """
        if player_num == 1:
            self.p1_binding = new_key
        else:
            self.p2_binding = new_key

        self.key_text.change_text(new_key)

    def change_player(self, player_num):
        """Display the key binding for one of the players.

        Args:
            player_num: An integer of 1 or 2, for player 1 and 2
                respectively. Any other value will default to 2.
        """
        if player_num == 1:
            self.key_text.change_text(self.p1_binding)
        else:
            self.key_text.change_text(self.p2_binding)

    def add_underline(self):
        """Draw an underline on the input name text."""
        self.input_text.add_underline()

    def erase_underline(self):
        """Redraw the input name text without an underline."""
        self.input_text.erase_underline()

    def erase_key_text(self):
        """Erase the text for the key name."""
        self.key_text.change_text("")

    def set_y(self, new_y):
        """Move this Key Binding to a new vertical position on-screen.

        Args:
            new_y: An integer for the new y-coordinate of this Key
                Binding relative to the game screen.
        """
        self.y = new_y
        self.input_text.y = new_y
        self.key_text.y = new_y

    def get_height(self):
        """Return the height of the input text graphic, in pixels."""
        return self.key_text.get_height()

    def draw(self, parent_surf):
        """Draws the text graphics for this key binding onto the
        specified Surface.

        Args:
            parent_surf     The Surface upon which the text will be
                            drawn.
        """
        self.input_text.draw(parent_surf)
        self.key_text.draw(parent_surf)


class UnderlineText(object):
    """Represents a text graphic that can be underlined.

    Class Constants:
        FONT_PATH           The filepath to the font used for rendering
                            text.
        FONT_COLOUR         The hexadecimal value for the colour used
                            in rendering the text.
        FONT_SIZE           The size of the font used for rendering the
                            text.
        UNDERLINE_COLOUR    The hexadecimal value for the colour used
                            in rendering the underline.
        UNDERLINE_SIZE      The height of the underline, in pixels.
        COLORKEY            The name of the color used in colorkeying
                            the Surface to create a transparent
                            background.

    Attributes:
        text    The string of text that will be shown.
        font    The PyGame font object that will be used for rendering
                the text.
        x       The x-position of the Surface relative to the parent
                Surface.
        y       The y-position of the Surface relative to the parent
                Surface.
        surf    The Surface onto which the text will be rendered.
    """
    FONT_PATH = "fonts/corbel.ttf"
    FONT_COLOUR = "0xFFFFFF"
    FONT_SIZE = 16
    #UNDERLINE_COLOUR = "0x1E1E1E"
    UNDERLINE_COLOUR = "0x888888"
    UNDERLINE_SIZE = 4
    COLORKEY = "grey20"

    def __init__(self, x, y, text):
        """Define and initialize instance variables.

        Args:
            x       The x-position for this object relative to its
                    parent Surface.
            y       The x-position for this object relative to its
                    parent Surface.
            text    The text that will be rendered onto this object's
                    Surface.
        """
        self.x = x
        self.y = y
        self.text = text
        self.font = Font(self.FONT_PATH, self.FONT_SIZE)
        self.surf = self.render_text(text)

    def render_text(self, text):
        """Render the specified text onto a new Suface and return
        it.

        Args:
            text        The string of text that will be drawn.
        """
        text_render = self.font.render(text, True, Color(self.FONT_COLOUR))
        text_width = text_render.get_width()
        text_height = text_render.get_height()

        # In order to enable proper antialiasing on the text, it will need to
        # be drawn on top of a colorkeyed Surface.
        new_surf = Surface((text_width, text_height))
        new_surf.fill(Color(self.COLORKEY))
        new_surf.set_colorkey(Color(self.COLORKEY))
        new_surf.blit(text_render, (0, 0))

        return new_surf

    def change_text(self, new_text):
        """Redraw the text Surface with a new text string.

        Args:
            new_text    The new text string that will be
                        written on the text Surface.
        """
        self.text = new_text
        self.surf = self.render_text(new_text)

    def add_underline(self):
        """Draws an underline on the text Surface, on top the text."""
        # The underline will be drawn from the bottom of the text Surface
        # and will extend its entire horizontal length.
        text_width = self.surf.get_width()
        text_height = self.surf.get_height()

        start_point = (0, text_height - 4)
        end_point = (text_width, text_height - 4)

        # The underline is drawn onto a new Surface with the same dimensions
        # as the text Surface, but slightly taller to account for the
        # underline. The text is drawn on top.
        new_surf = Surface((text_width, text_height + 4), pygame.SRCALPHA, 32)
        new_surf = new_surf.convert_alpha()
        draw.line(new_surf, Color(self.UNDERLINE_COLOUR), start_point,
                  end_point, self.UNDERLINE_SIZE)
        new_surf.blit(self.surf, (0, 0))

        self.surf = new_surf

    def erase_underline(self):
        """Re-renders the text Surface without an underline."""
        self.surf = self.render_text(self.text)

    def get_width(self):
        """Return the horizontal length of the text Surface."""
        return self.surf.get_width()

    def get_height(self):
        """Return the vertical length of the text graphic in pixels."""
        return self.surf.get_height()

    def draw(self, parent_surf):
        """Draws the text Surface onto the specified Surface.

        Args:
            parent_surf     The Surface onto which the text graphic
                            will be displayed.
        """
        parent_surf.blit(self.surf, (self.x, self.y))