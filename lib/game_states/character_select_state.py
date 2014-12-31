import pygame.transform as transform
import pygame.draw
from pygame import image
from pygame.surface import Surface
from pygame.rect import Rect
from lib.globals import SCREEN_SIZE


class CharacterPreview(object):
    """A looped character animation with an accompanying shadow and
    name.

    Class Constants:
        NAME_COLOR: A tuple containing the RGB values for the name
            text's color.
        NAME_OUTLINE_COLOR: A tuple containing the RGB values for the
            color of the name text's outline.
        SHADOW_HEIGHT: An integer for the height of the shadow, in
            pixels.
        SHADOW_COLOR: A tuple containing the RGB values for the color
            of the shadow.
        OFFSET_FROM_SHADOW: An integer for the distance, in pixels,
            from the bottom edge of the character sprite to the vertical
            center of the shadow.

    Attributes:
        x: An integer for the x-coordinate of the sprite relative to the
            screen.
        y: An integer for the y-coordinate of the sprite relative to the
            screen.
        is_facing_left: A Boolean indicating whether the character is
            facing to the left instead of to the right.
        name: A PyGame Surface with the character's name rendered onto
            it.
        spritesheet: A PyGame Surface containing all of the animation
            frames in order.
        shadow: A PyGame Surface with the character's shadow drawn onto
            it.
        frame_width: An integer for width, in pixels, of each frame in
            the animation.
        frame_durations: A tuple of integers containing the duration,
            in update cycles, of each animation frame in order.
        current_frame: An integer for the index of the animation frame
            currently being displayed.
        frame_timer: An integer for the number of update cycles elapsed
            since the current animation frame was shown.
    """
    NAME_COLOR = (255, 255, 255)
    NAME_OUTLINE_COLOR = (80, 80, 80)
    SHADOW_HEIGHT = 14
    SHADOW_COLOR = (0, 5, 90)
    OFFSET_FROM_SHADOW = 3

    def __init__(self, ground_y, is_facing_left, spritesheet_path, name,
                 name_font, frame_width, frame_durations):
        """Declare and initialize instance variables.

        Args:
            ground_y: An integer for the y-position of the ground where
                the character will be standing, relative to the screen.
            is_facing_left: A Boolean indicating whether the character
                is facing to the left, rather than to the right (which
                is the default direction for characters in this game).
            spritesheet_path: A String for the file path to the
                animation's sprite sheet image.
            name: A String for the character's name.s
            name_font: The PyGame font used for rendering the
                character's name.
            frame_width: An integer for the width, in pixels, of each
                frame in the animation sprite sheet.
            frame_durations: A tuple of integers containing the
                duration, in update cycles, of each animation frame in
                order. For example, passing (10, 8, 5) means that the
                first animation frame is shown for 10 update cycles,
                the second frame for 8 update cycles, and so on.
        """
        self.x = 0
        self.y = self.calculate_y_position(ground_y)
        self.is_facing_left = is_facing_left
        self.spritesheet = image.load(spritesheet_path).convert_alpha()
        self.name = self.render_name(name, name_font)
        self.frame_width = frame_width
        self.frame_durations = frame_durations
        self.current_frame = 0
        self.frame_timer = 0
        self.shadow = self.render_shadow()

        if is_facing_left:
            self.flip_sprite()
            self.correct_position()

    def calculate_y_position(self, ground_y):
        """Determine the vertical positioning of the character so that
        the bottom edge of the sprite (usually their feet) is touching
        the ground.

        Args:
            ground_y: An integer for the y-position of the ground
                relative to the screen.

        Returns:
            An integer for the character's y-position.
        """
        character_height = self.spritesheet.get_height()
        y = ground_y - character_height
        return y

    def correct_position(self):
        """Position the animation horizontally so that it is on the left
        edge of the screen if the character faces right, or on the right
        edge if the character faces left.
        """
        if self.is_facing_left:
            self.x = SCREEN_SIZE[0] - self.frame_width
        else:
            self.x = 0

    def get_num_of_frames(self):
        """Return an integer for the number of frames in the
        animation.
        """
        return len(self.frame_durations)

    def flip_sprite(self):
        """Alter the sprite sheet so that the character faces in the
        opposite direction.
        """
        flipped_sheet = transform.flip(self.spritesheet, xbool=True,
                                       ybool=False)
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
        flipped_sprite_sheet = Surface((self.spritesheet.get_width(),
                                        self.spritesheet.get_height()))
        flipped_sprite_sheet.convert_alpha()

        for frame_index in xrange(0, self.get_num_of_frames()):
            frame_x = self.frame_width * frame_index
            old_frame_index = self.get_num_of_frames() - 1 - frame_index
            old_region = self.get_frame_region(old_frame_index)

            flipped_sprite_sheet.blit(flipped_sheet, (frame_x, 0),
                                      old_region)

        return flipped_sprite_sheet

    def get_frame_region(self, frame_index):
        """Get the region occupied by of one of the animation frames
        within the sprite sheet.

        Args:
            frame_index: An integer for the index of the desired frame.

        Returns:
            A Rect containing the frame's position and dimensions within
            the sprite sheet.
        """
        frame_x = self.frame_width * frame_index
        sheet_height = self.spritesheet.get_height()
        region = Rect(frame_x, 0, self.frame_width, sheet_height)
        return region

    def render_name(self, name, font):
        """Render the character's name onto a new Surface.

        Args:
            name: A String for the character's name.
            font: A PyGame Font object that will be used to render the
                name as a text graphic.

        Returns:
            A Surface with the character's name drawn and outlined.
        """
        text_surf = font.render(name, True, self.NAME_COLOR)
        outline = font.render(name, True, self.NAME_OUTLINE_COLOR)
        name_surf = self.add_outline_to_text(text_surf, outline)
        return name_surf

    def add_outline_to_text(self, text_surf, outline):
        """Combine a text Surface with a pre-made outline Surface to add
        a 1-pixel thick outline to the text.

        Args:
            text_surf: A PyGame Surface with text drawn onto it.
            outline: A PyGame Surface containing the same text as the
                one in text_surf, but rendered in a darker color.

        Returns:
            A Surface with the original text outlined.
        """
        outlined_text = Surface((text_surf.get_width() + 2,
                                 text_surf.get_height() + 2))

        outlined_text.blit(outline, (0, 0))
        outlined_text.blit(outline, (0, 2))
        outlined_text.blit(outline, (2, 0))
        outlined_text.blit(outline, (2, 2))
        outlined_text.blit(text_surf, (1, 1))

        return outlined_text

    def render_shadow(self):
        """Render a shadow to fit the character.

        Returns:
            A Surface with a shadow wide enough to fit the character
            drawn onto it.
        """
        shadow_surf = Surface((self.frame_width, self.SHADOW_HEIGHT + 1))
        center_y = self.SHADOW_HEIGHT / 2

        draw_region = Rect(0, center_y, self.frame_width,
                           self.SHADOW_HEIGHT)
        pygame.draw.ellipse(shadow_surf, self.SHADOW_COLOR, draw_region)
        return shadow_surf
