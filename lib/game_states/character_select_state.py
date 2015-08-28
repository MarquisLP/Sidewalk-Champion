from math import ceil as round_up
import collections
import pygame.transform as transform
import pygame.draw
import pygame.locals
from pygame import image
from pygame.surface import Surface
from pygame.rect import Rect
from lib.graphics import load_tuple_of_images
from lib.graphics import render_outlined_text
from lib.graphics import convert_to_colorkey_alpha
from lib.graphics import Graphic, Animation, CharacterAnimation
from lib.globals import SCREEN_SIZE
from lib.custom_data.character_data import load_frame_durations
from lib.custom_data.character_loader import (load_all_characters,
                                              load_character)
from lib.game_states.state import State
from lib.game_states.state_ids import StateIDs
from lib.game_states.select_state_sfx import SelectStateSFX


PreviewData = collections.namedtuple('PreviewData',
                                     'name spritesheet frame_durations')


class CharacterSelectState(State):
    """The screen where players can select their characters before
    diving into battle.

    Class Constants:
        FONT_PATH: A String for the file path to the font used for
            rendering the text in this State.
        FONT_SIZE: An integer for the size of most text in this State.
        VS_SIZE: An integer for the size of the VS text.
        VS_COLOR: A tuple of three integers, representing the RGB color
            of the VS text.
        VS_OUTLINE_TEXT: A tuple of three integers, representing the
            RGB color of the VS text's outline.
        VS_POSITION: A tuple of two integers, for the x and y-positions
            of the VS text relative to the screen.
        NO_CHARS_POSITION: A tuple of two integers for the x and y-
            positions of the 'No Characters' text relative to the
            screen.

    Attributes:
        bg_lines: BackgroundLines that will be drawn on the screen.
        roster: A RosterDisplay that will allow the players to choose
            from all of the characters included in the game.
        all_preview_data: A tuple of PreviewData tuples, containing the
            name, spritesheet, and frame durations for each character's
            preview animation.
        p1_preview: A CharacterPreview for player 1's currently-
            selected character.
        p2_preview: A CharacterPreview for player 2's currently-
            selected character.
        select_prompt: A PlayerSelectPrompt displayed at the top of the
            screen.
        vs_text: A Graphic containing text that says "VS". It will be
            drawn between the two CharacterPreviews.
        no_chars_text: A Graphic containing a message that will be shown
            indicating that no characters could be loaded into the game.
        p1_char_index: An integer for the index of the character
            selected and confirmed by player 1. A value of None means
            that player 1 hasn't chosen a character yet.
        p2_char_index: An integer for the index of the character
            selected and confirmed by player 2.
        sfx: SelectStateSFX that will be used to play various sound
            effects within this State.
        intro: The IntroTransition that plays upon entering this State.
        outro: The OutroTransition that plays upon exiting this State.
    """
    FONT_PATH = 'fonts/fighting-spirit-TBS.ttf'
    FONT_SIZE = 16
    VS_SIZE = 28
    VS_COLOR = (255, 255, 255)
    VS_OUTLINE_COLOR = (80, 80, 80)
    VS_POSITION = (167, 80)
    NO_CHARS_COLOR = (255, 255, 255)
    NO_CHARS_POSITION = (40, 78)

    def __init__(self, state_manager, state_pass):
        """Declare and initialize instance variables.

        Args:
            state_manager: The GameStateManager that owns and runs this
                Game State.
            state_pass: The StatePass object containing all of the data
                passed between Game States.
        """
        super(CharacterSelectState, self).__init__(state_manager, state_pass)
        all_chars = load_all_characters()
        general_font = pygame.font.Font(self.FONT_PATH, self.FONT_SIZE)
        vs_font = pygame.font.Font(self.FONT_PATH, self.VS_SIZE)
        self.p1_preview = None
        self.p2_preview = None

        self.roster = RosterDisplay(all_chars)
        self.all_preview_data = self.load_all_preview_data(all_chars)
        self.p1_char_index = None
        self.p2_char_index = self.get_initial_p2_char_index()
        if self.num_of_characters() > 0:
            self.create_previews(general_font)
        self.bg_lines = BackgroundLines()
        self.select_prompt = PlayerSelectPrompt(general_font)
        self.vs_text = render_outlined_text(vs_font, 'VS', self.VS_COLOR,
                                            self.VS_OUTLINE_COLOR,
                                            self.VS_POSITION)
        self.no_chars_text = render_outlined_text(vs_font,
                                                  'No Characters Loaded',
                                                  self.NO_CHARS_COLOR,
                                                  self.VS_OUTLINE_COLOR,
                                                  self.NO_CHARS_POSITION)
        self.sfx = SelectStateSFX(self.state_pass.ui_channel)
        self.intro = IntroTransition(self,
                                     self.state_pass.announcer_channel)
        self.outro = OutroTransition(self)

        if self.returned_from_stage_select():
            self.select_previous_characters()
        else:
            self.intro.play()

    @staticmethod
    def load_all_preview_data(all_chars):
        """Return a tuple of PreviewData tuples for all characters'
        preview animations.

        Args:
            all_chars: A tuple of CharacterData objects for all of the
                characters included in the game.
        """
        all_preview_data = []

        if all_chars is not None:
            for character in all_chars:
                name = character.name
                spritesheet_path = character.actions[0].spritesheet_path
                spritesheet = pygame.image.load(spritesheet_path)
                spritesheet = spritesheet.convert_alpha()
                frame_durations = load_frame_durations(character.actions[0])

                all_preview_data.append(PreviewData(name, spritesheet,
                                                    frame_durations))

        return tuple(all_preview_data)

    def get_initial_p2_char_index(self):
        """Return an integer for the roster index of Player 2's initial
        character upon entering this State.

        If at least two characters are loaded into the game, the second
        character's index is returned.
        If not, the first character's index is returned.
        """
        if len(self.all_preview_data) > 1:
            return 1
        else:
            return 0

    def create_previews(self, name_font):
        """Initialize the CharacterPreviews to display their initial
        characters.

        Args:
            name_font: A PyGame Font used for rendering the characters'
                name text.
        """
        p1_char = self.all_preview_data[0]   # p1_char_index is initally None.
        p2_char = self.all_preview_data[self.p2_char_index]
        self.p1_preview = CharacterPreview(False, p1_char.spritesheet,
                                           p1_char.name, name_font,
                                           p1_char.frame_durations)
        self.p2_preview = CharacterPreview(True, p2_char.spritesheet,
                                           p2_char.name, name_font,
                                           p2_char.frame_durations)

    def num_of_characters(self):
        """Return an integer for the number of character loaded into
        the game.
        """
        return len(self.all_preview_data)

    def returned_from_stage_select(self):
        """Return a Boolean indicating whether the players returned to
        the CharacterSelectState after exiting the Stage Select Screen.
        """
        return (self.state_pass.character_one is not None and
                self.state_pass.character_two is not None)

    def select_previous_characters(self):
        """Select and display the Characters that were chosen the last
        time this State was run.
        """
        self.p1_char_index = self.state_pass.character_one
        self.p2_char_index = self.state_pass.character_two
        self.toggle_player_display()
        self.roster.select_character(self.p2_char_index)

        p1_char = self.all_preview_data[self.p1_char_index]
        p2_char = self.all_preview_data[self.p2_char_index]
        self.p1_preview.change_character(p1_char.spritesheet, p1_char.name,
                                         p1_char.frame_durations)
        self.p2_preview.change_character(p2_char.spritesheet, p2_char.name,
                                         p2_char.frame_durations)

    def get_player_input(self, event):
        """Respond to input from the players.

        Args:
            event: The PyGame event containing key input data.
        """
        if self.intro.is_running:
            return

        key_name = pygame.key.name(event.key)
        input_name = self.get_input_name(key_name)

        if input_name == 'start':
            if self.num_of_characters() > 0:
                self.sfx.play_confirm()
                self.confirm_character()
            else:
                self.sfx.play_no_confirm()
        elif input_name == 'cancel':
            self.sfx.play_cancel()
            self.cancel_selection()
        if (input_name in ['back', 'forward', 'up', 'down'] and
           self.num_of_characters() > 0):
            self.sfx.play_scroll()
            current_character = self.roster.get_character_index()

            if input_name == 'back':
                self.roster.select_previous()
            elif input_name == 'forward':
                self.roster.select_next()
            elif input_name == 'up':
                self.roster.scroll_up_row()
            elif input_name == 'down':
                self.roster.scroll_down_row()

            if current_character != self.roster.get_character_index():
                self.change_preview(self.roster.get_character_index())

    def get_input_name(self, key_name):
        """Get the name of the in-game input command based on the key
        that was pressed.

        Only the player who is in control will have their key bindings
        checked. For example, if player 2 is currently choosing their
        character, player 1's key bindings will not be looked at.

        Args:
            key_name: A String for the name of the key that was pressed.

        Returns:
            The String name of the in-game input command.
            (e.g. 'forward', 'start', 'light punch')
            None will be returned if key_name does not match any of the
            current player's key bindings.
        """
        if self.get_current_player() == 1:
            bindings_dict = self.state_pass.settings.player1_keys
        else:
            bindings_dict = self.state_pass.settings.player2_keys

        for input_name in bindings_dict.keys():
            if key_name == bindings_dict[input_name]:
                return input_name

        return None

    def cancel_selection(self):
        """Cancel the current player's selection and go back to the
        previous step.

        If player 1 was choosing, this State will be exited and
        transition back to the Title State.
        If player 2 was choosing, character selection will go back to
        player 1.
        """
        if self.get_current_player() == 1:
            self.clear_selected_characters()
            self.outro.play(StateIDs.TITLE, music_will_fade=True)
        else:
            self.change_preview(self.p2_char_index)
            p1_last_selection = self.p1_char_index
            self.p1_char_index = None
            self.roster.select_character(p1_last_selection)
            self.change_preview(p1_last_selection)
            self.toggle_player_display()

    def clear_selected_characters(self):
        """Clear the CharacterData stored as Player One's and Two's
        fighters within the StatePass.
        """
        self.state_pass.character_one = None
        self.state_pass.character_two = None
    def confirm_character(self):
        """Save the currently-selected character as a player's fighter
        in the next battle and move onto the appropriate operation.

        If player 1 is the one confirming, control of the game will be
        passed onto player 2 so that they can select their character.
        If player 2 is the one confirming, the State will transition
        into the Stage Select State.
        """
        if self.get_current_player() == 1:
            self.p1_char_index = self.roster.get_character_index()
            self.state_pass.character_one = self.p1_char_index
            self.roster.select_character(self.p2_char_index)
            self.toggle_player_display()
        else:
            self.p2_char_index = self.roster.get_character_index()
            self.state_pass.character_two = self.p2_char_index
            self.outro.play(StateIDs.SELECT_STAGE)

    def toggle_player_display(self):
        """Toggle certain graphics to indicate that the other player is
        now choosing.
        """
        self.select_prompt.toggle_player()
        self.roster.toggle_player_cursor()

    def change_preview(self, character_index):
        """Change the previewed character for the player currently
        selecting.

        Args:
            character_index: An integer for the index of the character.
                This index is based on the order of the character file
                paths in the character list text file.
        """
        preview_data = self.all_preview_data[character_index]

        if self.get_current_player() == 1:
            self.p1_preview.change_character(preview_data.spritesheet,
                                             preview_data.name,
                                             preview_data.frame_durations)
        else:
            self.p2_preview.change_character(preview_data.spritesheet,
                                             preview_data.name,
                                             preview_data.frame_durations)

    def get_current_player(self):
        """Return the number of the player currently making their
        selection (either 1 or 2).
        """
        if self.p1_char_index is None:
            return 1
        else:
            return 2

    def update_state(self, time):
        """Update all processes within the Game State.

        Args:
            time: A float for the time elapsed, in seconds, since the
                last update cycle.
        """
        if self.intro.is_running:
            self.intro.update(time)
        elif self.outro.is_running:
            self.outro.update(time)
        else:
            self.select_prompt.update()
            if self.num_of_characters() > 0:
                self.p1_preview.update()
                self.p2_preview.update()

        self.draw_state()

    def draw_state(self):
        """Render all of the State's graphical components onto the State
        Surface.
        """
        pygame.draw.rect(self.state_surface, (0, 0, 0),
                         Rect(0, 0, SCREEN_SIZE[0], SCREEN_SIZE[1]))

        if self.intro.is_running or self.outro.is_running:
            if self.num_of_characters() <= 0:
                center_text_pos = self.NO_CHARS_POSITION
            else:
                center_text_pos = self.VS_POSITION

            if self.intro.is_running:
                self.intro.draw(self.state_surface)
            else:
                self.outro.draw(self.state_surface)
        else:
            self.bg_lines.draw(self.state_surface)
            self.roster.draw(self.state_surface)
            self.select_prompt.draw(self.state_surface)

            if self.num_of_characters() <= 0:
                self.no_chars_text.draw(self.state_surface)
            else:
                self.vs_text.draw(self.state_surface)
                self.p1_preview.draw(self.state_surface)
                self.p2_preview.draw(self.state_surface)


