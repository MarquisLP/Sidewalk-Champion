"""This module contains values that affect the operation of the game's
Title Screen.

Module Constants:
    BG_PATH: A String for the file path to the background image's
            sprite sheet.
    BG_FRAMES: An integer greater than 0 for the amount of animation
        frames in the background image's sprite sheet.
    BG_DURATION: An integer greater than 0 for the duration of each
        frame in the background image's animation, in update cycles.
    LOGO_PATH: A String for the file path to the game logo's sprite
        sheet.
    LOGO_X: An integer for the game logo's x-position relative to
        the screen.
    LOGO_Y: an integer for the game logo's y-position relative to
        the screen.
    LOGO_FRAMES: An integer greater than 0 for the amount of animation
        frames in the game logo's sprite sheet.
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
    BG_OFFSET: A float for the distance of the background from the
        bottom of the screen, in pixels, when the animation starts.
    BG_SCROLL_SPEED: A float for the speed, in pixels per second,
        at which the background will be scrolled up.
    VOICE_PATH: A String for the file path of the voice clip where
        the announcer states the title of the game.
    FADE_DELAY: An integer for the alpha value that the logo
        Animation must attain before the voice clip is played.
    MUSIC_PATH: A String for the file path of the title theme.
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
    START_X: An integer for the x-position of the prompt relative to the
        screen.
    START_Y: An integer for the y-position of the prompt relative to the
        screen.
    START_PROMPT_TEXT: A String for the message prompt that will be displayed
        when waiting for the start button to be pressed.
    START_WAIT_SPEED_FLASH: An integer for the speed of the prompt's
        flash, in update cycles, while it is waiting for the
        players' input.
    MAIN_OPTIONS_X: The x-position of the main Options (Battle, Training,
        Settings, Exit) relative to the screen.
    MAIN_OPTIONS_Y: The y-position of the top main Option relative to the
        screen.
    BATTLE_X: The x-position of the first BattleSetting relative to the
        screen.
    BATTLE_Y: The y-position of the first BattleSetting relative to the
        screen.
    OPTION_NORMAL_COLOR: A tuple of ints for the RGB values for the regular
        color of an Option.
    OPTION_HIGHLIGHT_COLOR: A tuple of ints for the RGB values of an
        Option's color when it is selected by the users.
    OPTION_FONT_PATH: A String for the file path to the font file that
        will be used in rendering graphical text for Options.
    OPTION_FONT_SIZE: An integer size for the font used in rendering Option
        text.
    VALUE_X: The integer coordinate for the x-position of value
        text relative to the screen.
    LEFT_ARROW_PATH: A String for the file path to the scroll left
        arrow image.
    ARROW_DISTANCE: An integer for the horizontal distance between
        each scroll arrow and the text for the selected value.
    ARROW_Y_OFFSET: The integer distance, in pixels, between the
        the top of the text graphic and the top of each scroll
        arrow.
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
BG_OFFSET = 50.0
BG_SCROLL_SPEED = 70.0
FADE_LOGO_RATE = 7
VOICE_PATH = 'audio/announcer-title.wav'
FADE_DELAY = 7
MUSIC_PATH = 'audio/title_theme.wav'
OPTION_DISTANCE = 8
CONFIRM_DURATION = 60
TEXT_FLASH_SPEED = 5
TEXT_SLIDE_SPEED = 800
START_X = 135
START_Y = 150
START_PROMPT_TEXT = 'Press Start'
START_WAIT_FLASH_SPEED = 45
MAIN_OPTIONS_X = 155
MAIN_OPTIONS_Y = 104
BATTLE_X = 130
BATTLE_Y = 117
OPTION_NORMAL_COLOR = (169, 169, 169)
OPTION_HIGHLIGHT_COLOR = (255, 255, 255)
OPTION_FONT_PATH = 'fonts/fighting-spirit-TBS.ttf'
OPTION_FONT_SIZE = 18
VALUE_DISTANCE = 118
LEFT_ARROW_PATH = 'images/battle_setup_arrow_left.png'
ARROW_DISTANCE = 7
ARROW_Y_OFFSET = 5
