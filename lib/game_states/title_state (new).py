import sys
from __builtin__ import range
import pygame
from pygame.locals import *
from pygame.mixer import Sound
from pygame.font import Font
from pygame.color import Color
from lib.globals import SCREEN_SIZE
from lib.globals import FRAME_RATE
from lib.graphics import Graphic
from lib.graphics import Animation
from lib.game_states.state import *
from lib.game_states.state_ids import StateIDs


class OptionList(object):
    """Contains various Options that the players can scroll through and
    confirm.

    This is an abstract class; subclasses should implement their own
    ways of responding to a confirmed Option.

    Class Constants:
        CONFIRM_DURATION: The time, in update frames, to flash a
            confirmed Option's text before performing the appropriate
            operation.

    Attributes:
        state: The TitleState instance that this OptionList belongs to.
        options: A list of Options.
        selected_option: The index of the Option currently being
            highlighted by the players.
        x: An integer coordinate for the OptionList's x-position
            relative to the screen.
        y: An integer coordinate for the OptionList's y-position
            relative to the screen.
        sfx_confirm: A PyGame Sound that plays when the players confirm
            an option.
        sfx_cancel: A PyGame Sound that plays when the players leave
            this OptionList or otherwise cancel a decision.
        sfx_scroll: A PyGame Sound that plays when the players scroll
            through the list of Options.
        confirm_timer: An integer counter that keeps track of how long
            a confirmed Option has been flashing. Setting it to -1 will
            stop the timer.
    """
    pass


class Option(object):
    """An option that the players can select within the Title State.

    It is represented by a text name on the screen, which can be
    recolored or hidden to indicate player selection or confirmation.

    Class Constants:
        NORMAL_COLOR: A String name for the regular color of an Option.
        HIGHLIGHT_COLOR: A String name for the color of an Option when
            it is selected by the users.
        FONT_PATH: A String for the file path to the font file that
            will be used in rendering graphical text for Options.
        FONT_SIZE: An integer size of the font used in rendering Option
            text.

    Attributes:
        text: The text String that describes this Option. It will be
            written on the screen.
        x: An integer value for the Option text's x-coordinate relative
            to the screen.
        y: An integer value for the Option text's y-coordinate relative
            to the screen.
        is_visible: A Boolean indicating whether the text will be
            drawn onto its parent Surface.
        font: The PyGame Font object that stores the font used in
            rendering text.
        surf: The text graphic will be rendered onto this PyGame
            Surface.
    """
    NORMAL_COLOR = 'white'
    HIGHLIGHT_COLOR = 'dark gray'
    FONT_PATH = 'fonts/fighting-spirit-TBS.ttf'
    FONT_SIZE = 18

    def __init__(self, text, x, y):
        """Declare and initialize instance variables.

        Args:
            text: The String that describes this option.
            x: An integer value for the Option text's x-coordinate
                relative to the screen.
            y: An integer value for the Option text's y-coordinate
                relative to the screen.
        """
        self.text = text
        self.x = x
        self.y = y
        self.is_visible = True
        self.font = Font(self.FONT_PATH, self.FONT_SIZE)
        self.surf = self.render_text(text, self.NORMAL_COLOR)

    def render_text(self, text, color_name):
        """Create a new Surface with the specified text, using the
        font specifications defined by this class.

        Args:
            text: The String of text that will be drawn.
            color_name: A String containing the name or hex code of the
                color of the text.

        Returns:
            A Surface with the text drawn onto it.
        """
        text_color = Color(color_name)
        return self.font.render(text, True, text_color)

    def highlight(self):
        """Redraw the text with an alternate color."""
        self.surf = self.render_text(self.text, self.HIGHLIGHT_COLOR)

    def unhighlight(self):
        """Redraw the text with normal coloration."""
        self.surf = self.render_text(self.text, self.NORMAL_COLOR)

    def get_height(self):
        """Return the integer height of the text graphic."""
        return self.surf.get_height()

    def draw(self, parent_surf):
        """Draw the text onto a Surface.

        The text will only be shown if the is_visible attribute is set
        to True.

        Args:
            parent_surf: The Surface upon which the text will be drawn.
        """
        if self.is_visible:
            parent_surf.blit(self.surf, (self.x, self.y))