class TransitionSpeeds(object):
    """Contains constants for the speeds of various objects within this
    State when they are being moved during transition animations.

    Attributes:
        LINES: An integer for the speed, in pixels per second, that the
            BackgroundLines will scroll across the screen.
        ROSTER: An integer for the speed, in pixels per second, that the
            RosterDisplay will slide at.
        PREVIEWS: An integer for the speed, in pixels per second, that
            the CharacterPreviews will slide at.
        VS: An integer for the speed, in pixels per second, of the wipe
            in and wipe out effect on the VS text.
    """
    LINES = 500
    ROSTER = 150
    VS = 120


class IntroTransition(object):
    """Manages the Character Select State's introductory animation.

    The animation is performed as follows:
        * Music begins playing.
        * The BackgroundLines scroll into the screen from left to right.
        * The RosterDisplay slides in from the bottom of the screen,
          while the CharacterPreviews slide in from the left or right
          edge of the screen.
        * As those three components slide in, the announcer declares
          that they will choose their fighters.
        * Once the three components have finished sliding in, the VS
          VS text wipes into the middle of the screen.

    Class Constants:
        MUSIC_PATH: A String for the file path to the Character Select
            Screen and Stage Select Screen music.
        VOICE_PATH: A String for the file path to the announcer voice
            clip.

    Attributes:
        state: The CharacterSelectState that will be animated.
        vs_wipe_y: An integer for the top end of the wipe in effect,
            relative to the VS text Surface.
        voice: A PyGame Sound that plays the announcer voice clip.
        voice_channel: A PyGame Channel used for playing announcer
            voice clips.
        is_running: A Boolean indicating whether the intro is currently
            running.
    """
    MUSIC_PATH = 'audio/select-theme.wav'
    VOICE_PATH = 'audio/announcer-character_select.wav'

    def __init__(self, state, voice_channel):
        """Declare and initialize instance variables.

        Args:
            state (CharacterSelectState): The State that will be
                animated.
            voice_channel: A PyGame Channel used for playing announcer
                voice clips.
        """
        self.state = state
        self.vs_wipe_y = self.state.vs_text.rect.height
        self.is_running = False
        self.voice = pygame.mixer.Sound(self.VOICE_PATH)
        self.voice_channel = voice_channel
        self.voice_has_played = False

    def play(self):
        """Begin running the intro animation."""
        self.is_running = True

        if not self.state.returned_from_stage_select():
            pygame.mixer.music.load(self.MUSIC_PATH)
            pygame.mixer.music.play(-1)

        self.state.bg_lines.move_right_end(-1 * SCREEN_SIZE[0])
        self.state.roster.place_offscreen()
        if self.state.num_of_characters() > 0:
            self.state.p1_preview.place_offscreen()
            self.state.p2_preview.place_offscreen()

    def update(self, time):
        """Update the intro animation.

        Args:
            time: A float for time elapsed, in seconds, since the last
                update cycle.
        """
        if (self.state.p1_preview is not None and
             self.state.p2_preview is not None):
            self.state.p1_preview.update()
            self.state.p2_preview.update()

        if not self.state.bg_lines.are_fully_extended():
            self.move_lines_in(time)

        elif (self.state.num_of_characters() <= 0 and
              not self.state.roster.is_onscreen()):
            self.slide_in_roster(time)
        elif self.state.num_of_characters() > 0 and not (
                self.state.p1_preview.is_onscreen() and
                self.state.p2_preview.is_onscreen() and
                self.state.roster.is_onscreen()):
            self.slide_in_roster(time)
            self.slide_in_previews(time)

        elif self.vs_wipe_y > 0:
            self.wipe_in_vs(time)
            if not self.voice_has_played:
                self.voice_channel.play(self.voice)
                self.voice_has_played = True
        else:
            self.is_running = False

    def move_lines_in(self, time):
        """Scroll the BackgroundLines into the screen from left to
        right.

        Args:
            time: A float for time elapsed, in seconds, since the last
                update cycle.
        """
        distance = TransitionSpeeds.LINES * time
        self.state.bg_lines.move_right_end(distance)

        if self.state.bg_lines.are_fully_extended():
            self.state.bg_lines.reset()

    def slide_in_roster(self, time):
        """Slide the roster into the screen from the bottom edge.

        Args:
            time: A float for time elapsed, in seconds, since the last
                update cycle.
        """
        distance = -1 * TransitionSpeeds.ROSTER * time
        self.state.roster.move(dy=distance)

        if self.state.roster.is_onscreen():
            self.state.roster.correct_position()

    def slide_in_previews(self, time):
        """Slide both CharacterPreviews into the screen from the left
        and right edges.

        Args:
            time: A float for time elapsed, in seconds, since the last
                update cycle.
        """
        p1_distance = self.state.p1_preview.slide_speed() * time
        p2_distance = self.state.p2_preview.slide_speed() * time

        if not self.state.p1_preview.is_onscreen():
            self.state.p1_preview.move(dx=(p1_distance))
            if self.state.p1_preview.is_onscreen():
                self.state.p1_preview.correct_position()

        if not self.state.p2_preview.is_onscreen():
            self.state.p2_preview.move(dx=(-1 * p2_distance))
            if self.state.p2_preview.is_onscreen():
                self.state.p2_preview.correct_position()

    def wipe_in_vs(self, time):
        """Move the upper bound of the VS text's draw region in order
        to create a 'wipe-in' effect.

        Args:
            time: A float for time elapsed, in seconds, since the last
                update cycle.
        """
        self.vs_wipe_y -= TransitionSpeeds.VS * time
        if self.vs_wipe_y <= 0:
            self.vs_wipe_y = 0

    def draw(self, parent_surf):
        """Draw all of the Character Select Screen graphics onto a
        Surface.

        Args:
            parent_surf: The PyGame Surface upon which the various
                graphics will be drawn.
        """
        pygame.draw.rect(parent_surf, (0, 0, 0),
                         Rect(0, 0, SCREEN_SIZE[0], SCREEN_SIZE[1]))
        self.state.bg_lines.draw(parent_surf)
        self.state.roster.draw(parent_surf)
        if self.state.num_of_characters() > 0:
            self.state.p1_preview.draw(parent_surf)
            self.state.p2_preview.draw(parent_surf)
        self.draw_vs_text(parent_surf)

    def draw_vs_text(self, parent_surf):
        """Draw a portion of the VS text onto a Surface.

        The portion of the text drawn is controlled by the wipe-in
        effect.

        Args:
            parent_surf: The PyGame Surface upon which the VS text will
                be drawn.
        """
        if self.state.num_of_characters() <= 0:
            draw_region = Rect(0, 0, self.state.no_chars_text.rect.width,
                self.state.no_chars_text.rect.height - self.vs_wipe_y)
            self.state.no_chars_text.draw(parent_surf, region=draw_region)
        else:
            draw_region = Rect(0, 0, self.state.vs_text.rect.width,
                self.state.vs_text.rect.height - self.vs_wipe_y)
            self.state.vs_text.draw(parent_surf, region=draw_region)


