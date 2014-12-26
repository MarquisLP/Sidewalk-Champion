import sys
from __builtin__ import range
import pygame
from pygame.locals import *
from pygame.mixer import Sound
from pygame.font import Font
from pygame.color import Color
from lib.globals import SCREEN_SIZE
from lib.globals import FRAME_RATE
from lib.graphics import Graphic
from lib.graphics import Animation
from lib.game_states.state import *
from lib.game_states.state_ids import StateIDs


class TitleState(State):
    """The Game State that handles the Title Screen.

    This State is the first to run every time the game is launched.
    Additionally, every time this State is shown, a short introduction
    will be played that reveals the game's title.

    From here, the players can:
        * Setup a new battle.
        * Go to Training Mode.
        * Open the Settings Screen.
        * Exit the game window.

    Class Constants:
        BG_PATH: A String for the file path to the background image's
            sprite sheet.
        BG_FRAMES: An integer for the amount of animation frames in the
            background image's sprite sheet.
        BG_DURATION: An integer for the duration of each frame in the
            background image's animation, in update cycles.
        LOGO_PATH: A String for the file path to the game logo's sprite
            sheet.
        LOGO_X: an integer for the game logo's x-position relative to
            the screen.
        LOGO_Y: an integer for the game logo's y-position relative to
            the screen.
        LOGO_FRAMES: An integer for the amount of animation frames in
            the game logo's sprite sheet.
        LOGO_DURATION: An integer for the duration of each frame in the
            game logo's animation, in update cycles.
        SFX_CONFIRM_PATH: A String for the file path of the sound effect
            that plays when an Option is confirmed.
        SFX_CANCEL_PATH: A String for the file path of the sound effect
            that plays when a decision is cancelled.
        SFX_SCROLL_PATH: A String for the file path of the sound effect
            that plays when switching focus between Options.
        SFX_SLIDE_PATH: A String for the file path of the sound effect
            that plays during OptionLists' slide in and slide out
            animations.

        Attributes:
            background: The Title Screen's background Animation.
            logo: The game logo Animation.
            intro_player: An IntroAnimator that manages and performs
                the introductory animation.
            option_lists: A list containing three different OptionLists.
                This contains one instance each of PressStartPrompt,
                MainOptionList, and BattleSetupList.
            current_options: An integer for the index of the currently-
                displayed Option List within the option_lists attribute.
    """
    BG_PATH = 'images/title_back.png'
    BG_FRAMES = 7
    BG_DURATION = 5
    LOGO_PATH = 'images/logo.png'
    LOGO_X = 12
    LOGO_Y = 40
    LOGO_FRAMES = 6
    LOGO_DURATION = 5
    SFX_CONFIRM_PATH = 'audio/confirm.wav'
    SFX_CANCEL_PATH = 'audio/cancel.wav'
    SFX_SCROLL_PATH = 'audio/scroll.wav'
    SFX_SLIDE_PATH = 'audio/woosh.ogg'

    def __init__(self, state_manager, state_pass):
        """Declare and initialize instance variables.

        Args:
            state_manager: The GameStateManager object that manages and
                updates this State.
            state_pass: The StatePass object that stores info to pass
                onto other States.
        """
        super(TitleState, self).__init__(state_manager, state_pass)
        self.background = Animation(self.BG_PATH, (0, 0), self.BG_FRAMES,
                                    self.BG_DURATION)
        self.logo = Animation(self.LOGO_PATH, (self.LOGO_X, self.LOGO_Y),
                              self.LOGO_FRAMES, self.LOGO_DURATION)
        self.intro_animator = IntroAnimator()

        confirm = Sound(self.SFX_CONFIRM_PATH)
        cancel = Sound(self.SFX_CANCEL_PATH)
        scroll = Sound(self.SFX_SCROLL_PATH)
        slide = Sound(self.SFX_SLIDE_PATH)
        prompt = PressStartPrompt(confirm, cancel, scroll, slide)
        main_options = MainOptionList(confirm, cancel, scroll, slide)
        battle_setup = BattleSetupList(confirm, cancel, scroll, slide)
        self.option_lists = [prompt, main_options, battle_setup]
        self.current_options = TitleOptionList.PRESS_START

        self.reset_state()

    def load_state(self):
        self.is_loaded = True

    def reset_state(self):
        """Prepare this State to be shown again."""
        self.intro_animator.reset(self.background, self.logo)
        for option_list in self.option_lists:
            option_list.reset()

    def update_state(self, time):
        """Update all processes within this State.

        Args:
            time: An float for the time elapsed, in seconds, since the
                last update cycle.
        """
        if self.intro_animator.is_running:
            self.intro_animator.update(time, self.background, self.logo)
        else:
            updated_options = self.option_lists[self.current_options]

            updated_options.update(time)
            if updated_options.next_state > -1:
                self.change_state(updated_options.next_state)
                updated_options.next_state = -1
            elif updated_options.is_offscreen():
                self.change_options()

        self.draw_state()

    def draw_state(self):
        """Draw all graphics onto the State Surface."""
        self.background.draw(self.state_surface)
        self.logo.draw(self.state_surface)
        if not self.intro_animator.is_running:
            self.option_lists[self.current_options].draw(self.state_surface)

    def get_player_input(self, event):
        """Respond to player input.

        Args:
            event: The PyGame Event containing key input data.
        """
        if self.intro_animator.is_running:
            self.intro_animator.skip_intro(self.background, self.logo)
        else:
            active_list = self.option_lists[self.current_options]
            if not active_list.is_animating():
                input_name = self.get_input_name(pygame.key.name(event.key))
                active_list.handle_input(input_name)

    def get_input_name(self, key_name):
        """Get the name of an in-game input command that is bound to a
        certain keyboard key.

        Examples of such input commands are start, forward, light punch,
        etc.

        Args:
            key_name: A String for the name of the keyboard key.

        Returns:
            A String containing the name of the desired input command.
            If the key is not bound to an input command, an empty String
            will be returned instead.
        """
        p1_keys = self.state_pass.settings.player1_keys
        p2_keys = self.state_pass.settings.player2_keys

        for input_name in p1_keys.keys():
            if key_name == p1_keys[input_name]:
                return input_name

        for input_name in p2_keys.keys():
            if key_name == p2_keys[input_name]:
                return input_name

        return ''

    def change_options(self):
        """Switch to another Option List, based on whichever list was
        previously shown.
        """
        if self.current_options in [TitleOptionList.PRESS_START,
                                    TitleOptionList.BATTLE_SETUP]:
            self.current_options = TitleOptionList.MAIN_OPTIONS
        elif self.current_options == TitleOptionList.MAIN_OPTIONS:
            self.current_options = TitleOptionList.BATTLE_SETUP

    def change_state(self, state_id):
        """Switch game processing to another Game State.

        Args:
            state_id: The index of the next Game State to be run. For
                possible values, refer to the StateIDs enum.
        """
        self.update_battle_settings()

        self.state_pass.will_reset_state = True
        self.state_pass.enter_transition_on = True

        super(TitleState, self).change_state(state_id)

    def update_battle_settings(self):
        """Set the battle parameters within the StatePass object using
        values from the BattleSetupList.
        """
        battle_setup = self.option_lists[TitleOptionList.BATTLE_SETUP]
        rounds = battle_setup.get_rounds()
        time_limit = battle_setup.get_time_limit()

        self.state_pass.battle_rounds = rounds
        self.state_pass.time_limit = time_limit


