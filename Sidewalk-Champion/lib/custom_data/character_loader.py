import os.path
import xml.etree.ElementTree as tree
from pygame.rect import Rect
from lib.custom_data.xml_ops import *
from lib.custom_data.character_data import *

class CharacterLoader(object):
    """Loads character data from XML files and stores them in
    CharacterData objects that can be read by the game engine.

    Attributes:
        CHARACTER_VERIFY_CODE       The correct verification code for
                                    character files that are properly
                                    formatted.
        PROJECTILE_VERIFY_CODE      The correct verification code for
                                    projectile files that are properly
                                    formatted.
        CHARACTER_LIST_PATH         The filepath for the text file
                                    which lists the paths to all of the
                                    characters' XML files.
                                    The paths are separated by a
                                    new-line.
        DEFAULT_ACTION_NAMES        A List of names for all of the
                                    Default Actions, which are types of
                                    Actions that are universal across
                                    all characters, such as walking and
                                    blocking.
    """
    # Initialize
    def __init__(self):
        self.CHARACTER_VERIFY_CODE = "dfh943ooJLM3"
        self.PROJECTILE_VERIFY_CODE = "f849udjQMoh7"
        self.CHARACTER_LIST_PATH = "characters/character_list.txt"
        self.DEFAULT_ACTION_NAMES = self.create_default_names()

    def create_default_names(self):
        """Return a List of names for all of the Default Actions."""
        default_names = ['intro',
                        'stand',
                        'walk',
                        'crouch_down',
                        'crouching_idle',
                        'jump_up',
                        'jump_forward',
                        'jump_back',
                        'block_standing',
                        'block_high',
                        'block_low',
                        'standing_recoil',
                        'crouching_recoil',
                        'jumping_recoil',
                        'tripped',
                        'launched',
                        'falling',
                        'knockdown',
                        'recover',
                        'dizzy',
                        'chip_ko',
                        'victory']
        return default_names

    # Error Checking
    def has_all_default_names(self, default_actions):
        """Return False if any of the Default Action names are
        missing from the specified Dictionary's keys.

        Keyword arguments:
            default_actions     The Dictionary to check.
        """
        for name in self.DEFAULT_ACTION_NAMES:
            if name not in default_actions:
                return False

        return True

    # Load All Characters
    def load_all_characters(self):
        """Load the data from all of the XML files specified in the
        character_list file, and return it as a List of CharacterData
        objects.
        """
        character_list = []
        xml_paths = self.get_character_paths()

        for character_path in xml_paths:
            if is_valid_xml('characters/' + character_path,
                            self.CHARACTER_VERIFY_CODE,
                            'character') == True:
                new_character = self.load_character_data(character_path)

                # None is returned if there was an error reading the file.
                # If that happens, the current character won't be added and
                # the function will skip to the next character.
                if new_character != None:
                    character_list.append(new_character)

        return character_list

    def get_character_paths(self):
        """Return a List of all of the filepaths to the XML files for
        playable characters.
        """
        with open(self.CHARACTER_LIST_PATH) as f:
            character_path_list = [line.rstrip('\n') for line in f]
            return character_path_list

    # Load all Elements of a specific type.
    def load_default_actions(self, character_element):
        """Retrieve the names of all default actions as well as the
        indexes for the character's corresponding Actions and return
        them as a Dictionary.

        Keyword arguments:
            character_element   An XML element containing data for a
                                playable character. It should contain
                                a default_actions element.
        """
        default_list = {}
        default_element = character_element.find('default_actions')

        for default_action in default_element:
            default_list.update({default_action.tag:default_action.text})

        return default_list

    def load_all_actions(self, character_element):
        """Load all action elements from a character XML element and
        return them as a List of Action objects.
        Return None if any of the action elements have errors.
        
        Keyword arguments:
            character_element   The character XML element that
                                contains loadable action data.
        """
        all_actions = []

        for action_element in character_element.findall('action'):
            new_action = self.load_action(action_element)
            all_actions.append(new_action)

        # All characters must have at least one Action, so there would be an
        # error if the XML file doesn't have any.
        if len(all_actions) < 1:
            return None

        # If any of the Actions are None, there must have been an error
        # loading data from one or more of the elements.
        if has_null_items_in_list(all_actions) == True:
            return None

        return all_actions

    def load_all_inputs(self, action_element):
        """Load all of the input steps and their containing buttons
        and return them as a List of InputStep objects.

        Keyword arguments:
            action_element  The action XML element that contains an
                            input_list element.
        """
        inputs = []
        input_list_element = action_element.find('input_list')

        for input_step_element in input_list_element:
            new_input_step = InputStep()

            for input_element in input_step_element:
                button_name = input_element.text
                new_input_step.buttons.append(button_name)

            inputs.append(new_input_step)

        return inputs

    def load_all_frames(self, parent_element):
        """Load all frame elements from an action XML element and
        return them as a List of Frame objects.
        Return None if any of the hurtbox elements have errors.
        
        Keyword arguments:
            parent_element  The action or projectile XML element that
                            contains loadable frame data.
        """
        all_frames = []
        
        for frame_element in parent_element.findall('frame'):
            new_frame = self.load_frame(frame_element)
            all_frames.append(new_frame)

        # Like Characters and Actions, Actions and Projectiles have to have at
        # least one Frame to them. (Otherwise, how would they animate?)
        if len(all_frames) < 1:
            return None

        if has_null_items_in_list(all_frames) == True:
            return None

        return all_frames

    def load_all_hurtboxes(self, frame_element):
        """Load all hurtbox elements from a frame XML element and
        return them as a List of Hurtbox objects.
        Return None if any of the hurtbox elements have errors.
        
        Keyword arguments:
            frame_element   The frame XML element that contains
                            loadable hurtbox data.
        """
        all_hurtboxes = []

        for hurtbox_element in frame_element.findall('hurtbox'):
            new_hurtbox = self.load_hurtbox(hurtbox_element)
            all_hurtboxes.append(new_hurtbox)

        # Note that it is possible for a Frame to not have any hurtboxes.
        # (This also applies to hitboxes and projectiles.)

        if has_null_items_in_list(all_hurtboxes) == True:
            return None

        return all_hurtboxes

    def load_all_hitboxes(self, frame_element):
        """Load all hitbox elements from a frame XML element and
        return them as a List of Hitbox objects.
        Return None if any of the hitbox elements have errors.
        
        Keyword arguments:
            frame_element   The frame XML element that contains
                            loadable hitbox data.
        """
        all_hitboxes = []

        for hitbox_element in frame_element.findall('hitbox'):
            new_hitbox = self.load_hitbox(hitbox_element)
            all_hitboxes.append(new_hitbox)

        if has_null_items_in_list(all_hitboxes):
            return None

        return all_hitboxes

    def load_all_projectiles(self, frame_element):
        """Load all projectile elements from a frame XML element and
        return them as a List of Projectile objects.
        Return None if any of the projectile elements have errors.
        
        Keyword arguments:
            frame_element   The frame XML element that contains
                            loadable projectile data.
        """
        all_projectiles = []

        for projectile_element in frame_element.findall('projectile'):
            new_projectile = self.load_projectile_data(projectile_element)
            all_projectiles.append(new_projectile)

        if has_null_items_in_list(all_projectiles) == True:
            return None

        return all_projectiles

    # Load individual Elements.
    def load_character_data(self, xml_path):
        """Retrieve character data from the specified XML file and
        return it as a CharacterData object.
        Return None instead if there is an error loading data.

        Keyword arguments:
            xml_path    The filepath to the character's XML data file.
        """
        character = CharacterData()
        character_element = load_xml('characters/' + xml_path, 'character')
        # Immediately return an error if the XML file lacks a 'character' root
        # element.
        if character_element == None:
            return None

        character.name = character_element.get('name')
        character.stamina = character_element.get('stamina')
        character.speed = character_element.get('speed')
        character.stun_threshold = character_element.get('stun_threshold')
        character.mugshot_path = character_element.get('mugshot')
        character.action_list = self.load_all_actions(character_element)
        character.default_actions = self.load_default_actions(
            character_element)
        
        # If an attribute in the element couldn't be found, None is returned.
        # If any of the character's attributes are None, the XML file must
        # have been missing important attributes. In this case, None should be
        # returned to indicate an error and not have the character loaded into
        # the game.
        if has_null_attributes(character) == True:
            return None

        # Values from XML tags are read as Strings, so numeric values have to
        # be explicitly converted to integers.
        # However, an exception is raised if the argument passed to int() is
        # None, so the conversion is only done after the attribute check
        # above.
        character.stamina = int(character.stamina)
        character.speed = int(character.speed)
        character.stun_threshold = int(character.stun_threshold)

        if self.has_all_default_names(character.default_actions) == False:
            return None

        return character

    def load_action(self, action_element):
        """Retrieve action data from the specified action XML element
        and return it as an Action object.
        Return None instead if there is an error loading data.

        Keyword arguments:
            action_element  The XML element containing action data.
        """
        action = Action()

        action.name = action_element.get('name')
        action.spritesheet_path = action_element.get('filepath')
        action.frame_width = action_element.get('width')
        action.frame_height = action_element.get('height')
        action.x_offset = action_element.get('x_offset')
        action.condition = action_element.get('condition')
        action.is_multi_hit = action_element.get('multi_hit')
        action.input_priority = action_element.get('priority')
        action.meter_gain = action_element.get('meter_gain')
        action.meter_needed = action_element.get('meter_needed')
        action.proximity = action_element.get('proximity')
        action.start_counter_frame = action_element.get('start_counter_frame')
        action.frames = self.load_all_frames(action_element)
        action.input_list = self.load_all_inputs(action_element)

        if has_null_attributes(action) == True:
            return None

        action.frame_width = int(action.frame_width)
        action.frame_height = int(action.frame_height)
        action.x_offset = int(action.x_offset)
        action.condition = int(action.condition)
        action.is_multi_hit = int(action.is_multi_hit)
        action.input_priority = int(action.input_priority)
        action.meter_gain = int(action.meter_gain)
        action.meter_needed = int(action.meter_needed)
        action.proximity = int(action.proximity)
        action.start_counter_frame = int(action.start_counter_frame)

        return action

    def load_frame(self, frame_element):
        """Retrieve frame data from the specified frame XML
        element and return it as a Frame object.
        Return None instead if there is an error loading data.

        Keyword arguments:
            frame_element   The XML element containing frame data.
        """
        frame = Frame()

        frame.duration = frame_element.get('duration')
        frame.cancelable = frame_element.get('cancelable')
        frame.move_x = frame_element.get('move_x')
        frame.move_y = frame_element.get('move_y')
        frame.hurtboxes = self.load_all_hurtboxes(frame_element)
        frame.hitboxes = self.load_all_hitboxes(frame_element)
        frame.projectiles = self.load_all_projectiles(frame_element)

        if has_null_attributes(frame):
            return None

        frame.duration = int(frame.duration)
        frame.cancelable = int(frame.cancelable)
        frame.move_x = int(frame.move_x)
        frame.move_y = int(frame.move_y)

        return frame

    def load_collision_rect(self, box_element):
        """Load the x-offset, y-offset, width, and height of a
        collision box and return it as a PyGame Rect object.
        Return None instead if any of the attributes are missing from
        the element.

        Keyword arguments:
            box_element     The collision box XML element. This can be
                            a hurtbox or a hitbox.
        """
        x_offset = box_element.get('x_offset')
        y_offset = box_element.get('y_offset')
        width = box_element.get('width')
        height = box_element.get('height')

        # XML attributes are loaded as Strings, and Rect objects only accept
        # integer values for their dimensions.
        # However, the int() method for converting Strings to integers won't
        # work on None objects. The XML loader will return a None
        # object if one of the XML attributes isn't found, so in that case,
        # the function should be terminated immediately.
        if has_null_items_in_list([x_offset, y_offset, width, height]):
            return None

        collision_rect = Rect(int(x_offset), int(y_offset),
                              int(width), int(height))

        return collision_rect

    def load_hurtbox(self, hurtbox_element):
        """Retrieve hurtbox data from the specified hurtbox XML
        element and return it as a Hurtbox object.
        Return None instead if there is an error loading data.

        Keyword arguments:
            hurtbox_element   The XML element containing hurtbox data.
        """
        hurtbox = Hurtbox()

        hurtbox.rect = self.load_collision_rect(hurtbox_element)

        if has_null_attributes(hurtbox) == True:
            return None

        return hurtbox

    def load_hitbox(self, hitbox_element):
        """Retrieve hurtbox data from the specified hurtbox XML
        element and return it as a Hurtbox object.
        Return None instead if there is an error loading data.

        Keyword arguments:
            hurtbox_element   The XML element containing hurtbox data.
        """
        hitbox = Hitbox()

        hitbox.rect = self.load_collision_rect(hitbox_element)
        hitbox.damage = hitbox_element.get('damage')
        hitbox.hitstun = hitbox_element.get('hitstun')
        hitbox.blockstun = hitbox_element.get('blockstun')
        hitbox.knockback = hitbox_element.get('knockback')
        hitbox.dizzy_stun = hitbox_element.get('dizzy_stun')
        hitbox.effect = hitbox_element.get('effect')
        hitbox.can_block_high = hitbox_element.get('high_block')
        hitbox.can_block_low = hitbox_element.get('low_block')

        if has_null_attributes(hitbox) == True:
            return None

        hitbox.damage = int(hitbox.damage)
        hitbox.hitstun = int(hitbox.hitstun)
        hitbox.blockstun = int(hitbox.blockstun)
        hitbox.knockback = int(hitbox.knockback)
        hitbox.dizzy_stun = int(hitbox.dizzy_stun)
        hitbox.effect = int(hitbox.effect)
        hitbox.can_block_high = int(hitbox.can_block_high)
        hitbox.can_block_low = int(hitbox.can_block_low)

        return hitbox

    def load_projectile_data(self, projectile_element):
        """Retrieve projectile data from the specified hurtbox XML
        element and return it as a ProjectileData object.
        Return None instead if there is an error loading data.

        Keyword arguments:
            projectile_element  The XML element containing projectile
                                data.
        """
        projectile = ProjectileData()

        # Most of the data for the Projectile is kept in a separate XML file,
        # which is referenced in the 'filepath' attribute.
        projectile_doc_path = projectile_element.get('filepath')
        if is_valid_xml('characters/' + projectile_doc_path,
                        self.PROJECTILE_VERIFY_CODE,
                        'projectile') == False:
            return None
        projectile_doc = load_xml('characters/' + projectile_doc_path,
                                  'projectile')

        projectile.name = projectile_doc.get('name')
        projectile.spritesheet_path = projectile_doc.get('spritesheet')
        projectile.stamina = projectile_doc.get('stamina')
        projectile.first_loop_frame = projectile_doc.get('first_loop_frame')
        projectile.first_collision_frame = projectile_doc.get(
            'first_collision_frame')
        projectile.x_speed = projectile_element.get('x_speed')
        projectile.y_speed = projectile_element.get('y_speed')
        projectile.frames = self.load_all_frames(projectile_doc)
        # Remember that the PyGame Rect only accepts ints for parameters, so
        # these values will need to be assigned after the attribute check.
        x_offset = projectile_element.get('x_offset')
        y_offset = projectile_element.get('y_offset')
        width = projectile_doc.get('width')
        height = projectile_doc.get('height')

        if has_null_attributes(projectile):
            return None

        projectile.rect.x = int(x_offset)
        projectile.rect.y = int(y_offset)
        projectile.rect.width = int(width)
        projectile.rect.height = int(height)
        projectile.x_speed = int(projectile.x_speed)
        projectile.y_speed = int(projectile.y_speed)
        projectile.stamina = int(projectile.stamina)
        projectile.first_loop_frame = int(projectile.first_loop_frame)
        projectile.first_collision_frame = int(
            projectile.first_collision_frame)

        return projectile