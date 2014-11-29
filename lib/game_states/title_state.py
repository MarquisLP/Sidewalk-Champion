import sys
from __builtin__ import range
import pygame
from pygame.locals import *
from lib.globals import *
from lib.graphics import *
from lib.game_states.state import *
from lib.game_states.state_ids import StateIDs


class TitleState(State):
    """Handles the Title Screen of the game. It is also the first State
    that will be loaded and displayed.
    
    Class Constants:
        BG_PATH             The filepath for the background image.
        BG_SCROLL_SPEED     The speed, in pixels per second, at which
                            the background will be moved during the
                            intro animation.
        LOGO_PATH           The filepath for the logo image.
        LOGO_POSITION       The logo's top-left coordinates relative to
                            the screen.
        MUSIC_PATH          The filepath for the title theme music.
        VOICE_PATH          the filepath for the opening voice clip.
        CONFIRM_SOUND_PATH  The filepath for the 'confirm selection'
                            sfx.
        CANCEL_SOUND_PATH   The filepath for the 'cancel selection'
                            sfx.
        SCROLL_SOUND_PATH   The filepath for the 'change selection'
                            sfx.
        VOICE_DURATION      The duration, in update frames, of the
                            opening voice clip.
        PRESS_START_POS     The top-left coordinates of the 'Press
                            Start' text on-screen.
        CONFIRM_DURATION    The duration, in update frames, of the
                            confirmed text animation.
        POSSIBLE_ROUNDS     A List of the possible number of battle
                            rounds that can be selected by the players
                            during battle setup. In order, they are:
                            1, 3, and 5.
        POSSIBLE_TIMES      A List of the possible battle time limits,
                            in seconds, that can be selected by the
                            players during battle setup.
                            In order, they are: 30, 60, and 99.

    Attributes:
        state_manager       The GameStateManager object that manages
                            and updates this State.
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
        bg                  The background Animation object.
        logo                The logo Animation object.
        music               The PyGame Sound object that contains the
                            title theme.
        voice               The PyGame Sound object that contains the
                            opening voice clip.
        confirm_sound       The PyGame Sound object that contains the
                            'confirmed option' jingle.
        cancel_sound        The PyGame Sound object that contains the
                            'cancel option' jingle.
        scroll_sound        The PyGame Sound object that contains the
                            'change option' sound.
        voice_timer         A counter used to time the playing of the
                            opening voice clip.
        press_start_text    The TitleText object representing the
                            'Press Start' prompt.
        text_x_offset       The x-coordinate of all currently-displayed
                            text on the screen.
        displayed_text      A List containing the currently-displayed
                            set of TitleText objects that can be seen
                            and interacted with.
        options_list        A List of TitleText objects that represent
                            the selectable options from this State.
                            In order, they are: Battle, Training,
                            Settings, and Exit.
        battle_setup_text   A List of TitleText objects that represent
                            the selectable parameters when setting up
                            a new battle.
                            In order, they are: Rounds, Time Limit, and
                            Begin.
        selected_index      The index of the selected option e.g.
                            'Battle' or 'Settings'. These indices are
                            named via the TitleOptions enum and the
                            BattleSteup enum.
        has_pressed_start   Set to True if the players have already
                            pressed Start after the prompt.
        has_chosen_battle   Set to True if the players have highlighted
                            and confirmed Battle as their choice.
        confirmation_timer  A counter that increments after confirming
                            a selection. After the time specified by
                            CONFIRMATION_DURATION elapses, the screen
                            will move onto the next set of options or
                            the appropriate Game State.
                            Setting this to 0 will end the animation.
        player1_keys        The key bindings for Player 1, according to
                            the Dict of the same name in state_pass.
        player2_keys        The key bindings for Player 2, according to
                            the Dict of the same name in state_pass.
        battle_rounds_index The index of the selected Number of Battle
                            Rounds option, in accordance with the 
                            POSSIBLE_ROUNDS list.
        battle_time_index   The index of the selected Battle Time Limit
                            option, in accordance with the
                            POSSIBLE_TIMES List.
    """
    BG_PATH = 'images/title_back.png'
    BG_SCROLL_SPEED = 70.0
    LOGO_PATH = 'images/logo.png'
    LOGO_POSITION = (12, 40)
    MUSIC_PATH = 'audio/title_theme.wav'
    VOICE_PATH = 'audio/announcer-title.wav'
    CONFIRM_SOUND_PATH = 'audio/confirm.wav'
    CANCEL_SOUND_PATH = 'audio/cancel.wav'
    SCROLL_SOUND_PATH = 'audio/scroll.wav'
    VOICE_DURATION = 115
    PRESS_START_POS = (135, 150)
    CONFIRM_DURATION = 80
    POSSIBLE_ROUNDS = [1, 3, 5]
    POSSIBLE_TIMES = [30, 60, 99]

    # Initialization
    def __init__(self, state_manager, state_pass):
        """Declare and initialize instance variables.

        Keyword arguments:
            state_manager:  The GameStateManager object to which this
                            State belongs.
            state_pass      The StatePass object that will be
                            passed between all States.
        """
        super(TitleState, self).__init__(state_manager, state_pass)
        self.state_surface = Surface(SCREEN_SIZE)

        # Graphics
        self.bg = Animation(self.BG_PATH, (0.0, float(SCREEN_SIZE[1]) + 50.0),
                            7, 5)
        self.logo = Animation(self.LOGO_PATH, self.LOGO_POSITION, 6, 5, False)

        # Audio
        self.music = pygame.mixer.Sound(self.MUSIC_PATH)
        self.voice = pygame.mixer.Sound(self.VOICE_PATH)
        self.confirm_sound = pygame.mixer.Sound(self.CONFIRM_SOUND_PATH)
        self.cancel_sound = pygame.mixer.Sound(self.CANCEL_SOUND_PATH)
        self.scroll_sound = pygame.mixer.Sound(self.SCROLL_SOUND_PATH)

        # Intro
        self.voice_timer = 0

        # Text
        self.text_x_offset = 155
        self.press_start_text = TitleText('Press Start', 'white', False)
        self.displayed_text = []
        self.options_list = self.create_title_options()
        self.battle_setup_text = self.create_battle_setup_texts()
        self.selected_index = TitleOptions.BATTLE
        self.has_pressed_start = False
        self.has_chosen_battle = False
        self.confirmation_timer = 0

        # Key Bindings
        self.player1_keys = self.state_pass.settings.player1_keys
        self.player2_keys = self.state_pass.settings.player2_keys

        # Battle Setup
        self.battle_rounds_index = 1    # Initially 3 rounds.
        self.battle_time_index = 2      # Initially 99 seconds.

    def create_title_options(self):
        """Create all four of the title options (Battle, Training,
        Settings, and Exit) as TitleText objects and return them in
        a List.
        """
        battle_text = TitleText('Battle', 'dark grey', False)
        training_text = TitleText('Training', 'dark grey', False)
        settings_text = TitleText('Settings', 'dark grey', False)
        exit_text = TitleText('Exit', 'dark grey', False)

        return [battle_text, training_text, settings_text, exit_text]

    def create_battle_setup_texts(self):
        """Create the TitleText objects for the Battle Setup options
        and return them in a List. In order, this includes: Rounds,
        Time Limit, and Begin.
        """
        rounds_text = TitleText('Rounds       3', 'dark grey', False)
        time_limit_text = TitleText('Time Limit   99', 'dark grey', False)
        begin_text = TitleText('Begin', 'dark grey', False)
        
        return [rounds_text, time_limit_text, begin_text]

    # State Processing
    def load_state(self):
        """Prepare this State to be run and displayed in the game.
        """
        self.is_loaded = True
        self.displayed_text = [self.press_start_text]
        self.logo.image.set_alpha(0)
        self.is_intro_on = True

    def reset_state(self):
        """Reset this State to show the title animation once again."""
        self.has_pressed_start = False

        self.press_start_text.is_visible = True
        self.toggle_all_text_visibility(self.options_list, True)
        self.toggle_all_text_visibility(self.battle_setup_text, True)

    def update_state(self, time):
        """Update processing within this State."""
        if self.is_intro_on:
            self.animate_intro(time)
        if self.confirmation_timer > 0:
            self.animate_confirmed_text()

        self.draw_state()

    def draw_state(self):
        self.bg.draw(self.state_surface)
        self.logo.draw(self.state_surface)
        if not self.has_pressed_start:
            self.press_start_text.draw(self.state_surface,
                                       self.PRESS_START_POS)
        else:
            self.draw_title_texts(self.displayed_text)

    # Intro Animation
    def animate_intro(self, time):
        """Play the intro animation for this State.

        The animation sequence proceeds as follows:
        - Draw the background image just off the bottom edge of the
          screen.
        - Move the background up until it fits the entire screen.
        - Draw the logo completely transparent on the screen, with
          the animation turned off.
        - Gradually raise the logo's alpha value until it is opaque.
        - Play the opening voice over and wait for it to finish.
        - Start the music, enable the logo animation, and display the
          title screen options.

        The players can skip this sequence by pressing any button.

        Keyword arguments:
            time        The time elapsed, in seconds, since the last
                        update.
        """
        if self.bg.rect.y > 0:
            self.move_background_up(time)
        elif self.logo.image.get_alpha() < 255:
            self.fade_in_logo()
        
        if self.logo.image.get_alpha() > 15:
            if self.voice_timer <= 0:
                self.voice.play()
                self.voice_timer += 1
            elif self.voice_timer < self.VOICE_DURATION:
                self.voice_timer += 1
            else:
                self.voice_timer = 0
                self.logo.is_animated = True
                self.press_start_text.is_visible = True
                self.press_start_text.flash_mode = TextFlash.SLOW
                self.music.play(-1)
                self.is_intro_on = False

    def move_background_up(self, time):
        """Move the background up at the speed defined by
        BG_SCROLL_SPEED.

        Keyword arguments:
            time        The time elapsed, in seconds, since the last
                        update.
        """
        move_distance = self.BG_SCROLL_SPEED * time
        self.bg.move(0, -1.0 * move_distance)

        # Prevent the background from exceeding the top edge of the screen.
        if self.bg.rect.y < 0:
            self.bg.move(0, -1 * self.bg.rect.y)

    def fade_in_logo(self):
        """Gradually raise the logo's opacity."""
        old_alpha = self.logo.image.get_alpha()
        self.logo.image.set_alpha(old_alpha + 7)

    def skip_intro(self):
        """Skip the intro sequence."""
        self.bg.move(0, -1 * self.bg.rect.y)
        self.logo.image.set_alpha(255)
        self.logo.is_animated = True
        self.press_start_text.is_visible = True
        self.press_start_text.flash_mode = TextFlash.SLOW

        self.voice.play()
        self.music.play(-1)

        self.is_intro_on = False

    # Player Input
    def get_player_input(self, event):
        """Read input from the players and respond to it.
        
        Keyword arguments:
            event       The PyGame KEYDOWN event. It stores the ASCII
                        code for any keys that were pressed.
        """
        if self.is_intro_on == True:
            self.skip_intro()
        elif self.is_accepting_input == True:
            key_name = pygame.key.name(event.key)
            input_name = self.get_input_name(key_name)

            if input_name == 'start':
                # Only 'Begin' is confirmable in the Battle Setup display.
                if self.has_chosen_battle:
                    self.selected_index = BattleSetup.BEGIN
                    self.recolor_displayed_text()
                self.animate_confirmed_text()
            elif input_name in ['up', 'down'] and self.has_pressed_start:
                self.change_selected_text(input_name)
            elif input_name in ['back', 'forward'] and self.has_chosen_battle:
                if self.selected_index == BattleSetup.ROUNDS:
                    self.change_battle_rounds(input_name)
                elif self.selected_index == BattleSetup.TIME_LIMIT:
                    self.change_battle_time(input_name)
            elif input_name == 'cancel' and self.has_chosen_battle:
                    self.cancel_battle_setup()

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

    def change_selected_text(self, input_name):
        """Cycle selection through the available TitleText objects when
        Up or Down are pressed.

        Keyword arguments:
            input_name        The name of the entered input button.
        """
        self.scroll_sound.play()
        last_option_index = len(self.displayed_text) - 1

        if input_name == 'up':
            if self.selected_index <= 0:
                self.selected_index = last_option_index
            else:
                self.selected_index -= 1
            self.recolor_displayed_text()
        elif input_name == 'down':
            if self.selected_index >= last_option_index:
                self.selected_index = 0
            else:
                self.selected_index += 1
            self.recolor_displayed_text()

    def change_battle_rounds(self, input_name):
        """Change the number of Rounds that will be played during
        the next Battle.

        Keyword arguments:
            input_name        The name of the entered input button.
        """
        last_index = len(self.POSSIBLE_ROUNDS) - 1

        if input_name == 'back':
            if self.battle_rounds_index > 0:
                self.battle_rounds_index -= 1
        elif input_name == 'forward':
            if self.battle_rounds_index < last_index:
                self.battle_rounds_index += 1

        new_rounds = self.POSSIBLE_ROUNDS[self.battle_rounds_index]
        self.state_pass.battle_rounds = new_rounds

        # Re-write the text to indicate this new selection.
        new_text = 'Rounds       ' + str(new_rounds)
        self.battle_setup_text[BattleSetup.ROUNDS].rewrite_text(new_text)

    def change_battle_time(self, input_name):
        """Change the time limit for each Round in the next Battle.

        Keyword arguments:
            input_name        The name of the entered input button.
        """
        last_index = len(self.POSSIBLE_TIMES) - 1

        if input_name == 'back':
            if self.battle_time_index > 0:
                self.battle_time_index -= 1
        elif input_name == 'forward':
            if self.battle_time_index < last_index:
                self.battle_time_index += 1

        new_time = self.POSSIBLE_TIMES[self.battle_time_index]
        self.state_pass.time_limit = new_time

        # Re-write the text to indicate this new selection.
        new_text = 'Time Limit   ' + str(new_time)
        self.battle_setup_text[BattleSetup.TIME_LIMIT].rewrite_text(new_text)

    def cancel_battle_setup(self):
        """Return to the main option selection."""
        self.cancel_sound.play()
        self.has_chosen_battle = False
        self.text_x_offset = 155
        self.set_displayed_text(self.options_list)

    # Text Options
    def draw_title_texts(self, title_text_list):
        """Draw all of the TitleTexts from the specified List in order
        of their List index.
        """
        # Set the first text 15 pixels beneath the logo.
        text_y_offset = self.logo.get_bottom_edge() + 15

        for text in title_text_list:
            text.draw(self.state_surface, (self.text_x_offset, text_y_offset))

            # Draw the following text surface 5 pixels down.
            text_y_offset += text.get_height() + 5

    def set_displayed_text(self, text_list):
        """Change the List of TitleText objects that are currently
        displayed on the screen and that the players can interact with.

        Keyword arguments:
            text_list       The List of TitleText objects that will be
                            shown and activated.
        """
        self.toggle_all_text_visibility(self.displayed_text, False)

        self.displayed_text = text_list
        self.selected_index = 0
        self.toggle_all_text_visibility(text_list, True)
        self.recolor_displayed_text()

    def toggle_all_text_visibility(self, text_list, is_visible):
        """Toggles the visibility of all TitleText objects within
        the specified list.

        Keyword arguments:
            title_text_list     A List of TitleText objects that will
                                have their visibility toggled.
            is_visible          Set to True if the all of the TitleText
                                objects should be visible; False will
                                hide them.
        """
        for text in text_list:
            text.is_visible = is_visible

    def set_all_text_flash(self, text_list, flash_mode):
        """Set the flash mode for a list of TitleText objects.

        For the possible flash mode values, see the TextFlash
        enumeration.

        Args:
            text_list: A list of TitleText objects.
            flash_mode: An integer value based on the values from the
                TextFlash enumeration.
        """
        for text in text_list:
            text.is_visible = True
            text.flash_mode = flash_mode

    def recolor_displayed_text(self):
        """Change the color of all currently-available options to
        highlight the selected one. The highlighted one will be
        white, and all the others will be grey.
        """
        for i in range(0, len(self.displayed_text)):
            if i == self.selected_index:
                self.displayed_text[i].recolor_text('white')
            else:
                self.displayed_text[i].recolor_text('dark grey')

    def press_start(self):
        """Prepare and display the main options after the players
        complete the 'Press Start' prompt."""
        self.set_displayed_text(self.options_list)
        self.has_pressed_start = True

    def confirm_option(self):
        """Perform the appropriate operation based on which of the
        four possible options the players have selected.
        """
        if self.selected_index == TitleOptions.BATTLE:
            self.goto_battle()
        elif self.selected_index == TitleOptions.TRAINING:
            self.goto_training()
        elif self.selected_index == TitleOptions.SETTINGS:
            self.goto_settings()
        elif self.selected_index == TitleOptions.EXIT:
            pygame.quit()
            sys.exit()

    def start_new_battle(self):
        """After battle setup, go to the Character Selection screen
        with the selected battle settings.
        """
        self.state_pass.has_enter_transition = True
        self.change_state(StateIDs.BATTLE)

    def animate_confirmed_text(self):
        """Flash the on-screen text at a fast rate. Based on what is
        currently displayed, this can be the 'Press Enter' prompt,
        one of the four available options, or the 'Begin' text for
        setting up a Battle.
        Once the animation ends, the correct procedures will be called
        based on what was selected.
        """
        selected_index = self.selected_index

        self.confirmation_timer += 1

        if self.confirmation_timer <= 1:
            self.confirm_sound.play()
            self.is_accepting_input = False
            self.displayed_text[selected_index].is_visible = True
            self.displayed_text[selected_index].flash_mode = TextFlash.FAST
        elif self.confirmation_timer == self.CONFIRM_DURATION - 15:
            self.displayed_text[selected_index].is_visible = False
            self.displayed_text[selected_index].flash_mode = TextFlash.OFF
        elif self.confirmation_timer >= self.CONFIRM_DURATION:
            self.confirmation_timer = 0
            self.is_accepting_input = True

            if self.has_pressed_start == False:
                self.press_start()
            elif self.has_chosen_battle == False:
                self.confirm_option()
            else:
                self.start_new_battle()

    # Go To Another State
    def goto_battle(self):
        """Switch game processing to the Character Select screen
        for an upcoming battle.
        """
        self.has_chosen_battle = True
        self.text_x_offset = 130
        self.set_displayed_text(self.battle_setup_text)

    def goto_training(self):
        """Switch game processing to the Character Select Screen,
        with Training Mode options enabled.
        """
        self.state_pass.exit_transition_on = True
        self.state_pass.enter_transition_on = True
        self.state_pass.battle_rounds = 0
        self.state_pass.time_limit = 0
        self.change_state(StateIDs.BATTLE)

    def goto_settings(self):
        """Switch game processing to the Settings State."""
        self.set_all_text_flash(self.options_list, TextFlash.OFF)
        self.toggle_all_text_visibility(self.options_list, True)

        self.state_pass.will_reset_state = True
        self.state_pass.enter_transition_on = True
        self.change_state(StateIDs.SETTINGS)