class IntroAnimator(object):
    """This class is in charge of animating the Title Screen's
    introductory animation.

    Class Constants:
        BG_OFFSET: A float for the distance of the background from the
            bottom of the screen, in pixels, when the animation starts.
        BG_SCROLL_SPEED: A float for the speed, in pixels per second,
            at which the background will be scrolled up.
        VOICE_PATH: A String for the file path of the voice clip where
            the announcer states the title of the game.
        FADE_DELAY: An integer for the alpha value that the logo
            Animation must attain before the voice clip is played.
        VOICE_DURATION: An integer for the duration of the voice clip,
            in update cycles.

    Attributes:
        is_running: A Boolean indicating whether the animation is
            currently being shown.
        voice: A PyGame Sound with the announcer stating the game's
            title.
        voice_timer: An integer counter that keeps track of how many
            update cycles have passed since the voice clip started
            playing.
        voice_has_played: A Boolean indicating whether the voice clip
            has already played.
    """
    BG_OFFSET = 50.0
    BG_SCROLL_SPEED = 70.0
    FADE_LOGO_RATE = 7
    VOICE_PATH = 'audio/announcer-title.wav'
    FADE_DELAY = 7
    VOICE_DURATION = 118
    MUSIC_PATH = 'audio/title_theme.wav'

    def __init__(self):
        """Declare and initialize instance variables."""
        self.is_running = False
        self.voice = Sound(self.VOICE_PATH)
        self.voice_timer = 0
        self.voice_has_played = False

    def update(self, time, bg, logo):
        """Update the animation's processes.

        The animation will proceed as follows:
            1. Scroll the background up from the bottom edge until it
               fills the screen.
            2. Fade in the logo.
            3. As it fades in, play the voice clip.
            4. Once the voice clip finishes, play the title theme and
               activate the logo's animation.

        Args:
            time: A float for the time elapsed, in seconds, since the
                last update cycle.
            bg: The Title Screen's background Animation.
            logo: The game logo Animation.
        """
        if bg.exact_pos[1] > 0.0:
            self.move_background_up(bg, time)
        elif logo.image.get_alpha() < 255:
            self.fade_in_logo(logo)

        if (logo.image.get_alpha() >= self.FADE_DELAY
                and (not self.voice_has_played)):
            self.voice.play()
            self.voice_has_played = True
        elif (self.voice_has_played and
              self.voice_timer < self.VOICE_DURATION):
            self.voice_timer += 1
        elif self.voice_timer >= self.VOICE_DURATION:
            pygame.mixer.music.play(-1)
            logo.is_animated = True
            self.is_running = False

    def move_background_up(self, bg, time):
        """Move the background up at a set speed.

        The background will not move past the top edge of the screen.

        Args:
            bg: The Title Screen's background Animation.
            time: A float for the amount of time, in seconds, elapsed
                since the last update cycle.
        """
        distance = -1 * self.BG_SCROLL_SPEED * time
        bg.move(0, distance)

        if bg.exact_pos[1] < 0.0:
            distance = 0.0 - bg.exact_pos[1]
            bg.move(0, distance)

    def fade_in_logo(self, logo):
        """Gradually increase the opacity of the game logo.

        Args:
            logo: The game logo Animation.
        """
        old_alpha = logo.image.get_alpha()
        logo.image.set_alpha(old_alpha + self.FADE_LOGO_RATE)

    def skip_intro(self, bg, logo):
        """Skip to the end of animation immediately.

        Args:
            bg: The Title Screen's background Animation.
            logo: The game logo Animation.
        """
        if not self.voice_has_played:
            self.voice.play()

        bg.move(0, -1 * bg.rect[1])
        pygame.mixer.music.play(-1)
        logo.image.set_alpha(255)
        logo.is_animated = True
        self.is_running = False

    def reset(self, bg, logo):
        """Prepare the animation to be shown.

        This method must be called before the first call to update()
        to ensure that all components are ready for use.
        If not, bad things will happen... (maybe)

        Args:
            bg: The Title Screen's background Animation.
            logo: The game logo Animation.
        """
        pygame.mixer.stop()
        pygame.mixer.music.load(self.MUSIC_PATH)
        self.voice_timer = 0
        self.voice_has_played = False
        bg.exact_pos = (0.0, SCREEN_SIZE[1] + self.BG_OFFSET)
        logo.is_animated = False
        logo.image.set_alpha(0)
        self.is_running = True