class OutroTransition(object):
    """Manages the CharacterSelectState's outgoing animation.

    The animation is performed as follows:
        * The VS text disappears via a wipe-out effect.
        * The RosterDisplay and CharacterPreviews slide offscreen in
          their respective directions.
        * The BackgroundLines scroll out of the screen from left to
          right, leaving only a black screen.

    Class Constants:
        MUSIC_FADEOUT_TIME: An integer for the time taken, in
            milliseconds, to fade out the Select Screen music.

    Attributes:
        state: The CharacterSelectState that will be animated.
        vs_wipe_y: An integer for the top end of the wipe out effect,
            relative to the VS text Surface.
        is_running: A Boolean indicating whether the outro is currently
            running.
        next_state: An enum value representing the next Game State to
            run after this animation is completed. See the state_ids
            module for possible values.
    """
    MUSIC_FADEOUT_TIME = 2000

    def __init__(self, state):
        """Declare and initialize instance variables.

        Args:
            state (CharacterSelectState): The State that this object
                will animate.
        """
        self.state = state
        self.vs_wipe_y = self.state.vs_text.rect.height
        self.next_state = StateIDs.SELECT_CHARACTER
        self.is_running = False

    def play(self, next_state, music_will_fade=False):
        """Start playing the outro animation.

        Args:
            next_state: An integer for the index of the Game State to
                run once the outro finishes. See the StateIDs enum for
                possible values.
            music_will_fade: A Boolean indicating whether the Select
                Screen music should be faded out.
        """
        self.is_running = True
        self.next_state = next_state
        if music_will_fade:
            pygame.mixer.music.fadeout(self.MUSIC_FADEOUT_TIME)

    def update(self, time):
        """Update the outro animation.

        Args:
            time: A float for the amount of time elapsed, in seconds,
                since the last update.
        """
        if self.state.num_of_characters() > 0:
            self.state.p1_preview.update()
            self.state.p2_preview.update()

        # Start of animation sequence.
        if self.vs_wipe_y > 0:
            self.wipe_out_vs(time)

        elif (self.state.num_of_characters() <= 0 and
              not self.state.roster.is_offscreen()):
            self.slide_out_roster(time)
        elif (self.state.num_of_characters() > 0 and
              not (self.state.p1_preview.is_offscreen() and
                   self.state.p2_preview.is_offscreen() and
                   self.state.roster.is_offscreen())):
            self.slide_out_roster(time)
            self.slide_out_previews(time)

        elif not self.state.bg_lines.are_not_visible():
            self.move_lines_out(time)

        else:
            self.state.change_state(self.next_state)

    def move_lines_out(self, time):
        """Scroll the lines out of the screen, from left to right.

        Args:
            time: A float for the amount of time elapsed, in seconds,
                since the last update.
        """
        self.state.bg_lines.move_left_end(TransitionSpeeds.LINES * time)

    def slide_out_roster(self, time):
        """Slide the roster in the direction of the bottom edge of the
        screen.

        Args:
            time: A float for the amount of time elapsed, in seconds,
                since the last update.
        """
        self.state.roster.move(dy=(TransitionSpeeds.ROSTER * time))

    def slide_out_previews(self, time):
        """Slide the CharacterPreviews out toward either side of the
        screen.

        Args:
            time: A float for the amount of time elapsed, in seconds,
                since the last update.
        """
        p1_distance = self.state.p1_preview.slide_speed() * time
        p2_distance = self.state.p2_preview.slide_speed() * time
        self.state.p1_preview.move(dx=(-1 * p1_distance))
        self.state.p2_preview.move(dx=p2_distance)

    def wipe_out_vs(self, time):
        """Move the lower bound of the VS text's draw region upward in
        order to produce a 'wipe-out' effect.

        Args:
            time: A float for the amount of time elapsed, in seconds,
                since the last update.
        """
        self.vs_wipe_y -= TransitionSpeeds.VS * time
        if self.vs_wipe_y < 0:
            self.vs_wipe_y = 0

    def draw(self, parent_surf):
        """Draw all of the Character Select Screen graphics onto a
        Surface.

        Args:
            parent_surf: The PyGame Surface upon which the various
                graphics will be drawn.
        """
        self.state.bg_lines.draw(parent_surf)
        self.state.roster.draw(parent_surf)
        if self.state.num_of_characters() > 0:
            self.state.p1_preview.draw(parent_surf)
            self.state.p2_preview.draw(parent_surf)
        self.draw_vs_text(parent_surf)

    def draw_vs_text(self, parent_surf):
        """Draw a portion of the VS text onto a Surface.

        The portion drawn is controlled by the wipe-out effect.

        Args:
            parent_surf: The Surface ipon which the VS text will be
                drawn.
        """
        if self.state.num_of_characters() <= 0:
            draw_region = Rect(0, 0, self.state.no_chars_text.rect.width,
                               self.vs_wipe_y)
            self.state.no_chars_text.draw(parent_surf, region=draw_region)
        else:
            draw_region = Rect(0, 0, self.state.vs_text.rect.width,
                               self.vs_wipe_y)
            self.state.vs_text.draw(parent_surf, region=draw_region)