class TitleOptions:
    """An enum that names each of the options on the title screen."""
    BATTLE = 0
    TRAINING = 1
    SETTINGS = 2
    EXIT = 3


class BattleSetup:
    """An enum that names each of the parameters on the Battle Setup
    display.
    """
    ROUNDS = 0
    TIME_LIMIT = 1
    BEGIN = 2


class TextFlash:
    """An enum that names each of the possible text flash modes for
    Title Screen text.
    """
    OFF = 0
    SLOW = 1
    FAST = 2


class TitleText:
    """Represents one of the text strings displayed on the Title
    Screen.

    Class Constants:
        FONT_PATH       The filepath to the font that will be used to
                        render the text.
        FONT_SIZE       The size of the font used for rendering the
                        text.

    Attributes:
        text            The on-screen text describing this option.
        color_name      The name of the font colour.
        text_font       The PyGame Font that will be used to render
                        the text.
        text_surf       The PyGame Surface where the text will be
                        rendered and drawn.
        flash_mode      Determines whether text flashes and the speed
                        of the flash. 0 turns of flashing, 1 flashes
                        every 40 frames, and 2 flashes every 5 frames.
                        Note that these values are labelled via the
                        TextFlash enum.
        flash_timer     A counter that increments each time this object
                        is updated while one of the flash modes is on.
                        If it matches the duration for the current
                        flash mode, the visibility of the text will be
                        toggled.
        is_visible      Set to True if the text should be visible on-
                        screen.
    """
    FONT_PATH = 'fonts/fighting-spirit-TBS.ttf'
    FONT_SIZE = 18

    # Initialization
    def __init__(self, text, color_name, is_visible=True,
                 flash_mode=TextFlash.OFF):
        """Declare and initialize instance variables.

        Keyword arguments:
            text        The text string that will be rendered.
            color_name  The name of the text color.
            is_visible  Set to True if the text is immediately visible
                        on-screen.
            flash_mode  Sets the type of flash for this text. See the
                        TextFlash enum for the possible options.
        """
        self.text = text
        self.color_name = color_name
        self.text_font = pygame.font.Font(self.FONT_PATH, self.FONT_SIZE)
        self.text_surf = self.render_text(text, color_name)
        self.flash_mode = flash_mode
        self.flash_timer = 0
        self.is_visible = is_visible

    # Get Info
    def get_height(self):
        """Return the height of the text Surface.
        This is useful when listing multiple TitleTexts underneath
        one another.
        """
        return self.text_surf.get_height()

    # Change Text Properties
    def render_text(self, text, color_name):
        """Render a new text Surface and return it.
        
        Keyword arguments:
            text        The text string that will be drawn onto the
                        Surface.
            color_name  The name of the colour used to render the
                        text.
        """
        self.color_name = color_name
        render_color = pygame.color.Color(color_name)
        new_surf = self.text_font.render(text, True, render_color)

        return new_surf

    def recolor_text(self, color_name):
        """Re-render text_surf with a different color.
        
        Keyword arguments:
            color_name      The name of the new text color.
        """
        self.text_surf = self.render_text(self.text, color_name)

    def rewrite_text(self, new_string):
        """Change the text string that is written on the text Surface.
        
        Keyword arguments:
            new_string      The new text content that will be
                            displayed on this object's Surface.
        """
        self.text = new_string
        self.text_surf = self.render_text(new_string, self.color_name)

    def flash(self):
        """Update the flash timer and toggle the text's visibility
        once it reaches the appropriate duration.
        """
        self.flash_timer += 1

        if (self.flash_mode == TextFlash.SLOW and self.flash_timer >= 45 or
           self.flash_mode == TextFlash.FAST and self.flash_timer >= 5):
            self.is_visible = not self.is_visible
            self.flash_timer = 0

    # Display Text
    def draw(self, surf, position):
        """Draw text_surf onto the specified Surface.
        
        Keyword arguments:
            surf        The Surface to draw the text onto.
            position    A tuple containing the top-left coordinates of
                        the text Surface relative to the external
                        Surface.
        """
        if self.flash_mode != TextFlash.OFF:
            self.flash()

        if self.is_visible == True:
            surf.blit(self.text_surf, position)