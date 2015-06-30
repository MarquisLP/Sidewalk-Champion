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
import pygame.draw
from lib.graphics import Graphic
from pygame.surface import Surface
from pygame.rect import Rect


BORDER_WIDTH = 2
TOP_THUMB_Y = 34
THUMB_X = 302
THUMB_SIZE = 50
THUMB_BORDER_COLOR = (102, 102, 102)
THUMB_HIGHLIGHT_COLOR = (192, 0, 255)
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


class StageThumbnail(Graphic):
    """A small icon for a Stage that can be selected by the players.
    """
    def __init__(self, thumbnail_image, y):
        """Declare and initialize instance variables.
    
        Args:
            thumbnail_image (Surface): The Stage's icon image.
            y (int): The thumbnail's y-position on-screen.
        """
        position = (THUMB_X, y)
        super(StageThumbnail, self).__init__(thumbnail_image, position)
        self.add_border()

    def add_border(self):
        """Draw a border around the thumbnail image Surface."""
        new_surf = Surface((THUMB_SIZE + (BORDER_WIDTH * 2),
                            THUMB_SIZE + (BORDER_WIDTH * 2)))
        new_surf.blit(self.image, (BORDER_WIDTH, BORDER_WIDTH))
        border_rect = Rect(0, 0, new_surf.get_width() - 1,
                           new_surf.get_height() - 1)
        pygame.draw.rect(new_surf, THUMB_BORDER_COLOR, border_rect, 
                         BORDER_WIDTH)
        self.image = new_surf

    def change_stage(self, new_image):
        """Change the icon image to represent a different Stage.

        Args:
            new_image (Surface): The new Stage icon to display.
        """
        self.image.blit(new_image, (BORDER_WIDTH, BORDER_WIDTH))

    def change_border(self, color):
        """Redraw the border with a specific color.

        Args:
            color (tuple of int, int, int): The RGB values for the new
                border color.
        """
        border_rect = Rect(0, 0, self.image.get_width() - 1,
                           self.image.get_height() - 1)
        pygame.draw.rect(self.image, color, border_rect, BORDER_WIDTH)

    def highlight(self):
        """Recolor the border to show that the thumbnail is selected."""
        self.change_border(THUMB_HIGHLIGHT_COLOR)

    def unhighlight(self):
        """Recolor the border to show the thumbnail deselected."""
        self.change_border(THUMB_BORDER_COLOR)
