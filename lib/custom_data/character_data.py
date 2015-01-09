"""All classes in this module are read-only data classes and should not
have their values modified after being loaded from external files.

This module also contains various methods for retrieving data from these
classes.
"""
import pygame
from pygame.locals import Rect


def load_frame_durations(action):
    """Return a tuple containing tuples of ints, for the duration of
    each frame within the specified Action.

    Args:
        action: The Action that will be read.
    """
    frame_durations = []

    for frame in action.frames:
        frame_durations.append(frame.duration)

    return tuple(frame_durations)


class CharacterData(object):
    """A data class that stores all of the required information for a
    playable character.
    The information is retrieved from XML files, which are created with
    the Character Editor program and loaded via the CharacterLoader
    class.
    
    Attributes:
        name                The character's given name, as it will
                            appear in-game. Due to screen space, it
                            should not exceed 20 characters.
        speed               The speed, given in pixels/second, that the
                            character moves at while walking.
        stamina             The character's starting health. Taking
                            damage will reduce it based on the 'damage'
                            value of the colliding hitbox. Reducing it
                            to 0 means a K.O.
        stun_threshold      The amount of dizzy stun the character can
                            endure before becoming dizzy.
        mugshot_path        The filepath for the character's face
                            image, which will appear on the
                            Character Selection screen. All mugshots
                            are kept in the characters folder, so
                            'characters/' is omitted from this String.
        action_list         A List of all of the Actions that the
                            character can perform.
        default_actions     A Dictionary containing the names for all
                            of the types of Actions that are universal
                            for every character, such as walking, and
                            the index numbers of the corresponding
                            Actions for this character.
                            e.g. walk => 0 (The first Action listed in
                                            the character's XML file.)
                                 stand => 2 (The third Action listed.)
        """
    def __init__(self):
        self.name = ""
        self.speed = 0
        self.stamina = 0
        self.stun_threshold = 0
        self.mugshot_path = ""
        self.action_list = []
        self.default_actions = {}


class Action(object):
    """Represents a possible action that the character can perform.
    This can be a basic utility, such as walking or jumping, or an
    attack sequence.

    Attributes:
        name                    An identifier for the Action. This is
                                only displayed in the Character Editor.
                                (Note that the game engine identifies
                                 Actions by the order they were listed
                                 in the XML file.)
        spritesheet_path        The filepath for the animation's sprite
                                sheet. All sprite sheets are kept in
                                the characters folder, so 'characters/'
                                is omitted from this String.
        frame_width             The width of all frames in the sprite
                                sheet. All frames should have uniform
                                dimensions and be ordered from left-to-
                                right in order to display correctly.
        frame_height            The height of all frames in the sprite
                                sheet.
        x_offset                If this Action is the character's
                                neutral pose, this value will tell the
                                engine how far to shift the character
                                horizontally when the character changes
                                direction. This is to keep the
                                character's feet in the same position,
                                in case the sprite is unbalanced on one
                                side. (e.g. They're holding a sword
                                that extends far to the right.)
                                For any other Action, this value will
                                shift the character horizontally to
                                keep their feet in the same position
                                relative to the neutral pose.
        condition               The condition the character needs to be
                                in in order to execute this Action.
                                This can be Standing/Walking, Crouching,
                                or Jumping/In-the-Air.
        is_multi_hit            Normally, attacks will only hit once
                                and then ignore all Hitboxes in
                                subsequent Frames. If this is set to
                                True, all of the Frames in this Action
                                will be allowed to have one of their
                                Hitboxes land. (They are treated as
                                separate hits and thus count towards
                                the combo total.)
        input_priority          When the player inputs buttons, the
                                engine will search each Action's inputs
                                List to see if they match the last
                                sequence of buttons. Certain Actions
                                will have parts of their input
                                sequences that match parts of others.
                                (e.g. Light Punch: [light_punch]
                                      Fireball: down => forward =>
                                                [light_punch])
                                When this happens, the Action with the
                                highest input_priority will be the one
                                that executes.
        meter_gain              When this Action executes, this amount
                                is added to the player's Special Gauge.
                                The Gauge's maximum is 100.
        meter_needed            The amount of points in the player's
                                Special Gauge that are required to
                                perform this Action. When it is being
                                executed, this amount is deducted from
                                the Gauge.
        proximity               The Action will only be executed if the
                                opponent has at least one Hurtbox that
                                are this many pixels away, or less,
                                from the character's closest Hurtbox.
                                If this is 0, the Action can be
                                performed from any distance. Note that
                                Actions with a proximity limit have a
                                higher input priority than those that
                                don't.
        start_counter_frame     If this Action is a Counter-type move,
                                the animation will skip to the Frame of
                                this index value, if one of the
                                character's Hurtboxes is struck in one
                                of the previous Frames.
                                If the character is not hit before the
                                prior Frames are finished animating,
                                the subsequent Frames are ignored.
                                0 means that the Action isn't a
                                Counter attack.
        frames                  A List of all animation Frames within
                                this Action.
        input_list              A List detailing the required button
                                sequence needed to perform this Action.
    """
    def __init__(self):
        self.name = ""
        self.spritesheet_path = ""
        self.frame_width = 0
        self.frame_height = 0
        self.x_offset = 0
        self.condition = 0
        self.is_multi_hit = False
        self.input_priority = 1
        self.meter_gain = 0
        self.meter_needed = 0
        self.proximity = 0
        self.start_counter_frame = 0
        self.frames = []
        self.input_list = []


class InputStep(object):
    """To perform an Action, a specific sequence of buttons have to be
    pressed in a certain order. This class represents a single step in
    that sequence, containing all of the buttons required in that step.

    Attributes:
        buttons     A List containing the names of buttons that must be
                    pressed during this step.
    """
    def __init__(self):
        self.buttons = []


