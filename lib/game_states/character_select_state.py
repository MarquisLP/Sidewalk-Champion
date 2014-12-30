from pygame import image
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
        is_reversed: A Boolean indicating whether the character is
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

    def __init__(self, ground_y, is_reversed, spritesheet_path, name,
                 name_font, frame_width, frame_durations):
        """Declare and initialize instance variables.

        Args:
            ground_y: An integer for the y-position of the ground where
                the character will be standing, relative to the screen.
            is_reversed: A Boolean indicating whether the character
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
        self.spritesheet = image.load(spritesheet_path).convert_alpha()
        self.is_reversed = is_reversed
        self.x = 0
        self.y = self.calculate_y_position(ground_y)
        if is_reversed:
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
        if self.is_reversed:
            self.x = SCREEN_SIZE[0] - self.frame_width
        else:
            self.x = 0