# Option Lists
class OptionList(object):
    """Contains various Options that the players can scroll through and
    confirm.

    This is an abstract class; subclasses should implement their own
    unique Options as well as ways of responding to them.

    Class Constants:
        OPTION_DISTANCE: The vertical distance, in pixels, between
            two Options.
        CONFIRM_DURATION: An integer for the time, in update frames, to
            flash a confirmed Option's text before performing the
            appropriate operation.
        TEXT_FLASH_SPEED: An integer for the speed, in update frames, at
            which Option text will flash upon being selected and
            confirmed. For example, a value of 5 means that the text
            will change its visibility every 5 update cycles.
        TEXT_SLIDE_SPEED: The speed at which to slide Options in and out
            of the screen, in pixels per second.

    Attributes:
        options: A list of Options.
        option_index: The index of the Option currently being
            highlighted by the players.
        x: An integer coordinate for the OptionList's x-position
            relative to the screen.
        y: An integer coordinate for the OptionList's y-position
            relative to the screen.
        sfx_confirm: A PyGame Sound that plays when the players confirm
            an option.
        sfx_cancel: A PyGame Sound that plays when the players leave
            this OptionList or otherwise cancel a decision.
        sfx_scroll: A PyGame Sound that plays when the players scroll
            through the list of Options.
        confirm_timer: An integer counter that keeps track of how long
            a confirmed Option has been flashing. Setting it to -1 or
            less will stop the timer.
        animation: An integer value indicating whether an animation
            should be performed and if so, which. Refer to the
            ListAnimation enum for the possible values.
        next_state: The index of the next Game State will be run. Refer
            to the StateIDs enum for possible choices. A value of -1
            means that processing should remain in the Title State.
    """
    OPTION_DISTANCE = 8
    CONFIRM_DURATION = 60
    TEXT_FLASH_SPEED = 5
    TEXT_SLIDE_SPEED = 800

    def __init__(self, x, y, sfx_confirm, sfx_cancel, sfx_scroll,
                 sfx_slide):
        """Declare and initialize instance variables.

        Args:
            x: An integer for the x-position of the first Option,
                relative to the screen.
            y: An integer for the y-position of the first Option,
                relative to the screen.
            sfx_confirm: A PyGame Sound for confirming an option.
            sfx_cancel: A PyGame Sound for cancelling a decision.
            sfx_scroll: A PyGame Sound for scrolling through the list.
        """
        self.x = x
        self.y = y
        self.sfx_confirm = sfx_confirm
        self.sfx_cancel = sfx_cancel
        self.sfx_scroll = sfx_scroll
        self.sfx_slide = sfx_slide
        self.option_index = 0
        self.confirm_timer = -1
        self.animation = ListAnimation.NONE
        self.next_state = -1
        self.options = []
        self.create_options()
        self.highlight_option(0)

    def create_options(self):
        """Create all of the Options within this OptionList."""
        raise NotImplementedError

    def handle_input(self, input_name):
        """Respond to player input.

        Args:
            input_name: A String for the name of the input that was
                entered. (e.g. 'start', 'forward')
        """
        raise NotImplementedError

    def update(self, time):
        """Update the processes within this OptionList.

        Text flash for the currently-selected Option will be performed
        if the confirmation timer is set to a value higher than -1.
        Once it has flashed long enough, the operation described by
        the selected Option will be performed.
        In other cases, an animation will be shown based on the value
        of the animation variable.
        
        Args:
            time: A float for the amount of time elapsed, in seconds,
                since the last update cycle.
        """
        if self.is_offscreen():
            self.animation = ListAnimation.SHOW

        if self.confirm_timer > -1:
            self.flash_confirmed_option()
            if self.confirm_timer >= self.CONFIRM_DURATION:
                self.confirm_timer = -1     # End the flash.
                self.respond_to_confirm()
        elif self.animation == ListAnimation.SHOW:
            self.show_all(time)
        elif self.animation == ListAnimation.HIDE:
            self.hide_all(time)

    def draw(self, parent_surf):
        """Draw all of the Options in this list onto a Surface.

        Args:
            parent_surf: The Surface upon which the Option will be drawn
                to.
        """
        for option in self.options:
            option.draw(parent_surf)

    def reset(self):
        """Prepare this OptionList to be shown again."""
        raise NotImplementedError

    def prepare_to_show_all(self):
        """Position all of the Options in this list for the start of the
        'show all' animation.

        The first, third, etc. Options will start from the left edge of
        the screen, while every other Option will start from the right.
        """
        offset_from_center = (SCREEN_SIZE[0] / 2) - self.x

        biggest_width = 0
        for i in xrange(0, len(self.options), 2):
            if self.options[i].get_width > biggest_width:
                biggest_width = self.options[i].get_width()

        for i in xrange(0, len(self.options), 2):
            self.options[i].x = 0 - (offset_from_center * 2) - biggest_width
            
        if len(self.options) > 1:
            for i in xrange(1, len(self.options), 2):
                self.options[i].x = SCREEN_SIZE[0] + biggest_width

    def show_all(self, time):
        """Animate the OptionList revealing itself on-screen.
        
        The animation consists of sliding the Options in from either
        edge of the screen. The direction of the slide alternates
        between Options. (e.g. The first Option slides in from the left
        while the second Option comes from the right.)
        
        Args:
            time: A float for the time elapsed, in seconds, since the
                last update cycle.
        """
        if self.options[0].x == self.x:
            self.prepare_to_show_all()
        else:
            distance = int(self.TEXT_SLIDE_SPEED * time)
            
            for i in xrange(0, len(self.options), 2):
                self.options[i].x += distance
                # Prevent the Option from sliding past its final position.
                if self.options[i].x > self.x:
                    self.options[i].x = self.x
            if len(self.options) > 1:
                for i in xrange(1, len(self.options), 2):
                    self.options[i].x -= distance
                    if self.options[i].x < self.x:
                        self.options[i].x = self.x
                    
            if self.options[0].x >= self.x:
                self.animation = ListAnimation.NONE

    def hide_all(self, time):
        """Hide this OptionList on-screen and then send processing over
        to the next queued OptionList.

        The animation consists of sliding the Options out to either
        edge of the screen. The direction of the slide alternates
        between Options. (e.g. The first Option slides out to the left
        while the second Option goes over to the right.)

        Args:
            time: A float for the time elapsed, in seconds, since the
                last update cycle.
        """
        if self.options[0].x == self.x:
            self.sfx_slide.play()

        distance = self.TEXT_SLIDE_SPEED * time

        for i in xrange(0, len(self.options), 2):
            self.options[i].x -= distance
        if len(self.options) > 1:
            for i in xrange(1, len(self.options), 2):
                self.options[i].x += distance

    def is_animating(self):
        """Determine whether this OptionList is currently performing an
        animation.

        Returns:
            True if an Option is flashing or either of the slide in/out
            animations are being performed; False otherwise.
        """
        if self.confirm_timer > -1 or self.animation != ListAnimation.NONE:
            return True
        else:
            return False

    def is_offscreen(self):
        """Return a Boolean indicating whether all of the Options in
        this list are outside of the game window's viewable drawing
        region.
        """
        if self.animation == ListAnimation.HIDE:
            for i in range(0, len(self.options), 2):
                right_edge = self.options[i].x + self.options[i].get_width()
                if right_edge > 0:
                    return False

            for i in range(1, len(self.options), 2):
                if self.options[i].x < SCREEN_SIZE[0]:
                    return False

            return True
        else:
            return False

    def highlight_option(self, index):
        """Highlight one of the Options in this list.

        All other Options will be unhighlighted to emphasize focus on
        that single Option.

        Args:
            index: An integer for the index of an Option within this
                object's options list.
        """
        for option_text in self.options:
            option_text.unhighlight()
        self.options[index].highlight()

    def scroll_up(self):
        """Select the previous Option in the list."""
        if self.option_index <= 0:
            self.option_index = len(self.options) - 1
        else:
            self.option_index -= 1

        self.sfx_scroll.play()
        self.highlight_option(self.option_index)

    def scroll_down(self):
        """Select the next Option in the list."""
        if self.option_index >= len(self.options) - 1:
            self.option_index = 0
        else:
            self.option_index += 1

        self.sfx_scroll.play()
        self.highlight_option(self.option_index)

    def confirm_option(self):
        """Confirm the currently-selected Option and perform the
        appropriate operation.

        The Option will flash on-screen to indicate the confirmation.
        """
        self.sfx_confirm.play()
        self.confirm_timer = 0

    def flash_confirmed_option(self):
        """Flash the name of the confirmed Option."""
        self.confirm_timer += 1

        if self.confirm_timer % self.TEXT_FLASH_SPEED == 0:
            self.options[self.option_index].is_visible = (
                not self.options[self.option_index].is_visible)
    
    def respond_to_confirm(self):
        """Perform an operation based on the Option that was just
        confirmed.
        """
        raise NotImplementedError


