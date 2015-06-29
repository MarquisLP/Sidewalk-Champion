"""This module handles the Stage Select Screen and all of its various
components.

Module Constants:
    BORDER_WIDTH (int): The thickness, in pixels, of the borders of
        the stage preview as well as each stage thumbnail.
    TOP_THUMB_Y (int): The y-position of the top-most thumbnail
        on-screen.
    THUMB_X (int): The shared x-position of all thumbnails on-screen.
    THUMB_SIZE (int): The width and height, in pixels, of each thumbnail
        image.
    THUMB_BORDER_COLOR (tuple of int): The RGB values for the color of 
        the thumbnail border.
    THUMB_HIGHLIGHT_COLOR (tuple of int): The RGB values for the color
        of the thumbnail border when a particular thumbnail is selected.
    PREVIEW_X (int): The x-position of the stage preview on-screen.
    PREVIEW_Y (int): The y-position of the stage preview on-screen.
    PREVIEW_WIDTH (int): The width, in pixels, of the stage preview.
    PREVIEW_HEIGHT (int): The height, in pixels, of the stage preview.
    PREVIEW_OUTER_BORDER_COLOR (tuple): The RGB values for the color of
        the outermost preview border.
    PREVIEW_INNER_BORDER_COLOR (tuple): The RGB values for the color of
        the innermost preview border.
    LINE_WIDTHS (tuple of int): The respective widths, in pixels, of
        each BackgroundLine.
    LINE_SPEED (int): The speed, in pixels per second, at which the
        BackgroundLines travel and bounce horizontally.
    LINE_LEFT_BOUND (int): The on-screen x-position of the furthest left
        that the BackgroundLines can travel.
    LINE_RIGHT_BOUND (int): The on-screen x-position of the furthest 
        right that the BackgroundLines can travel.
    TRANSITION_SLIDE_SPEED (int): The speed, in pixels per second, that
        Graphics move in and out of the screen at when transitioning in
        or out of this State.
"""


BORDER_WIDTH = 2
TOP_THUMB_Y = 34
THUMB_X = 302
THUMB_SIZE = 50
THUMB_BORDER_COLOR = (192, 192, 192)
THUMB_HIGHLIGHT_COLOR = (192, 0, 256)
PREVIEW_X = 14
PREVIEW_Y = 11
PREVIEW_WIDTH = 245
PREVIEW_HEIGHT = 130
PREVIEW_INNER_BORDER_COLOR = (0, 7, 51)
PREVIEW_OUTER_BORDER_COLOR = (0, 19, 127)
LINE_WIDTHS = (4, 3, 16, 6, 9)
LINE_COLOR = (0, 19, 127)
LINE_SPEED = 500
LINE_LEFT_BOUND = 292
LINE_RIGHT_BOUND = 363
TRANSITION_SLIDE_SPEED = 500