class PlayerSelectPrompt(object):
    """A prompt that notifies either Player 1 or Player 2 that they are
    currently choosing their character.

    Class Constants:
        Y: An integer for the y-position of the prompt relative to the
            screen.
        FLASH_RATE: An integer for the amount of time elapsed, in update
            cycles, between toggling the visibility of the text.
        P1_TEXT: A String for the text that will be displayed as player
            1's prompt message.
        P2_TEXT: A String for the text that will be displayed as player
            2's prompt message.
        P1_COLOR: A tuple of three integers, representing the RGB value
            for player 1's text.
        P2_COLOR: A tuple of three integers, representing the RGB value
            for player 2's text.

    Attributes:
        p1_surf: A Surface containing player 1's prompt message.
        p2_surf: A Surface containing player 1's prompt message.
        current_surf: A Surface containing either player 1 or player 2's
            message as the prompt currently displayed on-screen.
        flash_timer: An integer timer that counts the duration between
            text flash cycles.
        text_is_visible: A Boolean indicating whether the current prompt
            is being shown.
    """
    Y = 13
    FLASH_RATE = 30
    P1_TEXT = 'P1 Select'
    P2_TEXT = 'P2 Select'
    P1_COLOR = (255, 0, 0)
    P2_COLOR = (0, 255, 255)

    def __init__(self, font):
        """Declare and initialize instance variables.

        Args:
            font: A PyGame Font that will be used in rendering the
                prompt text.
        """
        self.p1_surf = font.render(self.P1_TEXT, True, self.P1_COLOR)
        self.p2_surf = font.render(self.P2_TEXT, True, self.P2_COLOR)
        self.current_surf = self.p1_surf
        self.flash_timer = 0
        self.text_is_visible = True
        self.x = 0
        self.center_horizontally()

    def center_horizontally(self):
        """Position the text so that it is centered horizontally on the
        screen.
        """
        self.x = (SCREEN_SIZE[0] - self.current_surf.get_width()) / 2

    def toggle_player(self):
        """Display the other player's prompt."""
        if self.current_surf == self.p1_surf:
            self.current_surf = self.p2_surf
        else:
            self.current_surf = self.p1_surf
        self.center_horizontally()

    def update(self):
        """Update the text flashing."""
        self.flash_timer += 1
        if self.flash_timer >= self.FLASH_RATE:
            self.flash_timer = 0
            self.text_is_visible = not self.text_is_visible

    def draw(self, parent_surf):
        """Draw the current player's prompt onto a Surface.

        Args:
            parent_surf: The Surface upon which the prompt will be
                drawn.
        """
        if self.text_is_visible:
            parent_surf.blit(self.current_surf, (self.x, self.Y))

    def reset(self):
        """Reset the flash and display player 1's prompt."""
        self.text_is_visible = True
        self.flash_timer = 0
        self.current_surf = self.p1_surf
        self.center_horizontally()