class PressStartPrompt(OptionList):
    """The prompt that says "PRESS START" on the Title Screen, right
    after the introductory animation.

    Pressing Start will bring the players to another OptionList with the
    main Title Screen Options.

    Class Constants:
        X: An integer for the x-position of the prompt relative to the
            screen.
        Y: An integer for the y-position of the prompt relative to the
            screen.
        WAIT_SPEED_FLASH: An integer for the speed of the prompt's
            flash, in update cycles, while it is waiting for the
            players' input.

    Attributes:
        idle_flash_timer: An integer counter that keeps track of how
            many update cycles have flashed since the last time the
            prompt's visibility was toggled. Setting it to -1 or less
            will stop the idle flashing.
    """
    X = 135
    Y = 150
    WAIT_FLASH_SPEED = 45

    def __init__(self, sfx_confirm, sfx_cancel, sfx_scroll, sfx_slide):
        """Declare and initialize instance variables.

        Args:
            sfx_confirm: A PyGame Sound for confirming an option.
            sfx_cancel: A PyGame Sound for cancelling a decision.
            sfx_scroll: A PyGame Sound for scrolling through the list.
        """
        super(PressStartPrompt, self).__init__(self.X, self.Y,
                                               sfx_confirm, sfx_cancel,
                                               sfx_scroll, sfx_slide)
        self.idle_flash_timer = 0

    def create_options(self):
        """Create the prompt."""
        self.options.append(Option("Press Start", self.x, self.y))

    def update(self, time):
        """Update the processes within this prompt.

        Aside from confirmation flashing and show/hide animations,
        the 'Press Start' prompt will also flash at a slower speed
        while waiting for the players' input.

        Args:
            time: A float for the amount of time elapsed, in seconds,
                since the last update cycle.
        """
        if self.confirm_timer <= -1 and self.animation == ListAnimation.NONE:
            self.flash_idly()
        else:
            super(PressStartPrompt, self).update(time)

    def handle_input(self, input_name):
        """Go to the Main Options when the players press Start.

        Args:
            input_name: A String for the name of the input pressed.
        """
        if input_name == "start":
            self.idle_flash_timer = -1
            self.options[0].is_visible = True
            self.confirm_option()

    def reset(self):
        """Prepare the prompt to be shown again."""
        self.x = self.X
        self.y = self.Y
        self.idle_flash_timer = 0
        self.animation = ListAnimation.NONE

    def respond_to_confirm(self):
        """Hide the prompt and then go to the Main Options list."""
        self.animation = ListAnimation.HIDE

    def flash_idly(self):
        """Flash the prompt at a slower speed for waiting."""
        self.idle_flash_timer += 1

        if self.idle_flash_timer >= self.WAIT_FLASH_SPEED:
            self.options[0].is_visible = not self.options[0].is_visible
            self.idle_flash_timer = 0


