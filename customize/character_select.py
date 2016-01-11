"""This module contains constants that affect the operation of the game's
Character Select Screen.

Module Constants:
    FONT_PATH: A String for the file path to the font used for rendering
        the text on this screen.
    FONT_SIZE: An integer for the size of most text on this screen.
    VS_SIZE: An integer for the size of the VS text.
    VS_COLOR: A tuple of three integers, representing the RGB color of
        the VS text.
    VS_OUTLINE_TEXT: A tuple of three integers, representing the RGB
        color of the VS text's outline.
    VS_POSITION: A tuple of two integers, for the x and y-positions
        of the VS text relative to the screen.
    NO_CHARS_COLOR:
    NO_CHARS_POSITION: A tuple of two integers for the x and y-positions
        of the 'No Characters' text, relative to the screen.
    SPEED_OF_LINES: An integer for the speed, in pixels per second, at
        which the background lines will scroll across the screen.
    SPEED_OF_ROSTER: An integer for the speed, in pixels per second, at
        which the roster display will slide at.
    SPEED_OF_VS: An integer for the speed, in pixels per second, of the
        wipe in and wipe out effect on the VS text.
    MUSIC_PATH: A String for the file path to the Character Select
        Screen and Stage Select Screen music.
    VOICE_PATH: A String for the file path to the announcer voice clip.
    MUSIC_FADEOUT_TIME: An integer for the time taken, in
            milliseconds, to fade out the Select Screen music.
    PROMPT_Y: An integer for the y-position of the prompt relative to the
        screen.
    FLASH_RATE: An integer for the amount of time elapsed, in update
        cycles, between toggling the visibility of the prompt text.
    P1_TEXT: A String for the text that will be displayed as player
        1's prompt message.
    P2_TEXT: A String for the text that will be displayed as player
        2's prompt message.
    P1_COLOR: A tuple of three integers, representing the RGB value
        for player 1's prompt text.
    P2_COLOR: A tuple of three integers, representing the RGB value
        for player 2's prompt text.
    LINE_COLOR: A tuple three integers, representing the RGB color
        used in drawing all of the lines.
    LINE_Y_COORDS: A tuple of integers, each of which represent one
        of the lines' y-position relative to the screen.
    LINE_WIDTHS: A tuple of integers, each of which represent the
        width of one of the lines, in pixels.
        Note that this is in the same order as LINE_Y_COORDS. For
        example, if the first value in LINE_Y_COORS is 50 and the
        first value in LINE_WIDTHS is 5, a line with a width of 5
        pixels will be drawn at a y-position of 50.
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
    P1_SPRITESHEET: A String for the file path to player 1's cursor
        animation.
    P2_SPRITESHEET: A String for the file path to player 2's cursor
        animation.
    CURSOR_FRAME_AMOUNT: An integer for the amount of frames in each
        cursor animation.
    CURSOR_FRAME_DURATION: An integer for the duration, in update
        cycles, of each frame in each cursor animation.
    ARROW_SPRITESHEET: A String for the file path to the roster scroll
        arrow's animation spritesheet.
    ARROW_FRAME_AMOUNT: An integer for the number of frames in the
        roster scroll arrow animation.
    ARROW_FRAME_DURATION: An integer for the duration, in update cycles,
        of each frame in the roster scroll arrow animation.
    ARROW_ROSTER_DISTANCE: An integer for the distance, in pixels, of
        the roster scroll arrow from the edge of the roster.
    GROUND_Y: An integer for the y-position of the ground upon which
        a character will be standing, relative to the screen.
    NAME_COLOR: A tuple containing the RGB values for a character name
        text's color.
    NAME_OUTLINE_COLOR: A tuple containing the RGB values for the color
        of a character name text's outline.
    NAME_OFFSET: An integer for the vertical shift up, in pixels, of a
        character name text from the bottom of the character sprite.
    SHADOW_HEIGHT: An integer for the height of a character's shadow,
        in pixels.
    SHADOW_COLOR: A tuple containing the RGB values for the color of a
        character's shadow.
    OFFSET_FROM_SHADOW: An integer for the distance, in pixels, from the
        bottom edge of a character sprite to the vertical center of
        their shadow.
    PREVIEW_SLIDE_DURATION: A float for the the time taken, in seconds,
        to move a character preview into position during the intro and
        outro animations.
"""


FONT_PATH = 'fonts/fighting-spirit-TBS.ttf'
FONT_SIZE = 16
VS_SIZE = 28
VS_COLOR = (255, 255, 255)
VS_OUTLINE_COLOR = (80, 80, 80)
VS_POSITION = (167, 80)
NO_CHARS_COLOR = (255, 255, 255)
NO_CHARS_POSITION = (40, 78)
SPEED_OF_LINES = 500
SPEED_OF_ROSTER = 150
SPEED_OF_VS = 120
MUSIC_PATH = 'audio/select-theme.wav'
VOICE_PATH = 'audio/announcer-character_select.wav'
MUSIC_FADEOUT_TIME = 2000
PROMPT_Y = 13
FLASH_RATE = 30
P1_TEXT = 'P1 Select'
P2_TEXT = 'P2 Select'
P1_COLOR = (255, 0, 0)
P2_COLOR = (0, 255, 255)
LINE_COLOR = (0, 19, 127)
LINE_Y_COORDS = (11, 26, 59, 95, 151)
LINE_WIDTHS = (3, 9, 7, 5, 17)
MUGSHOT_SIZE = 50
SLOTS_PER_ROW = 5
FRAME_THICKNESS = 2
FRAME_COLOR = (102, 102, 102)
BACKGROUND_COLOR = (255, 255, 255)
ARROW_DISTANCE = 11
P1_SPRITESHEET = 'images/p1_character_cursor.png'
P2_SPRITESHEET = 'images/p2_character_cursor.png'
CURSOR_FRAME_AMOUNT = 2
CURSOR_FRAME_DURATION = 8
ARROW_SPRITESHEET = 'images/roster_up_arrow.png'
ARROW_FRAME_AMOUNT = 2
ARROW_FRAME_DURATION = 10
ARROW_ROSTER_DISTANCE = 18
GROUND_Y = 157
NAME_COLOR = (255, 255, 255)
NAME_OUTLINE_COLOR = (80, 80, 80)
NAME_OFFSET = 6
SHADOW_HEIGHT = 14
SHADOW_COLOR = (0, 5, 90)
OFFSET_FROM_SHADOW = 4
PREVIEW_SLIDE_DURATION = 0.4
