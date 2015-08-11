"""This module handles the Stage Select Screen and all of its various
components.

Module Constants:
    BORDER_WIDTH (int): The thickness, in pixels, of the borders of
        the stage preview as well as each stage thumbnail.
    NUM_OF_THUMBS (int): The number of Stage Thumbnails shown on the
        screen at once.
    THUMB_SIZE (int): The width and height, in pixels, of each thumbnail
        image.
    THUMB_BORDER_COLOR (tuple of int): The RGB values for the color of
        the thumbnail border.
    THUMB_HIGHLIGHT_COLOR (tuple of int): The RGB values for the color
        of the thumbnail border when a particular thumbnail is selected.
    PREVIEW_WIDTH (int): The width, in pixels, of the stage preview.
    PREVIEW_HEIGHT (int): The height, in pixels, of the stage preview.
    PREVIEW_OUTER_BORDER_COLOR (tuple): The RGB values for the color of
        the outermost preview border.
    PREVIEW_INNER_BORDER_COLOR (tuple): The RGB values for the color of
        the innermost preview border.
    LINE_WIDTHS (tuple of int): The respective widths, in pixels, of
        each BackgroundLine.
    LINE_COLOR (tuple of int): The RGB value for the color of the
        BackgroundLines.
    LINE_SPEED (int): The speed, in pixels per second, at which the
        BackgroundLines travel and bounce horizontally.
    LINE_LEFT_BOUND (int): The on-screen x-position of the furthest left
        that the BackgroundLines can travel.
    LINE_RIGHT_BOUND (int): The on-screen x-position of the furthest
        right that the BackgroundLines can travel.
    FONT_PATH (String): The file path to the font used for rendering
        the Stage name and subtitle text.
    NAME_SIZE (int): The font size used for rendering the Stage name
        text.
    SUBTITLE_SIZE (int): The font size used for rendering the Stage
        subtitle text.
    PREVIEW_TO_NAME_DISTANCE (int): The distance, in pixels, between
        the preview image and the Stage name text.
    SUBTITLE_TO_NAME_DISTANCE (int): The distance, in pixels, between
        the Stage name text and the Stage subtitle text.
    UP_ARROW_PATH (String): The file path to the scroll up arrow sprite
        sheet image.
    NUM_OF_ARROW_FRAMES (int): The number of frames in the scroll arrows'
        sprite sheet (as specified by UP_ARROW_PATH).
    ARROW_FRAME_DURATION (int): The duration, in update frames, of each
        animation frame for the scroll arrows.
    ARROW_DISTANCE_FROM_THUMBS (int): The vertical distance, in pixels,
        between the scroll arrows and the Thumbnails.
    THUMB_TO_ARROW_DISTANCE (int): The vertical distance, in pixels,
        between the Stage Thumbnails and the scroll arrows.
    TRANSITION_SLIDE_SPEED (int): The speed, in pixels per second, that
        Graphics move in and out of the screen at when transitioning in
        or out of this State.
"""
import pygame.draw
import pygame.image
from collections import namedtuple
from enum import IntEnum
from math import ceil
from random import randint
from lib.graphics import (Graphic, Animation, render_outlined_text,
                          get_line_center, calculate_center_position)
from lib.globals import SCREEN_SIZE
from lib.custom_data.stage_loader import load_all_stages
from lib.game_states.state import State
from pygame.surface import Surface
from pygame.rect import Rect


BORDER_WIDTH = 2
NUM_OF_THUMBS = 3
THUMB_SIZE = 50
THUMB_BORDER_COLOR = (102, 102, 102)
THUMB_HIGHLIGHT_COLOR = (192, 0, 255)
PREVIEW_WIDTH = 245
PREVIEW_HEIGHT = 130
PREVIEW_OUTER_BORDER_COLOR = (0, 7, 51)
PREVIEW_INNER_BORDER_COLOR = (0, 19, 127)
LINE_WIDTHS = (3, 4, 12, 6)
LINE_COLOR = (0, 19, 127)
LINE_SPEED = 200
LINE_LEFT_BOUND = 292
LINE_RIGHT_BOUND = 363
FONT_PATH = 'fonts/fighting-spirit-TBS.ttf'
NAME_SIZE = 20
SUBTITLE_SIZE = 12
PREVIEW_TO_NAME_DISTANCE = 14
NAME_TO_SUBTITLE_DISTANCE = 7
UP_ARROW_PATH = 'images/roster_up_arrow.png'
NUM_OF_ARROW_FRAMES = 2
ARROW_FRAME_DURATION = 10
THUMB_TO_ARROW_DISTANCE = 4
TRANSITION_SLIDE_SPEED = 500


