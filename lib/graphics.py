"""This module contains classes for representing in-game sprites and
animations via the PyGame Surface and Image modules.

It also contains module level methods to assist in loading and managing
in-game images in other modules.
"""
from __builtin__ import True, False
from math import ceil
from pygame.locals import *
from pygame.surface import Surface
from pygame import image
from pygame import transform
from pygame import color
from pygame import Rect


def load_tuple_of_images(filepaths):
    """Load a collection of Surfaces from file and store them in an
    immutable container -- a tuple.

    Args:
        filepaths: A tuple of Strings for the file paths to each image.

    Returns:
        A list of Surfaces, each containing an image loaded from file.
    """
    all_images = []

    for filepath in filepaths:
        new_image = image.load(filepath).convert_alpha()
        all_images.append(new_image)

    return tuple(all_images)


def render_text(font, text, text_color, outline_color=None,
                         position=None):
        """Render a text Surface or Graphic, with an optional outline
        1-pixel thick.

        Args:
            font: A PyGame Font object used for rendering the text.
            text: A String for the text that will be rendered.
            text_color: A tuple of integers which specify the RGB color
                of the text.
            outline_color: Optional. A tuple of integers which specify
                the RGB color  of a 1-pixel thick outline.
            position: Optional. A tuple containing integer coordinates
                for the text's position relative to its parent Surface.
                The default value of None will cause this function to
                return a Surface, while passing a proper position tuple
                will cause it to return a Graphic.

        Returns:
            A Surface with the desired text, outlined if specified.
            Passing a position returns a Graphic instead.
        """
        text_surf = font.render(text, True, text_color)

        if outline_color is not None:
            outline = font.render(text, True, outline_color)
            outlined_text_surf = Surface((text_surf.get_width() + 2,
                                    text_surf.get_height() + 2),
                                    SRCALPHA)
            outlined_text_surf.blit(outline, (0, 0))
            outlined_text_surf.blit(outline, (0, 2))
            outlined_text_surf.blit(outline, (2, 0))
            outlined_text_surf.blit(outline, (2, 2))
            outlined_text_surf.blit(text_surf, (1, 1))
            text_surf = outlined_text_surf

        if position is None:
            return text_surf
        else:
            text_graphic = Graphic(outlined_text_surf, position)
            return text_graphic


def convert_to_colorkey_alpha(surf, colorkey=color.Color('magenta')):
        """Give the surface a colorkeyed background that will be
        transparent when drawing.
        Colorkey alpha, unlike per-pixel alpha, will allow the
        surface's transparent background to remain while using
        methods such as Surface.set_alpha().

        Keyword arguments:
            surf        The Surface to convert.
            colorkey    The color value for the colorkey. The default
                        is magenta or RGB(255, 0, 255).
                        This should be set to a color that isn't
                        present in the image, otherwise those areas
                        with a matching colour will be drawn
                        transparent as well.
        """
        colorkeyed_surf = Surface(surf.get_size())

        colorkeyed_surf.fill(colorkey)
        colorkeyed_surf.blit(surf, (0, 0))
        colorkeyed_surf.set_colorkey(colorkey)
        colorkeyed_surf.convert()

        return colorkeyed_surf


