import sys
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
        character_list: Contains all of the CharacterData objects for
            every playable Character listed in the
            characters/character_list.txt file.
        stage_list: Contains all of the StageData objects for every
            playable Stage listed in the stages/stage_list.txt file.
        screen: The PyGame display Surface that represents the game
            screen.
        clock: A timer provided by the PyGame time module. It records
            the time elapsed between updates in milliseconds.
        state_pass: A StatePass object containing info to pass between
            States as they are loaded.
        state_list: A List of all the State objects present within the
            game.
        active_state_stack: A List containing all of the currently-active
            States, in the order they were called. The top-most State will
            always be called when the game updates, while other States
            underneath it will only be drawn and updated if they are visible on
            the screen.
        zoom_one_surf: A Surface with dimensions equivalent to the
            native resolution of the game. (See SCREEN_SIZE in
            globals.py.)
        zoom_two_surf: A Surface with dimensions twice as large as the
            native resolution.
        zoom_three_surf: A Surface with dimensions three times as large
            as the native resolution.
        scaled_surf: A Surface with dimensions that match the current
            window magnification rate. (The rate is defined by
            screen_scale in state_pass.settings.)
    """
    # Initialization
    def __init__(self, screen, clock, all_characters, all_stages,
                 settings_data):
        """Initialize instance variables.

        Args:
            screen: The PyGame Surface object that will serve
                as the game window.
            all_characters: A list containing CharacterData objects for
                all of the playable characters.
            all_stages: A list containing StageData objects for all
                of the playable stages.
            settings_data: A SettingsData object for various options
                that can be set by the players via the Settings screen.
        """
        self.character_list = all_characters
        self.stage_list = all_stages
        self.clock = clock
        self.screen = screen
        self.state_pass = StatePass(settings_data)
        self.active_state_stack = [self.create_state_by_id(StateIDs.TITLE)]
        self.create_scaled_surfaces()

    def create_scaled_surfaces(self):
        """Create three Surfaces with dimensions that reflect each of
        the possible window magnification rates: 1x, 2x, and 3x.

        Another Surface, called scaled_surf, will reference whichever
        one of these Surfaces needs to be used; scaled_surf will be
        the one that is actually drawn to the screen.
        """
        self.zoom_one_surf = Surface((SCREEN_SIZE[0], SCREEN_SIZE[1]))
        self.zoom_two_surf = Surface((SCREEN_SIZE[0] * 2,
                                      SCREEN_SIZE[1] * 2))
        self.zoom_three_surf = Surface((SCREEN_SIZE[0] * 3,
                                        SCREEN_SIZE[1] * 3))
        self.scaled_surf = self.zoom_one_surf

    # Support
    def create_state_by_id(self, state_id):
        """Initialize a new Game State and return it.

        Args:
            state_id: An integer for the ID of the new State, according to
                the StateIDs enum; view the enum itself for possible values.
        """
        if state_id == StateIDs.TITLE:
            return TitleState(self, self.state_pass)
        elif state_id == StateIDs.SETTINGS:
            return SettingsState(self, self.state_pass)
        # More will be added as new States are created.

    # Game Processing
    def change_state(self, next_state_id):
        """Pop the currently-active State from the stack and push a new State
        on top in its place.

        Game processing will immediately switch to this new State.

        Args:
            next_state_id: An integer for the ID of the new State, according to
                the StateIDs enum; view the enum itself for possible values.
        """
        self.active_state_list.pop()
        self.push_state(next_state_id)
    
    def push_state(self, next_state_id):
        """Push a another State onto the stack and switch processing to it.

        Args:
            next_state_id: An integer for the ID of the new State, according to
                the StateIDs enum; view the enum itself for possible values.
        """
        new_state = self.create_state_by_id(StateIDs.TITLE)
        self.active_state_stack.append(new_state)

    def pop_top_state(self):
        """Pop the currently-active State off the top of the stack and switch
        processing to the State underneath it.
        """
        self.active_state_stack.pop()

    def scale_screen(self, scale):
        """Resize the screen whenever the screen scale changes.

        Keyword arguments:
            scale: The magnification rate.
        """
        scaled_size = (SCREEN_SIZE[0] * scale,
                    SCREEN_SIZE[1] * scale)

        if self.screen.get_size() != scaled_size:
            if scale == FULL_SCALE:
                self.screen = pygame.display.set_mode(scaled_size,
                                                      pygame.FULLSCREEN |
                                                      pygame.HWSURFACE)
            else:
                self.screen = pygame.display.set_mode(scaled_size, 0)

    def scale_surface(self, surf, scale):
        """Magnify the specified Surface according to the specified
       magnification rate and draw it onto the appropriately-scaled
       Surface.

        Args:
            surf: The Surface to resize.
            scale: An integer for the magnification rate.
        """
        new_size = (SCREEN_SIZE[0] * scale,
                    SCREEN_SIZE[1] * scale)

        if scale == 1:
            self.scaled_surf = self.zoom_one_surf
        elif scale == 2:
            self.scaled_surf = self.zoom_two_surf
        else:
            self.scaled_surf = self.zoom_three_surf

        scaled_surf = pygame.transform.scale(surf, new_size,
                                             self.scaled_surf)

    def get_visible_states(self):
        """Determine which States on the stack are currently visible
        on-screen.

        Returns:
            A tuple containing the Game States that are both active and
            visible.
        """
        visible_states = []
        screen_is_covered = False
        
        for game_state in reversed(self.active_state_list):
            if not screen_is_covered:
                visible_states.append()
                
                if (game_state.exact_offset[0] == 0.0 and
                   game_state.exact_offset[1] == 0.0):
                    screen_is_covered = True

        return tuple(visible_states)

    def update_state(self, updated_state, seconds):
        """Update the specified State.

        Args:
            updated_state: The State that will be updated.
            seconds: A float for the amount of seconds elapsed since the last
                update.
        """
        updated_state.update_state(seconds)

    def draw_background(self):
        """Draw a black background underneath all States.
        This will keep the screen from being blank, which can reduce
        the likelihood of strange graphical glitches.
        """
        pygame.draw.rect(self.screen, (0, 0, 0),
                         Rect(0, 0, SCREEN_SIZE[0], SCREEN_SIZE[1]))

    def draw_state(self, drawn_state):
        """Draw the specified state's surface onto the screen and
        update the screen as a whole.

        The State Surface will also be scaled according to screen_scale
        within state_pass.

        Args:
            drawn_state: The State that will be drawn.
        """
        scale = self.state_pass.settings.screen_scale

        self.scale_surface(drawn_state.state_surface, scale)
        self.screen.blit(self.scaled_surf, drawn_state.screen_offset())

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
            milliseconds = self.clock.tick(FRAME_RATE)
            seconds = milliseconds / 1000.0
            
            visible_states = self.get_visible_states()
            for game_state in visible_states:
                self.update_state(game_state)

            self.scale_screen(self.state_pass.settings.screen_scale)
            self.draw_background()
            for game_state in visible_states:
                self.draw_state(game_state)
            pygame.display.update()

            sleep_time = (1000.0 / FRAME_RATE) - milliseconds
            if sleep_time > 0.0:
                pygame.time.wait(int(sleep_time))
            else:
                pygame.time.wait(1)