StageMetadata = namedtuple('StageMetadata', 'name subtitle preview thumbnail')


class StageSelectState(State):
    """The screen where players can select the Stage that will serve as
    their battleground.

    Attributes:
        metadata (tuple of StageMetadata): This contains the names,
            subtitles, preview images, and thumbnail images of all
            Stages available in the game.
        thumbnails (tuple of Thumbnail): This contains Thumbnails
            representing every Stage within the game.
        preview (StagePreview): A snapshot of the Stage currently
            highlighted by the cursor.
        stage_name (Graphic): A line of text displaying the name of the
            currently-selected Stage.
        stage_subtitle (Graphic): A line of text displaying the subtitle
            of the currently-selected Stage.
        no_stages_text (Graphic): A line of text notifying the players
            that no Stages could be loaded into the game.
        bg_lines (tuple of BackgroundLine): A set of animated lines that
            will bounce around an area of the screen.
        scroll_up_arrow (Graphic): An arrow that will appear and nudge
            up to indicate that more Stages are available above the ones
            already on-screen.
        scroll_down_arrow (Graphic): An arrow that will appear and nudge
            down to indicate that more Stages are available below the
            ones already on-screen.
        transition (TransitionAnimation): An object that handles the
            intro and outro animations for this State.
        selected_stage (int): The index number within metadata for the
            Stage currently being selected.
        is_selection_confirmed (Boolean): Indicates whether the players
            have confirmed a Stage for battle. Set to False by default.
    """
    def __init__(self, state_manager, state_pass):
        """Declare and initialize instance variables.

        Args:
            state_manager (GameStateManager): The state manager object
                that possesses and executes this State.
            state_pass (StatePass): Contains all of the data passed
                between Game States.
        """
        super(StageSelectState, self).__init__(state_manager, state_pass)
        name_font = pygame.font.Font(FONT_PATH, NAME_SIZE)
        subtitle_font = pygame.font.Font(FONT_PATH, SUBTITLE_SIZE)

        self.state_manager = state_manager
        self.state_pass = state_pass
        self.bg_lines = self.create_bg_lines()
        self.scroll_up_arrow = Animation.from_file(UP_ARROW_PATH, (0, 0),
            NUM_OF_ARROW_FRAMES, ARROW_FRAME_DURATION)
        self.scroll_down_arrow = Animation.from_file(UP_ARROW_PATH, (0, 0),
            NUM_OF_ARROW_FRAMES, ARROW_FRAME_DURATION)
        self.scroll_down_arrow.flip(is_vertical=True)

        self.metadata = self.load_all_stage_metadata()
        if self.num_of_stages() <= 0:
            self.no_stages_text = render_outlined_text(name_font,
                'No Stages Loaded', (255, 255, 255), (0, 0, 0), (0, 0))
        else:
            self.stage_name = render_outlined_text(name_font,
                self.metadata[0].name, (255, 255, 255), (0, 0, 0), (0, 0))
            self.stage_subtitle = render_outlined_text(subtitle_font,
                self.metadata[0].subtitle, (255, 255, 255), (0, 0, 0), (0, 0))
            self.preview = StagePreview(self.metadata[0].preview,
                                        self.calculate_preview_y())
            self.thumbnails = self.create_thumbnails()
            self.thumbnails[0].highlight()

        self.align_text()
        self.align_scroll_arrows()

        self.selected_stage = 0
        self.is_selection_confirmed = False

    def load_all_stage_metadata(self):
        """Return a tuple containing StageMetadata namedtuples for all
        Stages loaded into the game.
        """
        all_stage_data = load_all_stages()

        metadata = []
        for stage_data in all_stage_data:
            name = stage_data.name
            subtitle = stage_data.subtitle
            preview = pygame.image.load(stage_data.preview)
            thumbnail = pygame.image.load(stage_data.thumbnail)
            metadata.append(StageMetadata(name, subtitle, preview, thumbnail))

        return tuple(metadata)

    def num_of_stages(self):
        """Return the integer amount of Stages loaded into the game."""
        return len(self.metadata)

    def create_thumbnails(self):
        """Return a tuple containing a number of Thumbnails depicting
        the first few Stages loaded into the game.

        The number of Thumbnails instantiated is determined by the
        NUM_OF_THUMBS constant.
        """
        thumbnails = []
        total_thumb_height = ((THUMB_SIZE * NUM_OF_THUMBS) +
                              (BORDER_WIDTH * (NUM_OF_THUMBS + 1)))
        y = calculate_center_position(0, SCREEN_SIZE[1], total_thumb_height)

        for stage_index in range(0, NUM_OF_THUMBS):
            if stage_index <= self.num_of_stages() - 1:
                image = self.metadata[stage_index].thumbnail
            else:
                # If less Stages were loaded than the amount specified by
                # NUM_OF_THUMBS, fill the remaining Thumbnails with white.
                image = Surface((THUMB_SIZE, THUMB_SIZE))
                pygame.draw.rect(image, (255, 255, 255),
                                 Rect(0, 0, THUMB_SIZE, THUMB_SIZE))

            new_thumbnail = StageThumbnail(image, y)
            thumbnails.append(new_thumbnail)

            y += THUMB_SIZE + BORDER_WIDTH

        return tuple(thumbnails)

    def create_bg_lines(self):
        """Return a tuple containing a number of BackgroundLines.

        The number of BackgroundLines created, as well as their
        inidividual widths, are specified by LINE_WIDTHS. Their
        individual positions are randomly generated between
        LINE_LEFT_BOUND and LINE_RIGHT_BOUND.
        """
        bg_lines = []
        is_moving_right = True

        for width in LINE_WIDTHS:
            x = randint(LINE_LEFT_BOUND, LINE_RIGHT_BOUND)
            new_line = BackgroundLine(x, width, is_moving_right)
            bg_lines.append(new_line)
            is_moving_right = not is_moving_right

        return bg_lines

    def align_text(self):
        """Position the text Graphics appropriately on the screen."""
        preview_y = self.calculate_preview_y()
        self.stage_name.rect.y = (preview_y + PREVIEW_HEIGHT +
                                  (BORDER_WIDTH * 2) +
                                  PREVIEW_TO_NAME_DISTANCE)
        self.stage_subtitle.rect.y = (self.stage_name.rect.y +
                                      self.stage_name.rect.height +
                                      NAME_TO_SUBTITLE_DISTANCE)
        self.center_info_text()

    def align_scroll_arrows(self):
        """Position the scroll arrows appropriately on the screen."""
        x = calculate_center_position(LINE_LEFT_BOUND,
            LINE_RIGHT_BOUND - LINE_LEFT_BOUND,
            self.scroll_up_arrow.rect.width // NUM_OF_ARROW_FRAMES)
        self.scroll_up_arrow.rect.x = x
        self.scroll_down_arrow.rect.x = x

        self.scroll_up_arrow.rect.y = (self.thumbnails[0].rect.y -
                                       THUMB_TO_ARROW_DISTANCE -
                                       self.scroll_up_arrow.rect.height)
        self.scroll_down_arrow.rect.y = (
            self.thumbnails[NUM_OF_THUMBS - 1].rect.y +
            THUMB_SIZE + (BORDER_WIDTH * 2) +
            THUMB_TO_ARROW_DISTANCE)

    def calculate_preview_y(self):
        """Return an integer for the y-position of the StagePreview,
        such that it and the info text will be centered vertically
        along the screen.
        """
        preview_and_text_height = (PREVIEW_HEIGHT + (BORDER_WIDTH * 2) +
            PREVIEW_TO_NAME_DISTANCE + self.stage_name.rect.height +
            NAME_TO_SUBTITLE_DISTANCE + self.stage_subtitle.rect.height)
        return calculate_center_position(0, SCREEN_SIZE[1],
                                         preview_and_text_height)

    def center_info_text(self):
        """Center the Stage name and subtitle texts horizontally within
        their allotted area.
        """
        area_width = SCREEN_SIZE[0] - (SCREEN_SIZE[0] - LINE_LEFT_BOUND)

        if self.num_of_stages() > 0:
            self.stage_name.rect.x = calculate_center_position(0, area_width,
                self.stage_name.rect.width)
            self.stage_subtitle.rect.x = calculate_center_position(0,
                area_width, self.stage_subtitle.rect.width)
        else:
            self.no_stages_text.rect.x = calculate_center_position(0,
                area_width, self.no_stages_text.rect.width)

    def get_player_input(self, event):
        """Read input from the players and respond to it.

        Args:
            event (Event): The PyGame KEYDOWN event. It stores the
                ASCII code for any keys that were pressed.
        """
        input_name = self.get_input_name(pygame.key.name(event.key))

        if self.num_of_stages() > 1:
            if input_name == 'up':
                self.change_selected_stage(CursorDirection.PREVIOUS)
            elif input_name == 'down':
                self.change_selected_stage(CursorDirection.NEXT)
            elif input_name == 'back':
                self.change_selected_stage(CursorDirection.PREVIOUS_ROW)
            elif input_name == 'forward':
                self.change_selected_stage(CursorDirection.NEXT_ROW)

    def get_input_name(self, key_name):
        """Get the name of the in-game input command based on the key
        that was presssed.

        Args:
            key_name (String): The name of the key that was pressed.

        Returns:
            The String name of the in-game input command.
            (e.g. 'forward', 'start', 'light punch')
            None will be returned if key_name does not match either of
            the players' key bindings.
        """
        for input_name in self.state_pass.settings.player1_keys:
            if key_name == self.state_pass.settings.player1_keys[input_name]:
                return input_name
        for input_name in self.state_pass.settings.player2_keys:
            if key_name == self.state_pass.settings.player2_keys[input_name]:
                return input_name

    def change_selected_stage(self, direction):
        """Select a different Stage and display its preview image,
        name, and subtitle.

        Args:
            direction (CursorDirection): An enum value that represents
                which Stage relative to the current one should be
                selected.
        """
        if direction == CursorDirection.PREVIOUS :
            if self.selected_stage > 0:
                self.selected_stage -= 1
            else:
                self.selected_stage = self.num_of_stages() - 1

        elif direction == CursorDirection.NEXT:
            if self.selected_stage < self.num_of_stages() - 1:
                self.selected_stage += 1
            else:
                self.selected_stage = 0

        elif direction == CursorDirection.PREVIOUS_ROW:
            if self.selected_stage <= 0:
                self.selected_stage = self.num_of_stages() - 1
            elif self.selected_stage % NUM_OF_THUMBS == 0:
                # If the top-most Thumbnail in the current row is selected,
                # move selection to the previous row.
                if self.selected_stage - NUM_OF_THUMBS >= 0:
                    self.selected_stage -= NUM_OF_THUMBS
                else:
                    self.selected_stage = 0
            else:
                # If selection is below the top of the current row, move
                # selection up to the top-most thumbnail of the current row.
                current_row = self.selected_stage // NUM_OF_THUMBS
                self.selected_stage = current_row * NUM_OF_THUMBS

        elif direction == CursorDirection.NEXT_ROW:
            if self.selected_stage >= self.num_of_stages() - 1:
                self.selected_stage = 0
            elif (self.selected_stage + 1) % NUM_OF_THUMBS == 0:
                # If the bottom-most Thumbnail in the current row is selected,
                # move selection to the next row.
                if self.selected_stage + NUM_OF_THUMBS < self.num_of_stages():
                    self.selected_stage += NUM_OF_THUMBS
                else:
                    self.selected_stage = self.num_of_stages() - 1
            else:
                # If selection is above the bottom of the current row, move
                # selection to the bottom-most thumbnail of the current row.
                if self.selected_stage + NUM_OF_THUMBS < self.num_of_stages():
                    next_row = (self.selected_stage // NUM_OF_THUMBS) + 1
                    self.selected_stage = (next_row * NUM_OF_THUMBS) - 1
                else:
                    # Or move selection to the very last Stage if selection
                    # was on the final row.
                    self.selected_stage = self.num_of_stages() - 1

        self.highlight_selected_thumbnail()
        self.update_thumbnail_images()
        self.preview.change_stage(self.metadata[self.selected_stage].preview)

    def highlight_selected_thumbnail(self):
        """Highlight the currently-selected StageThumbnail, and
        unhighlight the rest.
        """
        for thumbnail in self.thumbnails:
            thumbnail.unhighlight()
        self.thumbnails[self.selected_thumbnail()].highlight()

    def selected_thumbnail(self):
        """Return the integer index of the currently-selected
        StageThumbnail within self.thumbnails.
        """
        return (self.selected_stage - ((self.selected_stage // NUM_OF_THUMBS) *
                                       NUM_OF_THUMBS))

    def update_thumbnail_images(self):
        """Display the icon images for all Stages within range of the
        selected one on the StageThumbnails.
        """
        top_of_row = (self.selected_stage -
                      (self.selected_stage % NUM_OF_THUMBS))
        for thumb_index in range(0, NUM_OF_THUMBS):
            if top_of_row + thumb_index <= self.num_of_stages() - 1:
                stage_index = top_of_row + thumb_index
                image = self.metadata[stage_index].thumbnail
            else:
                # If the last row is currently selected and it has less
                # Stages than NUM_OF_THUMBS, fill the remaining Thumbnails
                # with white.
                image = Surface((THUMB_SIZE, THUMB_SIZE))
                pygame.draw.rect(image, (255, 255, 255),
                                 Rect(0, 0, THUMB_SIZE, THUMB_SIZE))
            # The new image is blitted onto the Thumbnail Surface,
            # rather than having the image replaced, in order to
            # keep the border.
            self.thumbnails[thumb_index].image.blit(image, (BORDER_WIDTH,
                                                            BORDER_WIDTH))

    def update_state(self, time):
        """Update all processes within the State.

        Args:
            time (float): The time, in seconds, elapsed since the last
                game update.
        """
        for line in self.bg_lines:
            line.update_movement(time)

        self.draw_state()

    def draw_state(self):
        """Draw all graphics within this State onto the screen."""
        pygame.draw.rect(self.state_surface, (0, 0, 0),
                         Rect(0, 0, SCREEN_SIZE[0], SCREEN_SIZE[1]))

        for line in self.bg_lines:
            line.draw(self.state_surface)

        # Draw the currently-selected Thumbnail last and on top,
        # so that its highlighted border is not covered by the others.
        for index in range(0, NUM_OF_THUMBS):
            if not index == self.selected_thumbnail():
                self.thumbnails[index].draw(self.state_surface)
        self.thumbnails[self.selected_thumbnail()].draw(self.state_surface)

        if self.num_of_stages() > 0:
            self.draw_scroll_arrows()
            self.preview.draw(self.state_surface)
            self.stage_name.draw(self.state_surface)
            self.stage_subtitle.draw(self.state_surface)
        else:
            self.no_stages_text.draw(self.state_surface)

    def draw_scroll_arrows(self):
        """If there are more Stages that can be selected beyond the
        ones shown on screen, draw the scroll arrows to indicate this.
        """
        if self.num_of_stages() > NUM_OF_THUMBS:
            current_row = self.selected_stage // NUM_OF_THUMBS
            max_row = self.num_of_stages() // NUM_OF_THUMBS

            if current_row > 0:
                self.scroll_up_arrow.draw(self.state_surface)
            if current_row < max_row:
                self.scroll_down_arrow.draw(self.state_surface)


class StageThumbnail(Graphic):
    """A small icon for a Stage that can be selected by the players.
    """
    def __init__(self, thumbnail_image, y):
        """Declare and initialize instance variables.

        Args:
            thumbnail_image (Surface): The Stage's icon image.
            y (int): The thumbnail's y-position on-screen.
        """
        x = calculate_center_position(LINE_LEFT_BOUND,
                                      LINE_RIGHT_BOUND - LINE_LEFT_BOUND,
                                      THUMB_SIZE + (BORDER_WIDTH * 2))

        super(StageThumbnail, self).__init__(thumbnail_image, (x, y))
        self.add_border()

    def add_border(self):
        """Draw a border around the thumbnail image Surface."""
        new_surf = Surface((THUMB_SIZE + (BORDER_WIDTH * 2),
                            THUMB_SIZE + (BORDER_WIDTH * 2)))
        new_surf.blit(self.image, (BORDER_WIDTH, BORDER_WIDTH))
        border_rect = Rect(get_line_center(BORDER_WIDTH),
                           get_line_center(BORDER_WIDTH),
                           THUMB_SIZE + BORDER_WIDTH + 1,
                           THUMB_SIZE + BORDER_WIDTH + 1)
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


class StagePreview(Graphic):
    """A snapshot of the currently-selected Stage."""
    def __init__(self, image, y):
        """Declare and initialize instance variables.

        Args:
            image (Surface): The snapshot image initially displayed.
            y (int): The y-coordinate for the top-left corner of the
                preview on the screen.
        """
        x = calculate_center_position(0,
            SCREEN_SIZE[0] - (SCREEN_SIZE[0] - LINE_LEFT_BOUND),
            PREVIEW_WIDTH + (BORDER_WIDTH * 4))

        super(StagePreview, self).__init__(image, (x, y))
        self.add_borders()

    def add_borders(self):
        """Draw an outer and inner border around the snapshot image."""
        new_surf = Surface((PREVIEW_WIDTH + (BORDER_WIDTH * 4),
                            PREVIEW_HEIGHT + (BORDER_WIDTH * 4)))
        new_surf.blit(self.image, (BORDER_WIDTH * 2, BORDER_WIDTH * 2))

        inner_rect = Rect(BORDER_WIDTH + get_line_center(BORDER_WIDTH),
                          BORDER_WIDTH + get_line_center(BORDER_WIDTH),
                          PREVIEW_WIDTH + BORDER_WIDTH + 1,
                          PREVIEW_HEIGHT + BORDER_WIDTH + 1)
        outer_rect = Rect(get_line_center(BORDER_WIDTH),
                          get_line_center(BORDER_WIDTH),
                          PREVIEW_WIDTH + (BORDER_WIDTH * 3) + 1,
                          PREVIEW_HEIGHT + (BORDER_WIDTH * 3) + 1)
        pygame.draw.rect(new_surf, PREVIEW_INNER_BORDER_COLOR, inner_rect,
                         BORDER_WIDTH)
        pygame.draw.rect(new_surf, PREVIEW_OUTER_BORDER_COLOR, outer_rect,
                          BORDER_WIDTH)

        self.image = new_surf

    def change_stage(self, new_image):
        """Change the displayed snapshot to represent another Stage.

        Args:
            new_image (Surface): The new Stage snapshot to be displayed.
        """
        self.image.blit(new_image, (BORDER_WIDTH * 2, BORDER_WIDTH * 2))


class BackgroundLine(Graphic):
    """A vertical line that moves back and forth horizontally across the
    the screen.

    Attributes:
        is_moving_right (Boolean): This indicates whether the line is
            currently moving to the right horizontally.
    """
    def __init__(self, x, thickness, is_moving_right):
        """Declare and initialize instance variables.

        Args:
            x (int): The initial x-position of the line's left edge.
            thickness (int): The thickness of the line, in pixels.
            is_moving_right (Boolean): Indicates whether the line is
                moving to the right initially.
        """
        image = self.render(thickness)
        super(BackgroundLine, self).__init__(image, (x, 0))
        self.is_moving_right = is_moving_right

    def render(self, thickness):
        """Return a Surface containing the drawn line.

        Args:
            thickness (int): The thickness of the line, in pixels.
        """
        surf = Surface((thickness, SCREEN_SIZE[1]))
        x = get_line_center(thickness)
        pygame.draw.line(surf, LINE_COLOR, (x, 0),
                         (x, SCREEN_SIZE[1]), thickness)
        return surf

    def update_movement(self, time_elapsed):
        """Update the line's horizontal movement.

        Args:
            time_elapsed (float): The time elapsed, in seconds, since
                the last update cycle.
        """
        distance = LINE_SPEED * time_elapsed

        if self.is_moving_right:
            if self.get_right_edge() + distance > LINE_RIGHT_BOUND:
                # Line bounces off right edge.
                distance = LINE_RIGHT_BOUND - self.get_right_edge()
                self.move(distance * -1, 0)
                self.is_moving_right = False
            else:
                self.move(distance, 0)
        else:
            if self.rect.x - distance < LINE_LEFT_BOUND:
                # Line bounces off left edge.
                distance = self.rect.x - LINE_LEFT_BOUND
                self.move(distance, 0)
                self.is_moving_right = True
            else:
                self.move(distance * -1, 0)


class CursorDirection(IntEnum):
    """An enum containing values that represent the possible 'motion'
    of the cursor, as directed by the players.

    Values;
        PREVIOUS: Select the Stage above the current one.
        NEXT: Select the Stage below the current one.
        PREVIOUS_ROW: Move the cursor so that a number of Stages that
            fit the screen above the current Stage are displayed, with
            the top-most one selected.
        NEXT_ROW: Move the cursor so that a number of Stages that fit
            the screen below the current Stage are displayed, with the
            top-most one selected.
    """
    PREVIOUS = 0
    NEXT = 1
    PREVIOUS_ROW = 2
    NEXT_ROW = 3