class Frame(object):
    """An animation frame. Actions and Projectiles generally consist of
    several of these objects. On sprite sheets, they are represented as
    'cells' that have a uniform width and height and are ordered from
    left-to-right.

    Attributes:
        duration            The amount of time to display this Frame
                            before moving onto the next. This is
                            measured in the unit of 'frames' which,
                            in this game, means 1 frame/60 seconds.
                            For example, to have this Frame displayed
                            for a full second, this value should be 60.
        cancelable          If this is set to 1, the player can
                            interrupt this Frame to start another
                            Action.
                            If it is to 2, the player can interrupt it,
                            but only if one of the Hitboxes in this
                            Frame strikes the opponent.
                            (For most Default Actions, this value is
                            ignored.)
        move_x              The horizontal distance, in pixels, that
                            the character will move over the entire
                            duration of this Frame.
        move_y              The vertical distance to move the
                            character.
        hurtboxes           A List of all Hurtboxes contained in this
                            Frame.
        hitboxes            A List of all Hitboxes contained in this
                            Frame.
        projectiles         A List of all Projectiles that are created
                            from this Frame.
    """
    def __init__(self):
        self.duration = 0
        self.cancelable = 0
        self.move_x = 0
        self.move_y = 0
        self.hurtboxes = []
        self.hitboxes = []
        self.projectiles = []


class CollisionBox(object):
    """A rectangular area that is located somewhere on a Frame. This is
    an abstract class that Hurtbox and Hitbox are derived from.

    Attributes:
        rect        Contains the box's offset relative to the
                    character, as well as its dimensions.
    """

    def __init__(self):
        self.rect = Rect(0, 0, 0, 0)


class Hurtbox(CollisionBox):
    """A rectangular space located on a Frame that represents the
    character's vulnerable areas. If it collides with a Hitbox from the
    opponent or a hazardous Projectile, the character will take damage.

    Attributes:
        rect        Contains the Hurtbox's offset relative to the
                    character, as well as its dimensions.
    """


class Hitbox(CollisionBox):
    """A rectangular space on a Frame that represents the harmful areas
    of a Character or Projectile. If a character's Hurtbox collides
    with it, that character takes damage.

    Attributes:
        rect                Contains the Hitbox's offset relative to
                            the character, as well as its dimensions.
        damage              The amount of stamina lost by the colliding
                            character. If unblocked, the character
                            loses the full amount. If blocked, they
                            lose a fraction of the value instead.
        hitstun             The amount of time, in frames, in which the
                            colliding character recoils and is unable
                            to act. This is only applied if the attack
                            was unblocked.
        blockstun           If the attack was blocked, the character
                            will be trapped in the blocking animation
                            for this number of frames.
                            (For balancing purposes, this value should
                            always be less than the one for hitstun.)
        knockback           The distance, in pixels, that the colliding
                            character will be pushed back on the
                            horizontal plane.
        dizzy_stun          The amount of Dizzy Stun the character
                            receives if the attack was unblocked.
        effect              Specifies an additional effect on the
                            colliding character if they don't block the
                            attack.
                            If it is set to 1, the character trips. If
                            it is set to 2, they will be launched into
                            the air.
        can_block_high      If this value is False, the Hitbox cannot
                            be blocked while standing or in the air.
        can_block_low       If this value is False, the Hitbox cannot
                            be blocked while crouching.
    """
    def __init__(self):
        super(Hitbox, self).__init__()
        self.damage = 0
        self.hitstun = 0
        self.blockstun = 0
        self.knockback = 0
        self.dizzy_stun = 0
        self.effect = 0
        self.can_block_high = False
        self.can_block_low = False


class ProjectileData(object):
    """A damaging weapon that can be thrown by the character. It can be
    anything, from fireballs to bullets to stone bricks.

    Projectiles are separate entities that travel across the stage
    independent of the character who fired them. They have their own
    animation that contains their own set of Frames and Hitboxes. Most
    of this data is kept in separate Projectile XML files that are
    referenced by the Character's main XML file.
    Once they are generated from a character's Frame, they will begin
    to act on their own based on this data.

    Attributes:
        name                    An identifier for the Projectile. Only
                                displayed within the Character Editor.
        rect                    Contains the Projectile's initial
                                offset relative to the character, as
                                well as its Frame dimensions.
        x_speed                 The speed at which the Projectile
                                travels across the screen horizontally.
        y_speed                 The projectile's vertical speed.
        spritesheet_path        The filepath for the Projectile's
                                sprite sheet. These are always kept in
                                the characters folder, so 'characters/'
                                is omitted from this String.   
        stamina                 When the Projectile collides with an
                                opposing Projectile, it will lose
                                stamina equal to the other Projectile's
                                stamina value.
                                If its stamina drops to 0, it is
                                cancelled out.
        first_loop_frame        Any Frames preceding the one with this
                                index will only play once as a start-up
                                animation. All of the Frames from this
                                one, up until the one preceding the
                                Frame marked by first_collision_frame,
                                will play in a loop as long as the
                                Projectile is on-screen and hasn't hit
                                anything yet.
        first_collision_frame   When the Projectile collides with the
                                opponent or loses all of its stamina,
                                the animation will skip to the Frame at
                                this index.
        frames                  A List of the Frames that make up the
                                Projectile's animation. They can
                                contain several Hitboxes, but no
                                Hurtboxes.
    """
    def __init__(self):
        self.name = ""
        self.rect = Rect(0, 0, 0, 0)
        self.x_speed = 0
        self.y_speed = 0
        self.spritesheet_path = ""
        self.stamina = 0
        self.first_loop_frame = 0
        self.first_collision_frame = 0
        self.frames = []