class BackgroundLines(object):
    """A series of action lines that will be drawn in the background.

    The starting and end points of the lines can be moved to create a
    type of scrolling movement effect.

    Class Constants:
        LINE_COLOR: A tuple three integers, representing the RGB color
            used in drawing all of the lines.
        LINE_Y_COOORS: A tuple of integers, each of which represent one
            of the lines' y-position relative to the screen.
        LINE_WIDTHS: A tuple of integers, each of which represent the
            width of one of the lines, in pixels.
            Note that this is in the same order as LINE_Y_COORS. For
            example, if the first value in LINE_Y_COORS is 50 and the
            first value in LINE_WIDTHS is 5, a line with a width of 5
            pixels will be drawn at a y-position of 50.

    Attributes:
        left_end: An integer for the x-position of the lines' starting
            point from the left edge of the screen.
        right_end: An integer for the x-position of the lines' end point
            closer to the right side of the screen.
    """
    LINE_COLOR = (0, 19, 127)
    LINE_Y_COORDS = (11, 26, 59, 95, 151)
    LINE_WIDTHS = (3, 9, 7, 5, 17)

    def __init__(self):
        """Declare and initialize instance variables."""
        self.left_end = 0
        self.right_end = SCREEN_SIZE[0]

    def draw(self, parent_surf):
        """Draw all of the lines onto a Surface.

        Args:
            parent_surf: The Surface upon which the lines will be drawn.
        """
        if self.right_end > self.left_end:
            for line_index in xrange(0, len(self.LINE_Y_COORDS)):
                y = self.LINE_Y_COORDS[line_index]
                width = self.LINE_WIDTHS[line_index]
                pygame.draw.line(parent_surf, self.LINE_COLOR,
                                 (self.left_end, y), (self.right_end, y),
                                 width)

    def move_left_end(self, distance):
        """Move the starting point of all lines from the left side of
        the screen.

        Args:
            distance: An integer for the distance moved, in pixels. A
            positive value will shift the point to the right, while a
            negative value will shift it to the left.
        """
        self.left_end += distance

    def move_right_end(self, distance):
        """Move the end point of all lines from the right side of the
        screen.

        Args:
            distance: An integer for the distance moved, in pixels. A
            positive value will shift the point to the right, while a
            negative value will shift it to the left.
        """
        self.right_end += distance

    def are_fully_extended(self):
        """Return a Boolean indicating whether the lines cover the full
        width of the screen.
        """
        if self.left_end <= 0 and self.right_end >= SCREEN_SIZE[0]:
            return True
        else:
            return False

    def are_not_visible(self):
        """Return a Boolean indicating whether the lines cannot be seen
        on the screen at all.
        """
        if self.right_end <= self.left_end or self.right_end <= 0:
            return True
        else:
            return False

    def reset(self):
        """Set the lines back to their original state i.e. extending
        from the left edge of the screen all the way to the right edge.
        """
        self.left_end = 0
        self.right_end = SCREEN_SIZE[0]