class MainOptionList(OptionList):
    """An OptionList containing the 'main' Options one would expect to
    find on the game's Title Screen. They are:
        1. Battle - Set up a 2-player battle. This will call the
            BattleSetupList.
        2. Training - Launch Training Mode.
        3. Settings - Open the Settings screen.
        4. Exit - Close the game window.

    Class Constants:
        X: The x-position of the Options relative to the screen.
        Y: The y-position of the top Option relative to the screen.

    Attributes:
        state_pass: The StatePass object containing data that will be
            transferred between all Game States.
    """
    X = 155
    Y = 104

    def __init__(self, sfx_confirm, sfx_cancel, sfx_scroll, sfx_slide):
        """Declare and initialize instance variables.

        Args:
            sfx_confirm: A PyGame Sound for confirming an option.
            sfx_cancel: A PyGame Sound for cancelling a decision.
            sfx_scroll: A PyGame Sound for scrolling through the list.
        """
        super(MainOptionList, self).__init__(self.X, self.Y,
                                             sfx_confirm, sfx_cancel,
                                             sfx_scroll, sfx_slide)
        self.animation = ListAnimation.SHOW

    def create_options(self):
        """Create all of the Main Options and add them to the list."""
        names = ['Battle', 'Training', 'Settings', 'Exit']
        y = self.y

        for i in xrange(0, len(names)):
            self.options.append(Option(names[i], self.x, y))
            y += self.options[i].get_height() + self.OPTION_DISTANCE

    def handle_input(self, input_name):
        """Respond to input from the players.

        Args:
            input_name: A String for the name of the input pressed.
        """
        if input_name == 'up':
            self.scroll_up()
        elif input_name == 'down':
            self.scroll_down()
        elif input_name == 'start':
            self.confirm_option()

    def reset(self):
        """Prepare the OptionList to be shown again."""
        self.prepare_to_show_all()
        self.animation = ListAnimation.SHOW

    def respond_to_confirm(self):
        """Perform the appropriate operation based on whichever Option
        was just confirmed.
        """
        if self.option_index == MainOptionIndex.BATTLE:
            self.go_to_battle()
        elif self.option_index == MainOptionIndex.TRAINING:
            self.go_to_training()
        elif self.option_index == MainOptionIndex.SETTINGS:
            self.go_to_settings()
        elif self.option_index == MainOptionIndex.EXIT:
            self.exit_game()

    def go_to_battle(self):
        """Set up a new battle.

        This will bring the players to the BattleSetupList.
        """
        self.animation = ListAnimation.HIDE

    def go_to_training(self):
        """Launch Training Mode.

        This will immediately bring the players to the Character Select
        screen.
        """
        self.next_state = StateIDs.SELECT_CHARACTER

    def go_to_settings(self):
        self.next_state = StateIDs.SETTINGS

    def exit_game(self):
        """Close the game window."""
        pygame.quit()
        sys.exit()


