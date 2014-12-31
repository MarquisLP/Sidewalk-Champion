"""This module contains all of the necessary PyGame components for
running a simplified game loop. Use it for test cases on classes and
their methods.

Game State classes (that is, subclasses of the State class from the
state.py module) normally don't need to make use this script, as they
can be tested directly from the GameStateManager.
As such, this script will mostly be useful in testing component classes
within the States themselves.
"""
import sys
import pygame
from pygame.locals import *
from lib.globals import SCREEN_SIZE
from lib.globals import FRAME_RATE
# Import additional modules here.


def pygame_modules_have_loaded():
    success = True

    if not pygame.display.get_init:
        success = False
    if not pygame.font.get_init():
        success = False
    if not pygame.mixer.get_init():
        success = False

    return success


pygame.init()
pygame.font.init()
pygame.mixer.init(44100)

if pygame_modules_have_loaded():
    game_screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption('Test')
    clock = pygame.time.Clock()
    timer_rate = int((1.0 / FRAME_RATE) * 1000)
    pygame.time.set_timer(USEREVENT, timer_rate)
    
    # The class(es) that will be tested should be declared and initialized
    # here in the global scope.
    # Yes, globals are evil, but for a confined test script they will make
    # everything much easier. This way, you can access the class(es) from all
    # three of the methods provided below.

    def prepare_test():
        # Add in any code that needs to be run before the game loop starts.
        pass

    def handle_input(key_name):
        # Add in code for input handling.
        # key_name provides the String name of the key that was pressed.
        pass

    def update(screen, time):
        # Add in code to be run during each update cycle.
        # screen provides the PyGame Surface for the game window.
        # time provides the seconds elapsed since the last update.
        pygame.display.update()

    # Add additional methods here.

    def main():
        prepare_test()

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == KEYDOWN:
                    key_name = pygame.key.name(event.key)
                    handle_input(key_name)

                if event.type == USEREVENT:
                    milliseconds = clock.tick()
                    seconds = milliseconds / 1000.0
                    update(game_screen, seconds)

    main()