class RosterDisplay():
    """An on-screen list of the entire roster of playable characters
    available in this copy of the game.

    Players will use this list to select characters for a battle.
    Since only one row characters can be displayed at a time, only one
    player may select from the list at a time; the color of the cursor
    can be toggled to show which player is currently choosing.

    Class Constants:
        MUGSHOT_SIZE: An integer for the length and width of a
            character's mugshot image (which should be square-shaped).
        SLOTS_PER_ROW: An integer for the number of character slots that
            can be shown on the displayed row.
        FRAME_THICKNESS: An integer for the thickness, in pixels, of
            each character slot frame.
        FRAME_COLOR: A tuple of integers for the RGB color of the
            character slot frames.
        BACKGROUND_COLOR: A tuple of integers for the RGB color of each
            character slot's background.
        ARROW_DISTANCE: An integer for the horizontal distance, in
            pixels, between the edges of the roster and each of the
            scroll arrows.

    Attributes:
        x: An integer for the x-position of the roster relative to the
            screen.
        y: An integer for the y-position of the roster relative to the
            screen.
        mugshots: A tuple of Surfaces, each containing a character's
            mugshot.
        current_row: An integer for the index of the currently-selected
            'row' of characters. Each row contains a number of
            characters specified by the SLOTS_PER_ROW constant.
        current_slot: An integer for the index of the currently-selected
            slot within the current row.
            For example, if current_row is 1 and current_slot is 2, the
            seventh character overall is currently being selected. Use
            get_character_index() if you wish to obtain this data.
        cursor: A RosterCursor used for marking the currently-selected
            mugshot.
        rendered_row: A Surface containing the currently-selected row
            of character slots.
        scroll_up_arrow: A RosterArrow indicating that the players can
            scroll up a row.
        scroll_down_arrow: A RosterArrow indicating that the players can
            scroll down a row.
    """
    MUGSHOT_SIZE = 50
    SLOTS_PER_ROW = 5
    FRAME_THICKNESS = 2
    FRAME_COLOR = (102, 102, 102)
    BACKGROUND_COLOR = (255, 255, 255)
    ARROW_DISTANCE = 11

    def __init__(self, all_chars=None):
        """Declare and initialize instance variables.

        Args:
            all_chars: A tuple of CharacterData objects for all of the
                characters included in the game.
                If None is passed, a blank roster will be created.
        """
        if all_chars is None:
            self.mugshots = []
        else:
            self.mugshots = self.load_all_mugshots(all_chars)
        self.rendered_row = self.render_row(0)
        self.x = self.get_screen_centered_x()
        self.y = SCREEN_SIZE[1] - self.rendered_row.get_height()
        self.current_row = 0
        self.current_slot = 0
        self.cursor = RosterCursor((self.x, self.y))
        self.scroll_up_arrow = RosterArrow(ArrowType.UP, self.x, self.y,
                                           self.rendered_row.get_width(),
                                           self.rendered_row.get_height())
        self.scroll_down_arrow = RosterArrow(ArrowType.DOWN, self.x, self.y,
                                             self.rendered_row.get_width(),
                                             self.rendered_row.get_height())

    @staticmethod
    def load_all_mugshots(all_chars):
        """Return a tuple of Surfaces, containing the mugshot images for
        every character.

        Args:
            all_chars: A tuple of CharacterData objects for all of the
                characters included in the game.
        """
        mugshot_paths = []

        for character in all_chars:
            mugshot_paths.append(character.mugshot_path)

        return load_tuple_of_images(mugshot_paths)

    def render_row(self, row_index):
        """Render a row of mugshots in order from the mugshot list.

        Args:
            row_index: An integer for the index of the row that will be
                rendered. For example, given that SLOTS_PER_ROW is 5,
                passing 1 would render mugshots of index 5 through 9.
        """
        row_surf = Surface((self.slot_size() * self.SLOTS_PER_ROW,
                            self.slot_size()))
        slot_x = 0

        first_slot = row_index * self.SLOTS_PER_ROW
        last_slot = first_slot + self.SLOTS_PER_ROW

        for slot_index in xrange(first_slot, last_slot + 1):
            if slot_index <= len(self.mugshots) - 1:
                new_slot = self.render_slot(slot_index)
            else:
                new_slot = self.render_slot(-1)
            row_surf.blit(new_slot, (slot_x, 0))

            slot_x += self.slot_size()

        return row_surf

    def render_slot(self, slot_index):
        """Render one of the character's mugshots and place it within a
        frame.

        Alternatively, a blank slot with just a frame and background can
        be rendered.

        Args:
            slot_index: The index of the character's mugshot within
                mugshot_paths. Passing a value less than 0 will create
                a blank slot.

        Returns:
            A Surface containing a framed mugshot, if slot_index is 0 or
            more. Otherwise, a Surface with a blank slot is returned.
        """
        slot_surf = Surface((self.slot_size(), self.slot_size()))

        # Background.
        pygame.draw.rect(slot_surf, self.BACKGROUND_COLOR,
                         Rect(self.FRAME_THICKNESS, self.FRAME_THICKNESS,
                              self.MUGSHOT_SIZE, self.MUGSHOT_SIZE))

        # Mugshot.
        if slot_index >= 0:
            mugshot = self.mugshots[slot_index]
            slot_surf.blit(mugshot, (self.FRAME_THICKNESS, self.FRAME_THICKNESS))

        # Frame.
        pygame.draw.rect(slot_surf, self.FRAME_COLOR,
                         Rect(0, 0,
                              self.slot_size() - 1, self.slot_size() - 1),
                         self.FRAME_THICKNESS)
        return slot_surf

    def slot_size(self):
        """Return an integer for the length and width, in pixels, of
        a character slot (mugshot + frame).
        """
        return self.MUGSHOT_SIZE + (self.FRAME_THICKNESS * 2)

    def get_screen_centered_x(self):
        """Return an integer for the x-position that will center the
        roster on the screen.
        """
        return (SCREEN_SIZE[0] - self.rendered_row.get_width()) / 2

    def num_of_rows(self):
        """Return an integer for the number of rows of characters that
        can be selected.
        """
        return int(round_up(len(self.mugshots) / float(self.SLOTS_PER_ROW)))

    def draw(self, parent_surf):
        """Draw the entire roster onto another Surface.

        Args:
            parent_surf: The Surface upon which the roster will be
                drawn.
        """
        parent_surf.blit(self.rendered_row, (self.x, self.y))
        self.cursor.draw(parent_surf)
        if self.current_row > 0:
            self.scroll_up_arrow.draw(parent_surf)
        if self.current_row < self.num_of_rows() - 1:
            self.scroll_down_arrow.draw(parent_surf)

    def get_character_index(self):
        """Return an integer for the index of character currently
        selected.
        """
        return (self.current_row * self.SLOTS_PER_ROW) + self.current_slot

    def select_first(self):
        """Select the very first slot in the roster."""
        self.cursor.move(0 - self.slot_size() * self.current_slot, 0)
        self.current_row = 0
        self.current_slot = 0
        self.rendered_row = self.render_row(0)

    def select_character(self, character_index):
        """Move selection to a specific character.

        Args:
            character_index: An integer for the index of the character.
                This index is based on the order of the character file
                paths in the character list text file.
        """
        row = int(character_index / self.SLOTS_PER_ROW)
        new_slot = character_index - (self.SLOTS_PER_ROW * row)
        slot_diff = new_slot - self.current_slot

        self.current_row = row
        self.current_slot = new_slot
        self.rendered_row = self.render_row(row)
        self.cursor.move(self.slot_size() * slot_diff, 0)

    def select_next(self):
        """Select the next character slot, if there is one."""
        if self.get_character_index() < len(self.mugshots) - 1:
            if self.current_slot >= self.SLOTS_PER_ROW - 1:
                # Move on to the next row.
                self.cursor.move(0 - self.slot_size() * self.current_slot, 0)
                self.current_slot = 0
                self.current_row += 1
                self.rendered_row = self.render_row(self.current_row)
            else:
                self.current_slot += 1
                self.cursor.move(self.slot_size(), 0)

    def select_previous(self):
        """Select the previous character slot, if there is one."""
        if self.get_character_index() > 0:
            if self.current_slot <= 0:
                # Go back to the previous row.
                self.cursor.move(self.slot_size() *
                                 (self.SLOTS_PER_ROW - 1 - self.current_slot),
                                 0)
                self.current_slot = self.SLOTS_PER_ROW - 1
                self.current_row -= 1
                self.rendered_row = self.render_row(self.current_row)
            else:
                self.current_slot -= 1
                self.cursor.move(0 - self.slot_size(), 0)

    def correct_last_row_selection(self):
        """If the roster scrolls to the last row, and the last row has
        less slots than the previous one, make sure  the selection only
        goes as far as the very last slot.
        """
        if len(self.mugshots) % self.SLOTS_PER_ROW != 0:
            last_slot = (len(self.mugshots) - 1) % self.SLOTS_PER_ROW
            self.cursor.move(0 - (self.slot_size() *
                                  (self.current_slot - last_slot)), 0)
            self.current_slot = last_slot

    def scroll_down_row(self):
        """Scroll down to the next row of characters.

        If there are no more rows after the current one, selection will
        wrap around to the first row.
        """
        if self.current_row < self.num_of_rows() - 1:
            self.current_row += 1

            if self.get_character_index() > len(self.mugshots) - 1:
                self.correct_last_row_selection()
        else:
            self.current_row = 0

        self.rendered_row = self.render_row(self.current_row)

    def scroll_up_row(self):
        """Scroll up to the previous row of characters.

        If the current row is the first row, selection will wrap around
        to the last row.
        """
        if self.current_row > 0:
            self.current_row -= 1
        else:
            self.current_row = self.num_of_rows() - 1
            self.correct_last_row_selection()
        self.rendered_row = self.render_row(self.current_row)

    def move(self, dx=0, dy=0):
        """Move the roster across the screen space.

        Args:
            dx: An integer for the horizontal distance moved, in pixels.
            A positive value will result in a shift to the right, while
            a negative value will cause a shift to the left.
        """
        self.x += dx
        self.y += dy
        self.cursor.move(dx, dy)
        self.scroll_up_arrow.move(dx, dy)
        self.scroll_down_arrow.move(dx, dy)

    def place_offscreen(self):
        """Position the roster so that it is just off the bottom edge of
        the screen.
        """
        self.move(0, self.slot_size())

    def correct_position(self):
        """Position the roster so that it is fully visible on the bottom
        edge of the screen.
        """
        self.move(dy=(SCREEN_SIZE[1] - self.slot_size() - self.y))

    def is_onscreen(self):
        """Return a Boolean indicating whether all of the roster can be
        seen on-screen.
        """
        if (self.y >= 0 and
           self.y + self.rendered_row.get_height() <= SCREEN_SIZE[1]):
            return True
        else:
            return False

    def is_offscreen(self):
        """Return a Boolean indicating whether none of the roster can be
        seen at all.
        """
        if (self.y + self.rendered_row.get_height() <= 0 or
           self.y >= SCREEN_SIZE[1]):
            return True
        else:
            return False

    def toggle_player_cursor(self):
        """Toggle the cursor's animation to show that the other player
        is now choosing.
        """
        self.cursor.toggle_player()