class BattleSetupList(OptionList):
    """An OptionList that allows the players to specify parameters for
    an upcoming battle.

    These parameters include:
        1. Rounds - The total number of rounds in the upcoming battle.
            (e.g. 3 rounds for the best 2 out of 3.)
        2. Time Limit - The amount of time, in seconds, allotted for
            each round in the upcoming battle.

    In addition to these two BattleSettings, a third Option, "Begin",
    allows the players to confirm the chosen parameters and proceed to
    the Character Select Screen.

    Class Constants:
        X: The x-position of the first BattleSetting relative to the
            screen.
        Y: The y-position of the first BattleSetting relative to the
            screen.

    Attributes:
        state_pass: The StatePass object containing data that will be
            passed between all Game States.
    """
    X = 130
    Y = 117

    def __init__(self, sfx_confirm, sfx_cancel, sfx_scroll, sfx_slide):
        """Declare and initialize instance variables.

        Args:
            sfx_confirm: A PyGame Sound for confirming an option.
            sfx_cancel: A PyGame Sound for cancelling a decision.
            sfx_scroll: A PyGame Sound for scrolling through the list.
        """
        super(BattleSetupList, self).__init__(self.X, self.Y,
                                              sfx_confirm, sfx_cancel,
                                              sfx_scroll, sfx_slide)
        self.animation = ListAnimation.SHOW

    def create_options(self):
        """Create the two BattleSettings, as well as the 'Begin'
        Option, and add them to the list.
        """
        y = self.y
        rounds = BattleSetting('Rounds', self.x, y, 1, 3, 5)

        y += rounds.get_height() + self.OPTION_DISTANCE
        time_limit = BattleSetting('Time Limit', self.x, y, 30, 60, 99)

        y += time_limit.get_height() + self.OPTION_DISTANCE
        begin = Option('Begin', self.x, y)

        self.options.extend([rounds, time_limit, begin])

    def handle_input(self, input_name):
        """Respond to input from the players.

        Args:
            input_name: A String for the name of input pressed.
        """
        if input_name == 'up':
            self.scroll_up()
        elif input_name == 'down':
            self.scroll_down()
        elif input_name == 'back':
            self.scroll_setting_values_left()
        elif input_name == 'forward':
            self.scroll_setting_values_right()
        elif (input_name == 'start' and
              self.option_index == BattleSetupIndex.BEGIN):
            self.confirm_option()
        elif input_name == 'cancel':
            self.cancel_setup()

    def reset(self):
        """Prepare the OptionList to be shown again."""
        self.prepare_to_show_all()
        self.animation = ListAnimation.SHOW

    def get_rounds(self):
        """Return the number of rounds in the upcoming battle."""
        return self.options[BattleSetupIndex.ROUNDS].get_value()

    def get_time_limit(self):
        """Return the time limit per round in the upcoming battle."""
        return self.options[BattleSetupIndex.TIME_LIMIT].get_value()

    def scroll_setting_values_left(self):
        """Select the previous value in the currently-selected
        BattleSetting.

        If the selected Option is not a BattleSetting, nothing will
        occur.
        """
        if type(self.options[self.option_index]) == BattleSetting:
            self.options[self.option_index].scroll_values_left(
                self.sfx_scroll)

    def scroll_setting_values_right(self):
        """Select the next value in the currently-selected
        BattleSetting.

        If the selected Option is not a BattleSetting, nothing will
        occur.
        """
        if type(self.options[self.option_index]) == BattleSetting:
            self.options[self.option_index].scroll_values_right(
                self.sfx_scroll)

    def cancel_setup(self):
        """Hide the setup list and return to the list of Main Options."""
        self.animation = ListAnimation.HIDE

    def respond_to_confirm(self):
        """Proceed to the Character Select Screen with the chosen
        battle parameters.
        """
        self.next_state = StateIDs.SELECT_CHARACTER


