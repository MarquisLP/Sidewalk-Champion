import pygame.transform as transform
import pygame.draw
import pygame.locals
from pygame import image
from pygame.surface import Surface
from pygame.rect import Rect
from lib.graphics import load_tuple_of_images
from lib.graphics import render_outlined_text
from lib.graphics import convert_to_colorkey_alpha
from lib.graphics import Animation
from lib.graphics import CharacterAnimation
from lib.globals import SCREEN_SIZE


class RosterDisplay():
    """An on-screen list of the entire roster of playable characters
    available in this copy of the game.

    Players will use this list to select characters for a battle.
    Since only one row characters can be displayed at a time, only one
    player may select from the list at a time; the color of the cursor
    can be toggled to show which player is currently choosing.

    Class Constants:
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

    Attributes:
        x: An integer for the x-position of the roster relative to the
            screen.
        y: An integer for the y-position of the roster relative to the
            screen.
        mugshots: A tuple of Surfaces, each containing a character's
            mugshot.
        current_row: An integer for the index of the currently-selected
            'row' of characters. Each row contains a number of
            characters specified by the SLOTS_PER_ROW constant.
        current_slot: An integer for the index of the currently-selected
            slot within the current row.
            For example, if current_row is 1 and current_slot is 2, the
            seventh character overall is currently being selected. Use
            get_character_index() if you wish to obtain this data.
        cursor: A RosterCursor used for marking the currently-selected
            mugshot.
        rendered_row: A Surface containing the currently-selected row
            of character slots.
        scroll_up_arrow: A RosterArrow indicating that the players can
            scroll up a row.
        scroll_down_arrow: A RosterArrow indicating that the players can
            scroll down a row.
    """
    MUGSHOT_SIZE = 50
    SLOTS_PER_ROW = 5
    FRAME_THICKNESS = 2
    FRAME_COLOR = (102, 102, 102)
    BACKGROUND_COLOR = (255, 255, 255)
    ARROW_DISTANCE = 11

    def __init__(self, mugshot_paths):
        """Declare and initialize instance variables.

        Args:
            mugshot_paths: A tuple of Strings which refer to the file
                paths of each character's mugshot image.
        """
        self.mugshots = load_tuple_of_images(mugshot_paths)
        self.rendered_row = self.render_row(0)
        self.x = self.get_screen_centered_x()
        self.y = SCREEN_SIZE[1] - self.rendered_row.get_height()
        self.current_row = 0
        self.current_slot = 0
        self.cursor = RosterCursor((self.x, self.y))
        self.scroll_up_arrow = RosterArrow(ArrowType.UP, self.x, self.y,
                                           self.rendered_row.get_width(),
                                           self.rendered_row.get_height())
        self.scroll_down_arrow = RosterArrow(ArrowType.DOWN, self.x, self.y,
                                             self.rendered_row.get_width(),
                                             self.rendered_row.get_height())

    def render_row(self, row_index):
        """Render a row of mugshots in order from the mugshot list.

        Args:
            row_index: An integer for the index of the row that will be
                rendered. For example, given that SLOTS_PER_ROW is 5,
                passing 1 would render mugshots of index 5 through 9.
        """
        row_surf = Surface((self.slot_size() * self.SLOTS_PER_ROW,
                            self.slot_size()))
        slot_x = 0

        first_slot = row_index * self.SLOTS_PER_ROW
        last_slot = first_slot + self.SLOTS_PER_ROW

        for slot_index in xrange(first_slot, last_slot + 1):
            if slot_index <= len(self.mugshots) - 1:
                new_slot = self.render_slot(slot_index)
            else:
                new_slot = self.render_slot(-1)
            row_surf.blit(new_slot, (slot_x, 0))

            slot_x += self.slot_size()

        return row_surf

    def render_slot(self, slot_index):
        """Render one of the character's mugshots and place it within a
        frame.

        Alternatively, a blank slot with just a frame and background can
        be rendered.

        Args:
            slot_index: The index of the character's mugshot within
                mugshot_paths. Passing a value less than 0 will create
                a blank slot.

        Returns:
            A Surface containing a framed mugshot, if slot_index is 0 or
            more. Otherwise, a Surface with a blank slot is returned.
        """
        slot_surf = Surface((self.slot_size(), self.slot_size()))

        # Background.
        pygame.draw.rect(slot_surf, self.BACKGROUND_COLOR,
                         Rect(self.FRAME_THICKNESS, self.FRAME_THICKNESS,
                              self.MUGSHOT_SIZE, self.MUGSHOT_SIZE))

        # Mugshot.
        if slot_index >= 0:
            mugshot = self.mugshots[slot_index]
            slot_surf.blit(mugshot, (self.FRAME_THICKNESS, self.FRAME_THICKNESS))

        # Frame.
        pygame.draw.rect(slot_surf, self.FRAME_COLOR,
                         Rect(0, 0,
                              self.slot_size() - 1, self.slot_size() - 1),
                         self.FRAME_THICKNESS)
        return slot_surf

    def slot_size(self):
        """Return an integer for the length and width, in pixels, of
        a character slot (mugshot + frame).
        """
        return self.MUGSHOT_SIZE + (self.FRAME_THICKNESS * 2)

    def get_screen_centered_x(self):
        """Return an integer for the x-position that will center the
        roster on the screen.
        """
        return (SCREEN_SIZE[0] - self.rendered_row.get_width()) / 2