class RosterCursor(Animation):
    """An animated cursor that is used to mark the currently-selected
    character within the roster.

    The cursor can toggle between two different animations with
    identical dimensions; use this to signify which player is currently
    choosing.

    Class Constants:
        P1_SPRITESHEET: A String for the file path to player 1's cursor
            animation.
        P2_SPRITESHEET: A String for the file path to player 2's cursor
            animation.
        FRAME_AMOUNT: An integer for the amount of frames in each
            Animation.
        FRAME_DURATION: An integer for the duration, in update cycles,
            of each animation frame.

    Attributes:
        p1_image: A Surface containing player 1's spritesheet image.
        p2_image: A Surface containing player 2's spritesheet image.
        current_player: An integer representing the player currently
            choosing their character. This value can be either 1 or 2,
            for Player 1 and 2 respectively.
    """
    P1_SPRITESHEET = 'images/p1_character_cursor.png'
    P2_SPRITESHEET = 'images/p2_character_cursor.png'
    FRAME_AMOUNT = 2
    FRAME_DURATION = 8

    def __init__(self, position):
        """Declare and initialize instance variables.

        Args:
            position: A tuple of two integers which represent the x
                and y-positions of the cursor relative to ths screen.
        """
        self.p1_image = pygame.image.load(self.P1_SPRITESHEET)
        self.p1_image = convert_to_colorkey_alpha(self.p1_image)
        self.p2_image = pygame.image.load(self.P2_SPRITESHEET)
        self.p2_image = convert_to_colorkey_alpha(self.p2_image)
        super(RosterCursor, self).__init__(self.p1_image, position,
                                           self.FRAME_AMOUNT,
                                           self.FRAME_DURATION)
        self.current_player = 1

    def toggle_player(self):
        """Switch to the other player's cursor animation."""
        if self.current_player == 1:
            self.current_player = 2
            self.image = self.p2_image
        else:
            self.current_player = 1
            self.image = self.p1_image


class RosterArrow(Animation):
    """An animated arrow that notifies the players of a direction in
    which the character roster can be scrolled.

    Class Constants:
        SPRITESHEET: A String for the file path to the animation
            spritesheet.
        FRAME_AMOUNT: An integer for the number of frames in the
            animation.
        FRAME_DURATION: An integer for the duration, in update cycles,
            of each animation frame.
        ROSTER_DISTANCE: An integer for the distance, in pixels, of this
            arrow from the edge of the roster.
    """
    SPRITESHEET = 'images/roster_up_arrow.png'
    FRAME_AMOUNT = 2
    FRAME_DURATION = 10
    ROSTER_DISTANCE = 18

    def __init__(self, arrow_type, roster_x, roster_y, roster_width,
                 roster_height):
        """Declare and initialize instance variables.

        Args:
            arrow_type: An integer value from the ArrowType enum. This
                is used to specify the direction the arrow points.
            roster_x: An integer for the x-position of the roster
                relative to the screen.
            roster_y: An integer for the y-position of the roster
                relative to the screen.
            roster_width: An integer for the width of the roster, in
                pixels.
            roster_height: An integer for the height of the roster, in
                pixels.
        """
        spritesheet = image.load(self.SPRITESHEET)
        spritesheet = convert_to_colorkey_alpha(spritesheet)
        super(RosterArrow, self).__init__(spritesheet, (0, 0),
                                          self.FRAME_AMOUNT,
                                          self.FRAME_DURATION)
        self.correct_position(arrow_type, roster_x, roster_y,
                              roster_width, roster_height)
        if arrow_type == ArrowType.DOWN:
            self.flip(is_vertical=True)

    def correct_position(self, arrow_type, roster_x, roster_y,
                         roster_width, roster_height):
        """Move the arrow into the correct position beside the roster.

        If the arrow points up, it will be on the left edge; it it
        points down, it will be on the right edge.

        Args:
            arrow_type: An integer value from the ArrowType enum. This
                is used to specify the direction the arrow points.
            roster_x: An integer for the x-position of the roster
                relative to the screen.
            roster_y: An integer for the y-position of the roster
                relative to the screen.
            roster_width: An integer for the width of the roster, in
                pixels.
            roster_height: An integer for the height of the roster, in
                pixels.
        """
        y = roster_y + ((roster_height - self.image.get_height()) / 2)

        if arrow_type == ArrowType.UP:
            x = roster_x - self.frame_width - self.ROSTER_DISTANCE
            self.move(x, y)
        if arrow_type == ArrowType.DOWN:
            x = roster_x + roster_width + self.ROSTER_DISTANCE
            self.move(x, y)


class ArrowType(object):
    """An enumeration for the types of roster scroll arrows.

    Attributes:
        UP: An integer value representing an arrow pointing up.
        DOWN: An integer value representing an arrow pointing down.
    """
    UP = 0
    DOWN = 1