# Option Classes
class Option(object):
    """An option that the players can select within the Title State.

    It is represented by a text name on the screen, which can be
    recolored or hidden to indicate player selection or confirmation.

    Class Constants:
        NORMAL_COLOR: A String name for the regular color of an Option.
        HIGHLIGHT_COLOR: A String name for the color of an Option when
            it is selected by the users.
        FONT_PATH: A String for the file path to the font file that
            will be used in rendering graphical text for Options.
        FONT_SIZE: An integer size of the font used in rendering Option
            text.

    Attributes:
        text: The text String that describes this Option. It will be
            written on the screen.
        x: An integer value for the Option text's x-coordinate relative
            to the screen.
        y: An integer value for the Option text's y-coordinate relative
            to the screen.
        is_visible: A Boolean indicating whether the text will be
            drawn onto its parent Surface.
        font: The PyGame Font object that stores the font used in
            rendering text.
        surf: The text graphic will be rendered onto this PyGame
            Surface.
    """
    NORMAL_COLOR = 'dark gray'
    HIGHLIGHT_COLOR = 'white'
    FONT_PATH = 'fonts/fighting-spirit-TBS.ttf'
    FONT_SIZE = 18

    def __init__(self, text, x, y):
        """Declare and initialize instance variables.

        Args:
            text: The String that describes this option.
            x: An integer value for the Option text's x-coordinate
                relative to the screen.
            y: An integer value for the Option text's y-coordinate
                relative to the screen.
        """
        self.text = text
        self.x = x
        self.y = y
        self.is_visible = True
        self.font = Font(self.FONT_PATH, self.FONT_SIZE)
        self.surf = self.render_text(text, self.NORMAL_COLOR)

    def render_text(self, text, color_name):
        """Create a new Surface with the specified text, using the
        font specifications defined by this class.

        Args:
            text: The String of text that will be drawn.
            color_name: A String containing the name or hex code of the
                color of the text.

        Returns:
            A Surface with the text drawn onto it.
        """
        text_color = Color(color_name)
        return self.font.render(text, True, text_color)

    def highlight(self):
        """Redraw the text with an alternate color."""
        self.surf = self.render_text(self.text, self.HIGHLIGHT_COLOR)

    def unhighlight(self):
        """Redraw the text with normal coloration."""
        self.surf = self.render_text(self.text, self.NORMAL_COLOR)

    def get_width(self):
        """Return the integer width of the text graphic."""
        return self.surf.get_width()

    def get_height(self):
        """Return the integer height of the text graphic."""
        return self.surf.get_height()

    def draw(self, parent_surf):
        """Draw the text onto a Surface.

        The text will only be shown if the is_visible attribute is set
        to True.

        Args:
            parent_surf: The Surface upon which the text will be drawn.
        """
        if self.is_visible:
            parent_surf.blit(self.surf, (self.x, self.y))