class BattleSetting(Option):
    """One of the parameters required for setting up a battle.

    Aside from being a selectable Option, it also contains its own list
    of numerical values that the players can scroll through.

    Class Constants:
        VALUE_X: The integer coordinate for the x-position of value
            text relative to the screen.
        LEFT_ARROW_PATH: A String for the file path to the scroll left
            arrow image.
        ARROW_DISTANCE: An integer for the horizontal distance between
            each scroll arrow and the text for the selected value.
        ARROW_Y_OFFSET: The integer distance, in pixels, between the
            the top of the text graphic and the top of each scroll
            arrow.

    Attributes:
        values: A list of integer values that can be set for this
            BattleSetting.
        value_index: An integer for the index of the currently-selected
            value.
        value_surf: A PyGame Surface that contains the text graphic
            for the currently-selected value.
        scroll_left_arrow: A Graphic that displays the image of the
            'scroll values left' arrow.
        scroll_right_arrow: A Graphic that displays the image of the
            'scroll values right' arrow.
    """
    VALUE_X = 248
    LEFT_ARROW_PATH = 'images/battle_setup_arrow_left.png'
    ARROW_DISTANCE = 7
    ARROW_Y_OFFSET = 5

    def __init__(self, text, x, y, *values):
        """Declare and initialize instance variables.

        Args:
            text: The String that describes this BattleSetting.
            x: The integer coordinate for the text's x-position relative
                to the screen.
            y: The integer coordinate for the text's y-position relative
                to the screen.
            values: All of the integer values that can be set for this
                BattleSetting.
        """
        super(BattleSetting, self).__init__(text, x, y)
        self.values = values
        self.value_index = 0
        self.value_surf = self.render_text(self.value_index,
                                           self.NORMAL_COLOR)
        self.scroll_left_arrow = Graphic(self.LEFT_ARROW_PATH,
            (self.VALUE_X - self.ARROW_DISTANCE,
             self.y + self.ARROW_Y_OFFSET))
        self.scroll_right_arrow = Graphic(self.LEFT_ARROW_PATH,
            (self.VALUE_X + self.value_surf.get_width() + self.ARROW_DISTANCE,
            self.y + self.ARROW_Y_OFFSET))
        self.scroll_right_arrow.flip(is_horizontal=True)

    def scroll_values_left(self):
        """Select the previous value for this BattleSetting."""
        if self.value_index > 0:
            self.value_index -= 1
            self.value_surf = self.render_text(
                self.values[self.value_index], self.HIGHLIGHT_COLOR)

    def scroll_values_right(self):
        """Select the next value for this BattleSetting."""
        if self.value_index < len(self.values) - 1:
            self.value_index += 1
            self.value_surf = self.render_text(
                self.values[self.value_index], self.HIGHLIGHT_COLOR)

    def highlight(self):
        """Redraw the text with an alternate color."""
        super(BattleSetting, self).highlight()
        self.value_surf = self.render_text(
            self.values[self.value_index], self.HIGHLIGHT_COLOR)

    def unhighlight(self):
        """Redraw the text with normal coloration."""
        super(BattleSetting, self).unhighlight()
        self.value_surf = self.render_text(
            self.values[self.value_index], self.NORMAL_COLOR)

    def get_value(self):
        """Return the selected value."""
        return self.values[self.value_index]

    def draw(self, parent_surf):
        """Draw the text onto a Surface.

        Args:
            parent_surf: The Surface upon which the BattleSetting text
                will be drawn.
        """
        super(BattleSetting, self).draw(parent_surf)
        parent_surf.blit(self.value_surf, (self.VALUE_X,
                                           self.y + self.ARROW_Y_OFFSET))

    def draw_scroll_arrows(self, parent_surf):
        """Draw the scroll value arrows onto a Surface.

        The left arrow will only be shown if there are values preceding
        the one that is selected. Likewise, the right arrow will only
        be shown if there are subsequent values.

        Args:
            parent_surf: The Surface upon which the arrows will be
                drawn.
        """
        if self.value_index > 0:
            self.scroll_left_arrow.draw(parent_surf)
        if self.value_index < len(self.values) - 1:
            self.scroll_right_arrow.draw(parent_surf)