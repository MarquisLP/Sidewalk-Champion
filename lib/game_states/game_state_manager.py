import sys
import pygame
from pygame.locals import *
from lib.globals import *
from lib.game_states.state import *
from lib.game_states.state_ids import StateIDs
from lib.game_states.title_state import TitleState
from lib.game_states.settings_state import SettingsState

class GameStateManager(object):
    """This class runs the main game loop and updates the appropriate
    Game State.

    These Game States include: Title Screen, Settings, Selecting
    Characters, Selecting Stage, and Battle.
    Game processing works by switching between States and passing
    data between them.

    Attributes:
        character_list      Contains all of the CharacterData objects
                            for every playable Character listed in the
                            characters/character_list.txt file.
        stage_list          Contains all of the StageData objects for
                            every playable Stage listed in the
                            stages/stage_list.txt file.
        screen              The PyGame display Surface that represents
                            the game screen.
        clock               A timer provided by the PyGame time module.
                            It records the time elapsed between updates
                            in milliseconds.
        active_state        The State object that will be updated
                            and displayed.
        active_state_id     The index of the currently-active State
                            within state_list. Note that all of these
                            indexes are labelled by the StateIDs enum.
        previous_state_id   The index of the previously-active State
                            within state_list.
        state_pass          A StatePass object containing info to pass
                            between States as they are loaded.
        state_list          A List of all the State objects present
                            within the game.
    """
    # Initialization
    def __init__(self, screen, clock, all_characters, all_stages,
                 settings_data):
        """Initialize instance variables.

        Keyword arguments:
            screen          The PyGame Surface object that will serve
                            as the game window.
            all_characters  A list containing CharacterData objects for
                            all of the playable characters.
            all_stages      A list containing StageData objects for all
                            of the playable stages.
            settings_data   A SettingsData object for various options
                            that can be set by the players via the
                            Settings screen.   
        """
        self.character_list = all_characters
        self.stage_list = all_stages
        self.clock = clock
        self.screen = screen
        self.state_pass = StatePass(settings_data)
        self.state_list = self.create_state_list()
        self.active_state = self.state_list[StateIDs.TITLE]
        self.active_state_id = StateIDs.TITLE
        self.previous_state = None
        self.previous_state_id = StateIDs.TITLE

        self.set_update_timer()

    def create_state_list(self):
        """Create and initialize all State objects and return them in a
        List.
        """
        title_state = TitleState(self, self.state_pass)
        settings_state = SettingsState(self, self.state_pass)

        state_list = [title_state, settings_state]

        return state_list

    def set_update_timer(self):
        """Create the update timer.

        This frame rate constant can be found within lib.globals.
        """
        # Get the frame rate in milliseconds.
        timer_rate = int((1.0 / FRAME_RATE) * 1000)

        pygame.time.set_timer(USEREVENT, timer_rate)

    # Game Processing
    def change_state(self, next_state_id):
        """Change processing to the specified State. State resetting
        and loading may also be performed depending on the values
        within state_pass.

        Keyword arguments:
            next_state_id       The index of the next State to run.
                                This index refers to the State's
                                position within state_list.
        """
        self.previous_state_id = self.active_state_id
        self.previous_state = self.state_list[self.previous_state_id]

        self.active_state_id = next_state_id
        self.active_state = self.state_list[self.active_state_id]

        if self.active_state.is_loaded == False:
           self.active_state.load_state()
        elif self.state_pass.will_reset_state == True:
            self.active_state.reset_state()

        if self.state_pass.enter_transition_on:
            self.active_state.is_intro_on = True
            self.state_pass.enter_transition_on = False

    def get_seconds_elapsed(self):
        """Return the number of seconds elapsed since the last update.
        """
        milliseconds = self.clock.tick()
        seconds = milliseconds / 1000.0

        return seconds

    def scale_screen(self, scale):
        """Resize the screen when the screen scale changes.

        Keyword arguments:
            scale       The magnification rate.
        """
        scaled_size = (SCREEN_SIZE[0] * scale,
                    SCREEN_SIZE[1] * scale)

        if self.screen.get_size() != scaled_size:
            self.screen = pygame.display.set_mode(scaled_size)

    def scale_surface(self, surf, scale):
        """Magnify the specified Surface according to the specified
       magnification rate and return the modified Surface.

        Keyword arguments:
            surf        The Surface to resize.
            scale       The magnification rate.
        """
        new_size = (SCREEN_SIZE[0] * scale,
                    SCREEN_SIZE[1] * scale)
        scaled_surf = pygame.transform.scale(surf, new_size)

        return scaled_surf

    def update_state(self, state_id):
        """Update the specified State.

        Keyword arguments:
            state_id        The index of the State to update within
                            state_list.
        """
        time = self.get_seconds_elapsed()
        updated_state = self.state_list[state_id]

        updated_state.update_state(time)

    def draw_background(self):
        """Draw a black background underneath all States.
        This will keep the screen from being blank, which can reduce
        the likelihood of strange graphical glitches.
        """
        pygame.draw.rect(self.screen, (0, 0, 0),
                         Rect(0, 0, SCREEN_SIZE[0], SCREEN_SIZE[1]))

    def draw_state(self, state_id):
        """Draw the specified state's surface onto the screen and
        update the screen as a whole.
        The State Surface will also be scaled according to screen_scale
        within state_pass.

        Keyword arguments:
            state_id        The index of the State for drawing within
                            state_list.
        """
        scale = self.state_pass.settings.screen_scale
        drawn_state = self.state_list[state_id]

        scaled_surface = self.scale_surface(drawn_state.state_surface,
                                            scale)
        self.screen.blit(scaled_surface, drawn_state.screen_offset())

    def run_game(self):
        """Run the main game loop."""
        self.active_state.load_state()

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == KEYDOWN:
                    if self.active_state.is_accepting_input:
                        self.active_state.get_player_input(event)

                # Update processes after a passage of time equal to the
                # global frame rate.
                if event.type == USEREVENT:
                    self.scale_screen(
                        self.state_pass.settings.screen_scale)
                    self.draw_background()

                    self.update_state(self.active_state_id)
                    self.draw_state(self.active_state_id)
                    pygame.display.update()

            pygame.time.wait(0)