class RosterCursor(Animation):
    """An animated cursor that is used to mark the currently-selected
    character within the roster.

    The cursor can toggle between two different animations with
    identical dimensions; use this to signify which player is currently
    choosing.

    Class Constants:
        P1_SPRITESHEET: A String for the file path to player 1's cursor
            animation.
        P2_SPRITESHEET: A String for the file path to player 2's cursor
            animation.
        FRAME_AMOUNT: An integer for the amount of frames in each
            Animation.
        FRAME_DURATION: An integer for the duration, in update cycles,
            of each animation frame.

    Attributes:
        p1_image: A Surface containing player 1's spritesheet image.
        p2_image: A Surface containing player 2's spritesheet image.
    """
    P1_SPRITESHEET = 'images/p1_character_cursor.png'
    P2_SPRITESHEET = 'images/p2_character_cursor.png'
    FRAME_AMOUNT = 2
    FRAME_DURATION = 8

    def __init__(self, position):
        """Declare and initialize instance variables.

        Args:
            position: A tuple of two integers which represent the x
                and y-positions of the cursor relative to ths screen.
        """
        super(RosterCursor, self).__init__(self.P1_SPRITESHEET, position,
                                           self.FRAME_AMOUNT,
                                           self.FRAME_DURATION)
        self.p1_image = pygame.image.load(self.P1_SPRITESHEET)
        self.p1_image = convert_to_colorkey_alpha(self.p1_image)
        self.p2_image = pygame.image.load(self.P2_SPRITESHEET)
        self.p2_image = convert_to_colorkey_alpha(self.p2_image)

    def toggle_player(self):
        """Switch to the other player's cursor animation."""
        if self.filepath == self.P1_SPRITESHEET:
            self.filepath = self.P2_SPRITESHEET
            self.image = self.p2_image
        else:
            self.filepath = self.P1_SPRITESHEET
            self.image = self.p1_image


class RosterArrow(Animation):
    """An animated arrow that notifies the players of a direction in
    which the character roster can be scrolled.

    Class Constants:
        SPRITESHEET: A String for the file path to the animation
            spritesheet.
        FRAME_AMOUNT: An integer for the number of frames in the
            animation.
        FRAME_DURATION: An integer for the duration, in update cycles,
            of each animation frame.
        ROSTER_DISTANCE: An integer for the distance, in pixels, of this
            arrow from the edge of the roster.
    """
    SPRITESHEET = 'images/roster_up_arrow.png'
    FRAME_AMOUNT = 2
    FRAME_DURATION = 10
    ROSTER_DISTANCE = 18

    def __init__(self, arrow_type, roster_x, roster_y, roster_width,
                 roster_height):
        """Declare and initialize instance variables.

        Args:
            arrow_type: An integer value from the ArrowType enum. This
                is used to specify the direction the arrow points.
            roster_x: An integer for the x-position of the roster
                relative to the screen.
            roster_y: An integer for the y-position of the roster
                relative to the screen.
            roster_width: An integer for the width of the roster, in
                pixels.
            roster_height: An integer for the height of the roster, in
                pixels.
        """
        super(RosterArrow, self).__init__(self.SPRITESHEET, (0, 0),
                                          self.FRAME_AMOUNT,
                                          self.FRAME_DURATION)
        self.correct_position(arrow_type, roster_x, roster_y,
                              roster_width, roster_height)
        if arrow_type == ArrowType.DOWN:
            self.flip(is_vertical=True)

    def correct_position(self, arrow_type, roster_x, roster_y,
                         roster_width, roster_height):
        """Move the arrow into the correct position beside the roster.

        If the arrow points up, it will be on the left edge; it it
        points down, it will be on the right edge.

        Args:
            arrow_type: An integer value from the ArrowType enum. This
                is used to specify the direction the arrow points.
            roster_x: An integer for the x-position of the roster
                relative to the screen.
            roster_y: An integer for the y-position of the roster
                relative to the screen.
            roster_width: An integer for the width of the roster, in
                pixels.
            roster_height: An integer for the height of the roster, in
                pixels.
        """
        y = roster_y + ((roster_height - self.image.get_height()) / 2)

        if arrow_type == ArrowType.UP:
            x = roster_x - self.frame_width - self.ROSTER_DISTANCE
            self.move(x, y)
        if arrow_type == ArrowType.DOWN:
            x = roster_x + roster_width + self.ROSTER_DISTANCE
            self.move(x, y)


