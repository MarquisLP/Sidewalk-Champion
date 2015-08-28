import sys
from threading import Thread
from pygame.locals import *
from lib.globals import *
from lib.custom_data.settings_manager import load_settings
from lib.game_states.state import *
from lib.game_states.state_ids import StateIDs
from lib.game_states.title_state import TitleState
from lib.game_states.settings_state import SettingsState
from lib.game_states.character_select_state import CharacterSelectState
from lib.game_states.stage_select_state import StageSelectState

class GameStateManager(object):
    """This class runs the main game loop and updates the appropriate
    Game State.

    These Game States include: Title Screen, Settings, Selecting
    Characters, Selecting Stage, and Battle.
    Game processing works by switching between States and passing
    data between them.

    Attributes:
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
        next_state: A Game State object that is currently being initialized; it
            will be added to the top of the State stack and begin running once
            it is finished initializing.
            A value of None means that there is no Game State currently being
            prepared.
        init_state_thread: A Thread that handles initialization of new Game
            States concurrently to the main game thread.
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
    def __init__(self):
        """Initialize instance variables."""
        settings = load_settings()

        self.screen = self.create_screen(settings)
        self.prepare_screen()
        self.clock = pygame.time.Clock()
        self.state_pass = StatePass(settings)
        self.active_state_stack = [self.create_state_by_id(StateIDs.TITLE)]
        self.next_state = None
        self.init_state_thread = Thread()
        self.zoom_one_surf = Surface((SCREEN_SIZE[0],
                                      SCREEN_SIZE[1])).convert()
        self.zoom_two_surf = Surface((SCREEN_SIZE[0] * 2,
                                      SCREEN_SIZE[1] * 2)).convert()
        self.zoom_three_surf = Surface((SCREEN_SIZE[0] * 3,
                                        SCREEN_SIZE[1] * 3)).convert()
        self.scaled_surf = self.zoom_one_surf

    def create_screen(self, settings_data):
        """Return the Surface that will be used as the game screen.

        Args:
            settings_data: A SettingsData object for various options
                that can be set by the players via the Settings screen.
        """
        display_flags = 0
        if settings_data.screen_scale == FULL_SCALE:
            display_flags = pygame.FULLSCREEN | pygame.HWSURFACE

        screen = pygame.display.set_mode(
            (SCREEN_SIZE[0] * settings_data.screen_scale,
            SCREEN_SIZE[1] * settings_data.screen_scale), display_flags)

        return screen

    def prepare_screen(self):
        """Perform additional operations to initialize the game
        window display.
        """
        pygame.display.set_caption('Sidewalk Champion')
        pygame.mouse.set_visible(False)

    # Support
    def create_state_by_id(self, state_id):
        """Initialize a new Game State and return it.

        Args:
            state_id: An integer for the ID of the next State, according to
                the StateIDs enum; view the enum itself for possible values.
        """
        if state_id == StateIDs.TITLE:
            return TitleState(self, self.state_pass)
        elif state_id == StateIDs.SETTINGS:
            return SettingsState(self, self.state_pass)
        elif state_id == StateIDs.SELECT_CHARACTER:
            return CharacterSelectState(self, self.state_pass)
        elif state_id == StateIDs.SELECT_STAGE:
            return StageSelectState(self, self.state_pass)
        else:
            self.force_quit('The Game State of ID number ' + str(state_id) +
                            ' does not currently exist.')
        # More will be added as new States are created.

    def force_quit(self, message=None):
        """Force the program to terminate and display an optional
        message.

        Keyword Arguments:
            message: Optional. A String message that will be printed to
                 the console, usually for detailing an error.
        """
        if message is not None:
            print message
        pygame.event.post(pygame.event.Event(QUIT, {}))

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
        pygame.transform.scale(surf, new_size, self.scaled_surf)

        # Scaling causes the alpha value of the Surface to be lost,
        # so scaled_surf's alpha value will have to be explicitly set
        # to match the original transparency of the surf.
        self.match_surface_alpha(surf)

    def match_surface_alpha(self, surf):
        """Match the alpha transparency of the scaled Surface currently in use
        with that of another Surface.

        Args:
            surf: The Surface whose alpha value will be used as reference.
        """
        if self.scaled_surf.get_alpha() != surf.get_alpha():
            self.scaled_surf.set_alpha(surf.get_alpha())

    def is_loading_next_state(self):
        """Return a Boolean indicating whether the next Game State is currently
        being prepared to run next.
        """
        if self.init_state_thread.is_alive():
            return True
        else:
            return False

    def get_visible_states(self):
        """Determine which States on the stack are currently visible
        on-screen.

        Returns:
            A tuple containing the Game States that are both active and
            visible, in order from bottom to top of the stack.
        """
        visible_states = []
        screen_is_covered = False

        for game_state in reversed(self.active_state_stack):
            if not screen_is_covered:
                visible_states.append(game_state)

                if (game_state.exact_offset[0] == 0.0 and
                   game_state.exact_offset[1] == 0.0):
                    screen_is_covered = True

        visible_states.reverse()
        return tuple(visible_states)

    # Stack Management
    def pop_top_state(self):
        """Pop the currently-active State off the top of the stack and switch
        processing to the State underneath it.
        """
        self.active_state_stack.pop()

    def change_state(self, next_state_id):
        """Pop the currently-active State from the stack and push a new State
        on top in its place.

        Game processing will immediately switch to this new State.

        Args:
            next_state_id: An integer for the ID of the new State, according to
                the StateIDs enum; view the enum itself for possible values.
        """
        self.pop_top_state()
        self.push_state(next_state_id)

    def push_state(self, next_state_id):
        """Prepare the next active Game State and push it to the top of the
        State stack once it is finished initializing.

        Args:
            next_state_id: An integer for the ID of the new State, according to
                the StateIDs enum; view the enum itself for possible values.
        """
        self.init_state_thread = Thread(target=self.prepare_next_state,
                                        args=(next_state_id,))
        self.init_state_thread.start()

    def prepare_next_state(self, next_state_id):
        """Create a new Game State and store it as the next State to be run.

        Args:
            next_state_id: An integer for the ID of the new State, according to
                the StateIDs enum; view the enum itself for possible values.
        """
        self.next_state = self.create_state_by_id(next_state_id)

    def run_next_state(self):
        """Add the newly-prepared Game State to the top of the State stack and
        switch game processing to that State.
        """
        self.active_state_stack.append(self.next_state)
        self.next_state = None

    # Game Processing
    def handle_events(self):
        """Handle all PyGame events that are currently polled."""
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN and not self.is_loading_next_state():
                active_state = self.active_state_stack[-1]
                if active_state.is_accepting_input:
                    active_state.get_player_input(event)

    def update_visible_states(self, seconds):
        """Update all Game States currently visible on-screen.

        Args:
            seconds: A float for the time elapsed, in seconds, since the
            last update cycle.
        """
        for visible_state in self.get_visible_states():
            visible_state.update_state(seconds)

    def update_game_visuals(self):
        """Update the entire game display."""
        self.scale_screen(self.state_pass.settings.screen_scale)
        self.draw_background()
        for visible_state in self.get_visible_states():
            self.draw_state(visible_state)
        pygame.display.update()

    def draw_background(self):
        """Draw a black background underneath all States.
        This will keep the screen from being blank, which can reduce
        the likelihood of strange graphical glitches.
        """
        scale = self.state_pass.settings.screen_scale
        pygame.draw.rect(self.screen, (0, 0, 0),
                         Rect(0, 0, SCREEN_SIZE[0] * scale,
                              SCREEN_SIZE[1] * scale))

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

    def sleep_between_cycles(self, milliseconds):
        """If there is time remaining between game update cycles,
        allow the program to sleep during that time.

        This will free up a significant amount of CPU usage whenever
        possible.

        Args:
            milliseconds: A float for the time elapsed, in milliseconds,
                since the last update cycle.
        """
        sleep_time = (1000.0 / FRAME_RATE) - milliseconds
        if sleep_time > 0.0:
            pygame.time.wait(int(sleep_time))
        else:
            pygame.time.wait(1)

    def run_game(self):
        """Run the main game loop."""
        while True:
            # Update processes after a passage of time equal to the
            # global frame rate.
            milliseconds = self.clock.tick(FRAME_RATE)
            seconds = milliseconds / 1000.0

            if self.next_state is not None:
                self.run_next_state()
            self.handle_events()
            self.update_visible_states(seconds)
            self.update_game_visuals()
            self.sleep_between_cycles(milliseconds)