class BattleSetting(Option):
    """One of the parameters required for setting up a battle.

    Aside from being a selectable Option, it also contains its own list
    of numerical values that the players can scroll through.

    Class Constants:
        VALUE_X: The integer coordinate for the x-position of value
            text relative to the screen.
        LEFT_ARROW_PATH: A String for the file path to the scroll left
            arrow image.
        ARROW_DISTANCE: An integer for the horizontal distance between
            each scroll arrow and the text for the selected value.
        ARROW_Y_OFFSET: The integer distance, in pixels, between the
            the top of the text graphic and the top of each scroll
            arrow.

    Attributes:
        values: A list of integer values that can be set for this
            BattleSetting.
        value_index: An integer for the index of the currently-selected
            value.
        value_surf: A PyGame Surface that contains the text graphic
            for the currently-selected value.
        scroll_left_arrow: A Graphic that displays the image of the
            'scroll values left' arrow.
        scroll_right_arrow: A Graphic that displays the image of the
            'scroll values right' arrow.
    """
    VALUE_DISTANCE = 118
    LEFT_ARROW_PATH = 'images/battle_setup_arrow_left.png'
    ARROW_DISTANCE = 7
    ARROW_Y_OFFSET = 5

    def __init__(self, text, x, y, *values):
        """Declare and initialize instance variables.

        Args:
            text: The String that describes this BattleSetting.
            x: The integer coordinate for the text's x-position relative
                to the screen.
            y: The integer coordinate for the text's y-position relative
                to the screen.
            values: All of the integer values that can be set for this
                BattleSetting.
        """
        super(BattleSetting, self).__init__(text, x, y)
        self.values = values
        self.value_index = 0
        self.value_surf = self.render_text(str(self.values[0]),
                                           self.NORMAL_COLOR)
        value_x = self.x + self.VALUE_DISTANCE
        self.scroll_left_arrow = Graphic(self.LEFT_ARROW_PATH,
            (value_x - self.ARROW_DISTANCE, self.y + self.ARROW_Y_OFFSET))
        self.scroll_left_arrow.move(-1 * self.scroll_left_arrow.rect[2], 0)
        self.scroll_right_arrow = Graphic(self.LEFT_ARROW_PATH,
            (value_x + self.value_surf.get_width() + self.ARROW_DISTANCE,
            self.y + self.ARROW_Y_OFFSET))
        self.scroll_right_arrow.flip(is_horizontal=True)

    def scroll_values_left(self, scroll_sound):
        """Select the previous value for this BattleSetting.

        Args:
            scroll_sound: A PyGame Sound for scrolling through choices.
        """
        if self.value_index > 0:
            self.value_index -= 1
            self.value_surf = self.render_text(
                str(self.values[self.value_index]), self.HIGHLIGHT_COLOR)
            scroll_sound.play()

    def scroll_values_right(self, scroll_sound):
        """Select the next value for this BattleSetting.

        Args:
            scroll_sound: A PyGame Sound for scrolling through choices.
        """
        if self.value_index < len(self.values) - 1:
            self.value_index += 1
            self.value_surf = self.render_text(
                str(self.values[self.value_index]), self.HIGHLIGHT_COLOR)
            scroll_sound.play()

    def highlight(self):
        """Redraw the text with an alternate color."""
        super(BattleSetting, self).highlight()
        self.value_surf = self.render_text(
            str(self.values[self.value_index]), self.HIGHLIGHT_COLOR)

    def unhighlight(self):
        """Redraw the text with normal coloration."""
        super(BattleSetting, self).unhighlight()
        self.value_surf = self.render_text(
            str(self.values[self.value_index]), self.NORMAL_COLOR)

    def get_value(self):
        """Return the selected value."""
        return self.values[self.value_index]

    def draw(self, parent_surf):
        """Draw the text onto a Surface.

        Args:
            parent_surf: The Surface upon which the BattleSetting text
                will be drawn.
        """
        super(BattleSetting, self).draw(parent_surf)
        parent_surf.blit(self.value_surf, (self.x + self.VALUE_DISTANCE,
                                           self.y))
        self.draw_scroll_arrows(parent_surf)

    def draw_scroll_arrows(self, parent_surf):
        """Draw the scroll value arrows onto a Surface.

        The left arrow will only be shown if there are values preceding
        the one that is selected. Likewise, the right arrow will only
        be shown if there are subsequent values.

        Args:
            parent_surf: The Surface upon which the arrows will be
                drawn.
        """
        value_x = self.x + self.VALUE_DISTANCE
        left_arrow_x = (value_x - self.scroll_left_arrow.rect[2]
                        - self.ARROW_DISTANCE)
        right_arrow_x = (value_x + self.value_surf.get_width()
                         + self.ARROW_DISTANCE)
        y = self.y + self.ARROW_Y_OFFSET

        if self.value_index > 0:
            self.scroll_left_arrow.draw(parent_surf, left_arrow_x, y)
        if self.value_index < len(self.values) - 1:
            self.scroll_right_arrow.draw(parent_surf, right_arrow_x, y)


# Enumerations
class TitleOptionList(object):
    """An enum containing the indices of all of the OptionLists within
    TitleState.

    Attributes:
        PRESS_START: An integer for the index of the 'press start'
            prompt.
        MAIN_OPTIONS: An integer for the index of the list containing
            the actual Title Screen options. (e.g. Battle, Settings)
        BATTLE_SETUP: An integer for the index of the list where the
            parameters for the next battle can be set.
    """
    PRESS_START = 0
    MAIN_OPTIONS = 1
    BATTLE_SETUP = 2


class ListAnimation(object):
    """An enumeration for the different animations that an OptionList
    can perform.

    Attributes:
        NONE: An integer value indicating that no animation should be
            shown.
        SHOW: An integer value indicating that the slide-in animation
            should be shown.
        HIDE: An integer value indicating that the slide-out animation
            should be shown.
    """
    NONE = 0
    SHOW = 1
    HIDE = 2


class MainOptionIndex(object):
    """An enumeration for the index of each Option within the list of
    the Main Title Screen Options.

    Attributes:
        BATTLE: An integer for the index of the Option for setting up a
            new battle.
        TRAINING: An integer for the index of Option for launching
            Training Mode.
        SETTINGS: An integer for the index of Option that will call the
            Settings Screen.
        EXIT: An integer for the index of the Option that will close
            the game.
    """
    BATTLE = 0
    TRAINING = 1
    SETTINGS = 2
    EXIT = 3


class BattleSetupIndex(object):
    """An enumeration for the index of each Option within the
    BattleSetupList.

    Attributes:
        ROUNDS: An integer for the index of the BattleSetting that sets
            the number of rounds for the upcoming battle.
        TIME_LIMIT: An integer for the index of the BattleSetting that
            sets the number time limit per round for the upcoming
            battle.
        BEGIN: An integer for the index of the Option that will allow
            the players to confirm battle settings and proceed to the
            Character Select Screen.
    """
    ROUNDS = 0
    TIME_LIMIT = 1
    BEGIN = 2
