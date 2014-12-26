"""This module contains classes for representing in-game sprites and
animations via the PyGame Surface and Image modules."""
from __builtin__ import True, False
from pygame.locals import *
from pygame import Surface
from pygame import image
from pygame import transform
from pygame import color
from pygame import Rect

class Graphic(object):
    """An in-game image that can be drawn to the screen.
    
    Attributes:
            image       The PyGame Surface object that contains this
                        Graphic's visual content.
            filepath    The filepath to where the image content was
                        loaded from.
            exact_pos   A tuple containing the Graphic's exact
                        on-screen coordinates as floats. rect will
                        round them down to integers to make the
                        position suitable for whole-pixel drawing.
            rect        A PyGame Rect object that contains the
                        Graphic's on-screen coordinates as well as its
                        dimensions.
    """
    def __init__(self, filepath, position):
        """Declare and initialize instance variables.

        Keyword arguments:
            filepath    The filepath to the image that will be loaded
                        and displayed in-game.
            position    Tuple containing the coordinates of the
                        top-left corner of the image relative to the
                        screen.
        """
        self.image = image.load(filepath)
        self.image = self.convert_to_colorkey_alpha(self.image)
        self.filepath = filepath

        width = self.image.get_width()
        height = self.image.get_height()
        self.exact_pos = position
        self.rect = Rect(int(self.exact_pos[0]), int(self.exact_pos[1]),
                         width, height)

    def convert_to_colorkey_alpha(self, surf,
                                  colorkey=color.Color('magenta')):
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

    def draw(self, surf, x=None, y=None):
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
        """
        if x is None or y is None:
            surf.blit(self.image, self.rect)
        else:
            surf.blit(self.image, (x, y))

    def move(self, dx, dy):
        """Move the Graphic some distance across the screen.

        Keyword arguments:
            dx      The horizontal distance. Positive values will move
                    it to the right, and negative values will move it
                    to the left.
            dy      The vertical distance. Positive values will move it
                    down, and negative values will move it up.
        """
        self.exact_pos = (self.exact_pos[0] + dx, self.exact_pos[1] + dy)
        self.rect = Rect(int(self.exact_pos[0]), int(self.exact_pos[1]),
                         self.rect.width, self.rect.height)


class Animation(Graphic):
    """An animated graphic that displays different frames after a time
    interval.
    Animations use spritesheet images, with frames of the same width
    and height being lined up in order from left-to-right.

    Attributes:
        image               The PyGame Surface object that contains
                            this Animation's spritesheet.
        filepath            The filepath to where the spritesheet
                            image is located.
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

    def __init__(self, filepath, position, frame_amount, frame_duration,
                 is_animated=True, is_looped=True, is_reversed=False):
        """Declare and initialize instance variables.

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
        super(Animation, self).__init__(filepath, position)
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