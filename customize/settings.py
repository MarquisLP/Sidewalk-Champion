'''This module contains values that affect the operation of the game's
Settings Screen.

Module Constants:
    BG_PATH: A string containing the file path for the background image.
    SLIDE_SFX_PATH: A string containing the file path for the slide-in
        sound effect.
    SCROLL_SFX_PATH: A string containing the file path for the scroll list
        sound effect.
    EXIT_SFX_PATH: A string containing the file path for the exit screen
        sound effect.
    SLIDE_SPEED: An integer that sets the speed at which the State Surface
        will slide, in pixels per second.
    SETTING_LIST_X: The x-position of the top of the list relative to the game
        screen.
    SETTING_LIST_Y: The y-position of the top of the list relative to the game
        screen.
    SETTING_DISTANCE: The vertical distance between Setting text
        graphics, in pixels.
    OPTION_DISTANCE: The horizontal distance, in pixels, between each of the
        text graphics for options.
    OPTION_X: The x-coordinate for a Setting's first Option, relative to the
        Setting Surface.
    BINDING_LIST_X: The x-position of the Key Binding List's Surface,
        relative to the
        parent Surface.
    BINDING_LIST_Y: The y-position of the Key Binding List's Surface,
        relative to the parent Surface.
    REMAP_SFX_PATH: A string containing the file path for the
        key remap sound effect.
    INVALID_SFX_PATH: A string containing the file path for the
        invalid key sound effect.
    BINDING_TEXT_DISTANCE   The vertical distance, in pixels, between
        the top edges of the text graphic for each Key Binding.
    BINDINGS_ON_SCREEN: The number of key bindings that will be shown
        on-screen at any one time.
    UP_ARROW_PATH   The filepath for the scroll up arrow sprite sheet.
    DOWN_ARROW_PATH The filepath for the scroll down arrow sprite sheet.
    ARROW_X: The x-position of both arrows on the Key Binding List's
        Surface.
    UP_ARROW_Y: The y-position of the up arrow on the Key Binding List's
        Surface.
    DOWN_ARROW_Y: The y-position of the down arrow on the Key Binding List's
        Surface.
    ARROW_FRAMES    The number of frames in the scroll arrows' sprite sheets.
    ARROW_DURATION  The duration of each frame in the scroll arrows'
        animations, in pixels per second.
    KEY_TEXT_X: The x-position of the text for a keyboard key's name.
    FONT_PATH: The filepath to the font used for rendering
        underlineable text.
    FONT_COLOUR: A tuple containing the RGB values for the color of
        underlineable text.
    FONT_SIZE: The size of the font used for rendering underlineable text.
    UNDERLINE_COLOUR: A tuple containing the RGB values for the underline
        color.
    UNDERLINE_SIZE  The height of the underline, in pixels.
'''


BG_PATH = "images/settings_back.png"
SLIDE_SFX_PATH = "audio/settings_slide.wav"
SCROLL_SFX_PATH = "audio/scroll.wav"
EXIT_SFX_PATH = "audio/cancel.wav"
SLIDE_SPEED = 1000.0
SETTING_LIST_X = 21
SETTING_LIST_Y = 17
SETTING_DISTANCE = 15
OPTION_DISTANCE = 20
OPTION_X = 200
BINDING_LIST_X = 52
BINDING_LIST_Y = 115
REMAP_SFX_PATH = "audio/settings_remap.wav"
INVALID_SFX_PATH = "audio/invalid.wav"
BINDING_TEXT_DISTANCE = 23
BINDINGS_ON_SCREEN = 4
UP_ARROW_PATH = "images/settings_arrow_up.png"
DOWN_ARROW_PATH = "images/settings_arrow_down.png"
ARROW_X = 125.0
UP_ARROW_Y = 0.0
DOWN_ARROW_Y = 86.0
ARROW_FRAMES = 2
ARROW_DURATION = 10
KEY_TEXT_X = 175
FONT_PATH = "fonts/corbel.ttf"
FONT_COLOUR = (255, 255, 255)
FONT_SIZE = 16
UNDERLINE_COLOUR = (136, 136, 136)
UNDERLINE_SIZE = 4