def calculate_center_position(area_origin, area_size, obj_size):
    """Return an integer for the position of a graphical object such
    that the object is positioned at the horizontal or vertical center
    of an area.

    To center an object horizontally, pass the widths of the object and
    area, as well as the area's top-left x-coordinate.
    To center an object vertically, pass their heights in addition to
    the area's top-left y-coordinate.

    Args:
        area_origin (int): The x or y coordinate  of the top-left
            corner of the area upon which the object will be centered.
        area_size (int): Either the width or height, in pixels, of the
             area upon which the object will be centered.
        obj_size (int): Either the width or height of the object in
            pixels.
    """
    if obj_size < area_size:
        return (area_origin + ((area_size - obj_size) // 2))
    else:
        return (area_origin + ((obj_size - area_size) // 2))


def get_line_center(thickness):
    """Return an integer representing the center of a line, or a line
    that is part of a rectangle, drawn by the pygame.draw module.

    The x or y coordinate passed to a pygame.draw function is used as
    the 'centre' of the drawing's thickness. To position it from the
    left or top, add the value produced by this function to the x or y
    argument(s) within the pygame.draw function call.

    Args:
        thickness (int): The thickness of the line, in pixels.
    """
    # Since even-number widths don't have a center, pygame.draw shifts the
    # line center 1 pixel left/up, if the thickness is even.
    # Thus, center is calculated by dividing thickness by 2 and subtracting 1.

    # But wouldn't subtracting 1 mess up odd-number widths, which have a center?
    # To cancel out the subtraction, ceil() is used to round decimal quotients
    # up by 1.
    center = ceil(float(thickness) / 2.0) - 1
    return int(center)


class Graphic(object):
    """An in-game image that can be drawn to the screen.

    Attributes:
            image       The PyGame Surface object that contains this
                        Graphic's visual content.
            exact_pos   A tuple containing the Graphic's exact
                        on-screen coordinates as floats. rect will
                        round them down to integers to make the
                        position suitable for whole-pixel drawing.
            rect        A PyGame Rect object that contains the
                        Graphic's on-screen coordinates as well as its
                        dimensions.
    """
    def __init__(self, surf, position):
        """Declare and initialize instance variables.

        Keyword arguments:
            surf        The PyGame Surface containing this Graphic's
                        image.
            position    Tuple containing the coordinates of the
                        top-left corner of the image relative to the
                        screen.
        """
        self.image = surf
        self.exact_pos = position
        width = self.image.get_width()
        height = self.image.get_height()
        self.rect = Rect(int(self.exact_pos[0]), int(self.exact_pos[1]),
                         width, height)

    @classmethod
    def from_file(self, filepath, position):
        """Create a Graphic from an external image file.

        Keyword arguments:
            filepath    The file path to the image that will be loaded
                        into this Graphic.
            position    Tuple containing the coordinates of the
                        top-left corner of the image relative to the
                        screen.
        """
        external_image = image.load(filepath)
        external_image = convert_to_colorkey_alpha(external_image)
        return Graphic(external_image, position)

    def get_right_edge(self):
        """Return the x-coordinate of the Graphic's right edge."""
        right_edge = self.rect.x + self.rect.width
        return right_edge

    def get_bottom_edge(self):
        """Return the y-coordinate of the Graphic's bottom edge."""
        bottom_edge = self.rect.y + self.rect.height
        return bottom_edge

    def flip(self, is_horizontal=False, is_vertical=False):
        """Flip this graphic horizontally, vertically, or both.

        Args:
            is_horizontal: A Boolean indicating whether to flip the
                Graphic's image horizontally.
            is_vertical: A Boolean indicating whether to flip the
                Graphic's image vertically.
        """
        self.image = transform.flip(self.image, is_horizontal,
                                    is_vertical)

    def draw(self, surf, x=None, y=None, region=None):
        """Draw the Graphic onto a specified Surface.

        Args:
            surf: The Surface where this Graphic will be drawn
                to.
            x: Optional. The x-position of the Graphic relative to the
                parent Surface. If this is not given, the position
                passed to init() will be used instead.
            y: Optional. The y-position of the Graphic relative to the
                parent Surface. If this is not given, the position
                passed to init() will be used instead.
            region: Optional. A Rect specifying the area of this
                Graphic that will be drawn onto the parent Surface. If
                this is None, all of the Graphic will be drawn.
        """
        if x is None or y is None:
            surf.blit(self.image, self.rect, region)
        else:
            surf.blit(self.image, (x, y), region)

    def move(self, dx=0, dy=0):
        """Move the Graphic some distance across the screen.

        Keyword arguments:
            dx      Optional. The horizontal distance. Positive values
                    will move it to the right, and negative values will
                    move it to the left.
            dy      Optional. The vertical distance. Positive values
                    will move it down, and negative values will move it
                    up.
        """
        self.exact_pos = (self.exact_pos[0] + dx, self.exact_pos[1] + dy)
        self.rect = Rect(int(self.exact_pos[0]), int(self.exact_pos[1]),
                         self.rect.width, self.rect.height)

    def reposition(self, x=None, y=None):
        """Directly set the x and/or y-position of this Graphic
        on-screen.

        Args:
            x (int): Optional. The new x-position for this Graphic
                on-screen. Set this parameter to the default None to
                keep the current x-position.
            y (int): Optional. The new y-position for this Graphic
                on-screen. Set this parameter to the default None to
                keep the current y-position.
        """
        if x is not None:
            self.exact_pos = (float(x), self.exact_pos[1])
            self.rect.x = x
        if y is not None:
            self.exact_pos = (self.exact_pos[0], float(y))
            self.rect.y = y


class Animation(Graphic):
    """An animated graphic that displays different frames after a time
    interval.
    Animations use spritesheet images, with frames of the same width
    and height being lined up in order from left-to-right.

    Attributes:
        image               The PyGame Surface object that contains
                            this Animation's spritesheet.
        exact_pos           A tuple containing the Animation's exact
                            on-screen coordinates as floats. rect will
                            round them down to integers to make the
                            position suitable for whole-pixel drawing.
        rect                A PyGame Rect object that contains the
                            Animation's on-screen coordinates as well
                            as its dimensions.
        frame_amount        The number of frames in the Animation.
        frame_width         The width of each frame within the
                            spritesheet.
        frame_duration      The amount of time to display each frame
                            before moving onto the next.
                            This is measured in update 'frames,' which
                            are 1/60th of a second.
        duration_counter    A counter that is incremented each time the
                            game updates. When the value matches
                            frame_duration, it is reset and the
                            animation switches to the next frame.
        current_frame       The index of the current frame
                            being displayed.
        last_frame          The index of the last frame.
        draw_rect           A Rect for the region of the spritesheet
                            that corresponds to the current frame. This
                            is the portion that will be drawn
                            on-screen.
        is_animated         Set to True to have the Animation cycle
                            through the display of each of its frames.
                            Each frame will be shown for the duration
                            specified by frame_duration before moving
                            onto the next.
                            By default, this is set to True.
        is_looped           Set to True if the Animation should return
                            to the first frame after displaying the
                            final frame. False will keep the final
                            frame displayed once the Animation
                            finishes.
                            By default, this is set to True.
        is_reversed         Set to True if the Animation should cycle
                            through its frames in reverse order.
                            By default, this is set to False.
    """

    def __init__(self, surf, position, frame_amount, frame_duration,
                 is_animated=True, is_looped=True, is_reversed=False):
        """Declare and initialize instance variables.

        Keyword arguments:
            surf                The PyGame Surface containing this
                                Animation's spritesheet image.
            position            A tuple containing the coordinates of
                                the top-left point of the Animation
                                relative to the screen.
            frame_amount        The number of frames in this Animation.
            frame_duration      How long each frame should be displayed
                                for. Measured in units of one frame per
                                FPS (check globals.py for this value).
            is_animated         Set to False if the Animation shouldn't
                                start playing immediately.
            is_looped           Set to False if the Animation should
                                only play once.
            is_reversed         Set to True if the Animation should
                                play backwards.
        """
        super(Animation, self).__init__(surf, position)
        self.frame_amount = frame_amount
        self.frame_width = self.calculate_frame_width()
        self.frame_duration = frame_duration
        self.duration_counter = 0
        self.current_frame = 0
        self.last_frame = frame_amount - 1
        self.draw_rect = self.get_draw_rect()
        self.is_animated = is_animated
        self.is_looped = is_looped
        self.is_reversed = is_reversed

    @classmethod
    def from_file(self, filepath, position, frame_amount, frame_duration,
                  is_animated=True, is_looped=True, is_reversed=False):
        """Create an Animation from an external image file.

        Keyword arguments:
            filepath            The filepath to this Animation's
                                spritesheet.
            position            A tuple containing the coordinates of
                                the top-left point of the Animation
                                relative to the screen.
            frame_amount        The number of frames in this Animation.
            frame_duration      How long each frame should be displayed
                                for. Measured in units of one frame per
                                FPS (check globals.py for this value).
            is_animated         Set to False if the Animation shouldn't
                                start playing immediately.
            is_looped           Set to False if the Animation should
                                only play once.
            is_reversed         Set to True if the Animation should
                                play backwards.
        """
        external_sheet = image.load(filepath)
        external_sheet = convert_to_colorkey_alpha(external_sheet)
        return Animation(external_sheet, position, frame_amount,
                         frame_duration, is_animated, is_looped,
                         is_reversed)

    def calculate_frame_width(self):
        """Calculate the frame width by dividing the width of the
        spritesheet by the number of frames specified in frame_amount
        and return the result.
        """
        frame_width = int(self.rect.width / self.frame_amount)
        return frame_width

    def get_draw_rect(self):
        """Determine the region of the spritesheet representing the
        current frame and return it as a Rect.
        """
        # Since the frames in the spritesheet are ordered left-to-right and
        # have a uniform width, the left edge of a frame can be found by
        # multiplying the frame width by the desired frame's index number.
        x = self.frame_width * self.current_frame
        y = 0
        width = self.frame_width
        height = self.rect.height   # All frames share the same height.

        draw_rect = Rect(x, y, width, height)

        return draw_rect

    def get_right_edge(self):
        """Return the x-coordinate of the Animation frame's right
        edge.
        """
        right_edge = self.rect.x + self.frame_width
        return right_edge

    def reset_animation(self):
        """Reset the animation and prepare it to be played again."""
        self.duration_counter = 0
        self.current_frame = 0

    def animate(self):
        """Update the duration counter and switch to the next frame
        when it matches the frame duration.
        If is_looped is set to True, the animation will loop back
        to the first frame after the final frame is complete.
        is_reversed will cause the frames to be cycled backwards.
        """
        self.duration_counter += 1

        if self.duration_counter >= self.frame_duration:
            # Cycle through to the next frame.
            if self.is_reversed == False:
                self.current_frame += 1
            else:
                self.current_frame -= 1

            # At the end of a regular animation.
            if self.current_frame > self.last_frame:
                if self.is_looped == True:
                    self.current_frame = 0
                else:
                    self.is_animated = False
            # At the end of a reversed animation.
            elif self.current_frame < 0:
                if self.is_looped == True:
                    self.current_frame = self.last_frame
                else:
                    self.is_animated = False

            self.draw_rect = self.get_draw_rect()
            self.duration_counter = 0

    def draw(self, parent_surf):
        """Draw the current frame onto the specified Surface.

        Keyword arguments:
            parent_surf     The Surface upon which the Animation will
                            be drawn.
        """
        if self.is_animated == True:
            self.animate()

        parent_surf.blit(self.image, self.rect, self.draw_rect)


class CharacterAnimation(object):
    """A special type of animation for a character's action.

    Unlike regular Animations, this one can have different durations for
    each individual frame.

    Attributes:
        is_facing_left: A Boolean indicating whether the character is
            facing to the left instead of to the right.
        spritesheet: A PyGame Surface containing all of the animation
            frames in order.
        frame_durations: A tuple of integers containing the duration,
            in update cycles, of each animation frame in order.
        current_frame: An integer for the index of the animation frame
            currently being displayed.
        frame_timer: An integer for the number of update cycles elapsed
            since the current animation frame was shown.
    """
    def __init__(self, is_facing_left, spritesheet, frame_durations):
        """Declare and initialize instance variables:

        Args:
            is_facing_left: A Boolean indicating whether the character
                is facing to the left, rather than to the right (which
                is the default direction for characters in this game).
            spritesheet_path: A Surface containing the animation's
                spritesheet image.
            frame_width: An integer for the width, in pixels, of each
                frame in the animation sprite sheet.
            frame_durations: A tuple of integers containing the
                duration, in update cycles, of each animation frame in
                order. For example, passing (10, 8, 5) means that the
                first animation frame is shown for 10 update cycles,
                the second frame for 8 update cycles, and so on.
        """
        self.spritesheet = spritesheet
        self.is_facing_left = is_facing_left
        self.frame_durations = frame_durations
        self.current_frame = 0
        self.frame_timer = 0
        if is_facing_left:
            self.flip_sprite()

    def change_animation(self, spritesheet, frame_durations):
        """Display a different animation.

        Args:
            spritesheet: A Surface containing the animation's
                spritesheet image.
            frame_durations: A tuple of integers containing the
                duration, in update cycles, of each animation frame in
                order. For example, passing (10, 8, 5) means that the
                first animation frame is shown for 10 update cycles,
                the second frame for 8 update cycles, and so on.
        """
        self.frame_durations = frame_durations
        self.spritesheet = spritesheet
        self.current_frame = 0
        self.frame_timer = 0
        if self.is_facing_left:
            self.flip_sprite()

    def get_num_of_frames(self):
        """Return an integer for the number of frames in the
        animation.
        """
        return len(self.frame_durations)

    def switch_direction(self):
        """Make the animation face in the opposite direction."""
        self.is_facing_left = not self.is_facing_left
        self.flip_sprite()

    def flip_sprite(self):
        """Alter the spritesheet so that the character faces in the
        other direction.
        """
        flipped_sheet = transform.flip(self.spritesheet, True, False)
        self.spritesheet = self.order_reversed_spritesheet(flipped_sheet)

    def order_reversed_spritesheet(self, flipped_sheet):
        """Reorganize the frames in a flipped sprite sheet so that
        they are in the same order as the original sheet.

        Args:
            flipped_sheet: A PyGame Surface containing a flipped sprite
                sheet.

        Returns:
            A PyGame Surface containing the sprite sheet with each frame
            flipped and in the correct order.
        """
        ordered_sheet = Surface((self.spritesheet.get_width(),
                                 self.spritesheet.get_height()),
                                SRCALPHA)
        ordered_sheet.convert_alpha()

        for frame_index in xrange(0, self.get_num_of_frames()):
            frame_x = self.get_width() * frame_index
            old_frame_index = self.get_num_of_frames() - 1 - frame_index
            old_region = self.get_frame_region(old_frame_index)

            ordered_sheet.blit(flipped_sheet, (frame_x, 0), old_region)

        return ordered_sheet

    def get_frame_region(self, frame_index):
        """Get the region occupied by of one of the animation frames
        within the sprite sheet.

        Args:
            frame_index: An integer for the index of the desired frame.

        Returns:
            A Rect containing the frame's position and dimensions within
            the sprite sheet.
        """
        frame_x = self.get_width() * frame_index
        sheet_height = self.spritesheet.get_height()
        region = Rect(frame_x, 0, self.get_width(), sheet_height)
        return region

    def get_width(self):
        """Return an integer for the width, in pixels, of each
        individual animation frame.
        """
        width = self.spritesheet.get_width() / self.get_num_of_frames()
        return int(width)

    def get_height(self):
        """Return an integer for the height of each frame, in pixels."""
        return self.spritesheet.get_height()

    def draw(self, parent_surf, x, y):
        """Draw the animation onto a Surface at a specific location.

        Args:
            parent_surf: The Surface upon which the animation will be
                drawn.
            x: An integer for the animation's x-position relative to the
                parent Surface.
            y: An integer for the animation's y-position relative to the
                parent Surface.
        """
        frame_region = self.get_frame_region(self.current_frame)
        parent_surf.blit(self.spritesheet, (x, y), frame_region)

    def update(self):
        """Update the animation by cycling through to the next frame
        once enough time has elapsed.
        """
        self.frame_timer += 1

        if self.frame_timer >= self.frame_durations[self.current_frame]:
            self.frame_timer = 0

            self.current_frame += 1
            if self.current_frame > self.get_num_of_frames() - 1:
                self.current_frame = 0