class ArrowType(object):
    """An enumeration for the types of roster scroll arrows.

    Attributes:
        UP: An integer value representing an arrow pointing up.
        DOWN: An integer value representing an arrow pointing down.
    """
    UP = 0
    DOWN = 1


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
        NAME_OFFSET: An integer for the vertical shift up, in pixels,
            of the name text from the bottom of the character sprite.
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
    NAME_OFFSET = 6
    SHADOW_HEIGHT = 14
    SHADOW_COLOR = (0, 5, 90)
    OFFSET_FROM_SHADOW = 4

    def __init__(self, is_facing_left, spritesheet, name, name_font,
                 frame_durations):
        """Declare and initialize instance variables.

        Args:
            is_facing_left: A Boolean indicating whether the character
                is facing to the left, rather than to the right (which
                is the default direction for characters in this game).
            spritesheet_path: A Surface containing the character
                animation's spritesheet image.
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
                                            spritesheet, frame_durations)
        self.name_font = name_font
        self.name = render_outlined_text(name_font, name, self.NAME_COLOR,
                                         self.NAME_OUTLINE_COLOR)
        self.shadow = self.render_shadow()
        self.x = 0
        self.y = self.calculate_y_position()

        if is_facing_left:
            self.correct_position()

    def change_character(self, spritesheet, name, frame_durations):
        """Display a different character animation.

        Args:
            spritesheet_path: A Surface containing the character
                animation's spritesheet image.
            name: A String for the character's name.
            frame_durations: A tuple of integers containing the
                duration, in update cycles, of each animation frame in
                order. For example, passing (10, 8, 5) means that the
                first animation frame is shown for 10 update cycles,
                the second frame for 8 update cycles, and so on.
        """
        self.animation.change_animation(spritesheet, frame_durations)
        self.name = render_outlined_text(self.name_font, name,
                                         self.NAME_COLOR,
                                         self.NAME_OUTLINE_COLOR)
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

    def draw(self, parent_surf):
        """Draw the CharacterPreview onto a Surface.

        parent_surf: The Surface upon which the preview will be drawn.
        """
        self.draw_shadow(parent_surf)
        self.animation.draw(parent_surf, self.x, self.y)
        self.draw_name(parent_surf)

    def draw_shadow(self, parent_surf):
        """Draw the shadow at the character's feet (or, where their
        feet would be in case they're feetless).

        Args:
            parent_surf: The Surface upon which the shadow will be
                drawn.
        """
        char_bottom = self.y + self.animation.get_height()
        y = char_bottom - self.shadow.get_height() + self.OFFSET_FROM_SHADOW
        parent_surf.blit(self.shadow, (self.x, y))

    def draw_name(self, parent_surf):
        """Draw the character's name at the bottom of their sprite.

        Args:
            parent_surf: The Surface upon which the name will be drawn.
        """
        if self.name.get_width() < self.animation.get_width():
            x = self.get_centered_x(self.name.get_width())
        elif self.is_facing_left:
            x = self.x + self.animation.get_width() - self.name.get_width()
        else:
            x = self.x
        y = self.y + self.animation.get_height() - self.NAME_OFFSET
        parent_surf.blit(self.name, (x, y))

    def get_centered_x(self, width):
        """Calculate an x-value that would allow a Surface of a given
        width to be centered relative to the character sprite.

        Note that this only works with Surfaces that have a smaller
        width than the character.

        Args:
            width: An integer for the width of a Surface.
        """
        surface_difference = self.animation.get_width() - width
        return self.x + int(surface_difference / 2)

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