class CharacterPreview(object):
    """A looped character animation with an accompanying shadow and
    name.

    Class Constants:
        GROUND_Y: An integer for the y-position of the ground upon which
            the character will be standing, relative to the screen.
        NAME_COLOR: A tuple containing the RGB values for the name
            text's color.
        NAME_OUTLINE_COLOR: A tuple containing the RGB values for the
            color of the name text's outline.
        NAME_OFFSET: An integer for the vertical shift up, in pixels,
            of the name text from the bottom of the character sprite.
        SHADOW_HEIGHT: An integer for the height of the shadow, in
            pixels.
        SHADOW_COLOR: A tuple containing the RGB values for the color
            of the shadow.
        OFFSET_FROM_SHADOW: An integer for the distance, in pixels,
            from the bottom edge of the character sprite to the vertical
            center of the shadow.
        SLIDE_DURATION: A float for the the time taken, in seconds,
            to move this preview into position during transition
            animations.

    Attributes:
        x: An integer for the x-coordinate of the sprite relative to the
            screen.
        y: An integer for the y-coordinate of the sprite relative to the
            screen.
        is_facing_left: A Boolean indicating whether the character is
            facing to the left instead of to the right.
        animation: A CharacterAnimation object that updates and displays
            the character's animation.
        name: A Graphic with the character's name rendered onto it.
        shadow: A Graphic with the character's shadow drawn onto it.
    """
    GROUND_Y = 157
    NAME_COLOR = (255, 255, 255)
    NAME_OUTLINE_COLOR = (80, 80, 80)
    NAME_OFFSET = 6
    SHADOW_HEIGHT = 14
    SHADOW_COLOR = (0, 5, 90)
    OFFSET_FROM_SHADOW = 4
    SLIDE_DURATION = 0.4

    def __init__(self, is_facing_left, spritesheet, name, name_font,
                 frame_durations):
        """Declare and initialize instance variables.

        Args:
            is_facing_left: A Boolean indicating whether the character
                is facing to the left, rather than to the right (which
                is the default direction for characters in this game).
            spritesheet: A Surface containing the character
                animation's spritesheet image.
            name: A String for the character's name.
            name_font: The PyGame font used for rendering the
                character's name.
            frame_durations: A tuple of integers containing the
                duration, in update cycles, of each animation frame in
                order. For example, passing (10, 8, 5) means that the
                first animation frame is shown for 10 update cycles,
                the second frame for 8 update cycles, and so on.
        """
        self.is_facing_left = is_facing_left
        self.animation = CharacterAnimation(is_facing_left,
                                            spritesheet, frame_durations)
        self.x = 0
        self.y = self.calculate_y_position()
        if is_facing_left:
            self.correct_position()
        self.name_font = name_font
        self.name = self.render_name(name_font, name)
        self.shadow = self.render_shadow()

    def change_character(self, spritesheet, name, frame_durations):
        """Display a different character animation.

        Args:
            spritesheet_path: A Surface containing the character
                animation's spritesheet image.
            name: A String for the character's name.
            frame_durations: A tuple of integers containing the
                duration, in update cycles, of each animation frame in
                order. For example, passing (10, 8, 5) means that the
                first animation frame is shown for 10 update cycles,
                the second frame for 8 update cycles, and so on.
        """
        self.animation.change_animation(spritesheet, frame_durations)
        self.x = 0
        self.y = self.calculate_y_position()
        if self.is_facing_left:
            self.correct_position()
        self.name = self.render_name(self.name_font, name)
        self.shadow = self.render_shadow()

    def calculate_y_position(self):
        """Determine the vertical positioning of the character so that
        the bottom edge of the sprite (usually their feet) is touching
        the ground.

        Args:
            ground_y: An integer for the y-position of the ground
                relative to the screen.

        Returns:
            An integer for the character's y-position.
        """
        character_height = self.animation.get_height()
        y = self.GROUND_Y - character_height
        return y

    def correct_position(self):
        """Position the animation horizontally so that it is on the left
        edge of the screen if the character faces right, or on the right
        edge if the character faces left.
        """
        if self.is_facing_left:
            self.x = SCREEN_SIZE[0] - self.animation.get_width()
        else:
            self.x = 0

    def render_shadow(self):
        """Render a shadow to fit the character.

        Returns:
            A Graphic with a shadow wide enough to fit the character
            drawn onto it.
        """
        frame_width = self.animation.get_width()
        shadow_surf = Surface((frame_width, self.SHADOW_HEIGHT + 1),
                              pygame.locals.SRCALPHA)
        draw_region = Rect(0, 0, frame_width, self.SHADOW_HEIGHT)

        pygame.draw.ellipse(shadow_surf, self.SHADOW_COLOR, draw_region)

        char_bottom = self.y + self.animation.get_height()
        y = char_bottom - self.SHADOW_HEIGHT + self.OFFSET_FROM_SHADOW
        return Graphic(shadow_surf, (self.x, y))

    def update(self):
        """Update the character animation."""
        self.animation.update()

    def draw(self, parent_surf):
        """Draw the CharacterPreview onto a Surface.

        parent_surf: The Surface upon which the preview will be drawn.
        """
        self.shadow.draw(parent_surf)
        self.animation.draw(parent_surf, self.x, self.y)
        self.name.draw(parent_surf)

    def render_name(self, name_font, name):
        """Return a Graphic containing the specified name.

        Args:
            name_font: The PyGame font used for rendering the
                character's name.
            name: A String containing the character's name.
        """
        name_graphic = render_outlined_text(name_font, name, self.NAME_COLOR,
                                            self.NAME_OUTLINE_COLOR, (0, 0))

        if name_graphic.rect.width < self.animation.get_width():
            x = self.get_centered_x(name_graphic.rect.width)
        elif self.is_facing_left:
            x = self.x + self.animation.get_width() - name_graphic.rect.width
        else:
            x = self.x
        y = self.y + self.animation.get_height() - self.NAME_OFFSET
        name_graphic.move(x, y)

        return name_graphic

    def get_centered_x(self, width):
        """Calculate an x-value that would allow a Surface of a given
        width to be centered relative to the character sprite.

        Note that this only works with Surfaces that have a smaller
        width than the character.

        Args:
            width: An integer for the width of a Surface.
        """
        surface_difference = self.animation.get_width() - width
        return self.x + int(surface_difference / 2)

    def slide_speed(self):
        """Return a float for the speed at which this preview will move
        during transition animations.
        """
        return (float(self.animation.get_width()) / self.SLIDE_DURATION)

    def move(self, dx=0, dy=0):
        """Move the animation around the screen space.

        Args:
            dx: An integer for the horizontal shift, in pixels.
                A positive value causes a shift to the right, while a
                negative value causes a shift to the left.
            dx: An integer for the vertical shift, in pixels.
                A positive value shifts the animation down, while a
                negative value shifts the animation up.
        """
        self.x += dx
        self.y += dy
        self.name.move(dx, dy)
        self.shadow.move(dx, dy)

    def place_offscreen(self):
        """Set the position of the animation so that it is just off the
        left edge of the screen if the character faces right, or just
        off the right edge of the screen if the character faces left.
        """
        if self.is_facing_left:
            self.move(self.animation.get_width())
        else:
            self.move(0 - self.animation.get_width())

    def is_onscreen(self):
        """Return a Boolean indicating whether all of the animation is
        visible on-screen.
        """
        if (self.x >= 0 and
           self.x + self.animation.get_width() <= SCREEN_SIZE[0]):
            return True
        else:
            return False

    def is_offscreen(self):
        """Return a Boolean indicating whether none of the animation is
        visible on-screen.
        """
        if (self.x + self.animation.get_width() <= 0 or
           self.x >= SCREEN_SIZE[0]):
            return True
        else:
            return False
