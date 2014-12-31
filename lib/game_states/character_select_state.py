import pygame.transform as transform
import pygame.draw
import pygame.locals
from pygame import image
from pygame.surface import Surface
from pygame.rect import Rect
from lib.graphics import CharacterAnimation
from lib.globals import SCREEN_SIZE


class CharacterPreview(object):
    """A looped character animation with an accompanying shadow and
    name.

    Class Constants:
        GROUND_Y: An integer for the y-position of the ground upon which
            the character will be standing, relative to the screen.
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
        animation: A CharacterAnimation object that updates and displays
            the character's animation.
        name: A PyGame Surface with the character's name rendered onto
            it.
        shadow: A PyGame Surface with the character's shadow drawn onto
            it.
    """
    GROUND_Y = 157
    NAME_COLOR = (255, 255, 255)
    NAME_OUTLINE_COLOR = (80, 80, 80)
    SHADOW_HEIGHT = 14
    SHADOW_COLOR = (0, 5, 90)
    OFFSET_FROM_SHADOW = 3

    def __init__(self, is_facing_left, spritesheet_path, name,
                 name_font, frame_durations):
        """Declare and initialize instance variables.

        Args:
            is_facing_left: A Boolean indicating whether the character
                is facing to the left, rather than to the right (which
                is the default direction for characters in this game).
            spritesheet_path: A String for the file path to the
                animation's sprite sheet image.
            name: A String for the character's name.
            name_font: The PyGame font used for rendering the
                character's name.
            frame_durations: A tuple of integers containing the
                duration, in update cycles, of each animation frame in
                order. For example, passing (10, 8, 5) means that the
                first animation frame is shown for 10 update cycles,
                the second frame for 8 update cycles, and so on.
        """
        self.is_facing_left = is_facing_left
        self.animation = CharacterAnimation(is_facing_left,
                                            spritesheet_path,
                                            frame_durations)
        self.name_font = name_font
        self.name = self.render_name(name)
        self.shadow = self.render_shadow()
        self.x = 0
        self.y = self.calculate_y_position()

        if is_facing_left:
            self.correct_position()

    def change_character(self, spritesheet_path, name, frame_durations):
        """Display a different character animation.

        Args:
            spritesheet_path: A String for the file path to the
                animation's sprite sheet image.
            name: A String for the character's name.
            frame_durations: A tuple of integers containing the
                duration, in update cycles, of each animation frame in
                order. For example, passing (10, 8, 5) means that the
                first animation frame is shown for 10 update cycles,
                the second frame for 8 update cycles, and so on.
        """
        self.animation.change_animation(spritesheet_path,
                                        frame_durations)
        self.name = self.render_name(name)
        self.shadow = self.render_shadow()
        self.x = 0
        self.y = self.calculate_y_position()
        if self.is_facing_left:
            self.correct_position()

    def calculate_y_position(self):
        """Determine the vertical positioning of the character so that
        the bottom edge of the sprite (usually their feet) is touching
        the ground.

        Args:
            ground_y: An integer for the y-position of the ground
                relative to the screen.

        Returns:
            An integer for the character's y-position.
        """
        character_height = self.animation.get_height()
        y = self.GROUND_Y - character_height
        return y

    def correct_position(self):
        """Position the animation horizontally so that it is on the left
        edge of the screen if the character faces right, or on the right
        edge if the character faces left.
        """
        if self.is_facing_left:
            self.x = SCREEN_SIZE[0] - self.animation.get_width()
        else:
            self.x = 0

    def render_name(self, name):
        """Render the character's name onto a new Surface.

        Args:
            name: A String for the character's name.
            font: A PyGame Font object that will be used to render the
                name as a text graphic.

        Returns:
            A Surface with the character's name drawn and outlined.
        """
        text_surf = self.name_font.render(name, True, self.NAME_COLOR)
        outline = self.name_font.render(name, True,
                                        self.NAME_OUTLINE_COLOR)
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
                                 text_surf.get_height() + 2),
                                pygame.locals.SRCALPHA)

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
        frame_width = self.animation.get_width()
        shadow_surf = Surface((frame_width, self.SHADOW_HEIGHT + 1),
                              pygame.locals.SRCALPHA)
        draw_region = Rect(0, 0, frame_width, self.SHADOW_HEIGHT)

        pygame.draw.ellipse(shadow_surf, self.SHADOW_COLOR, draw_region)
        return shadow_surf

    def update(self):
        """Update the character animation."""
        self.animation.update()

    def move(self, dx=0, dy=0):
        """Move the animation around the screen space.

        Args:
            dx: An integer for the horizontal shift, in pixels.
                A positive value causes a shift to the right, while a
                negative value causes a shift to the left.
            dx: An integer for the vertical shift, in pixels.
                A positive value shifts the animation down, while a
                negative value shifts the animation up.
        """
        self.x += dx
        self.y += dy

    def place_offscreen(self):
        """Set the position of the animation so that it is just off the
        left edge of the screen if the character faces right, or just
        off the right edge of the screen if the character faces left.
        """
        if self.is_facing_left:
            self.x = SCREEN_SIZE[0]
        else:
            self.x = 0 - self.animation.get_width()

    def is_onscreen(self):
        """Return a Boolean indicating whether all of the animation is
        visible on-screen.
        """
        if (self.x >= 0 and
           self.x + self.animation.get_width() <= SCREEN_SIZE[0]):
            return True
        else:
            return False

    def is_offscreen(self):
        """Return a Boolean indicating whether none of the animation is
        visible on-screen.
        """
        if (self.x + self.animation.get_width() <= 0 or
           self.x >= SCREEN_SIZE[0]):
            return True
        else:
            return False
