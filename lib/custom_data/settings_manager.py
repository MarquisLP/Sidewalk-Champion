import os
import xml.etree.ElementTree as tree
from lib.custom_data.settings_data import SettingsData
from lib.custom_data.xml_ops import *

class SettingsManager(object):
    """Saves to and loads data from the settings file.
    
    Attributes:
        SETTINGS_VERIFY_CODE    The verification code for a correctly-
                                formatted Settings XML file.
        SETTINGS_PATH           Filepath for the settings file.
    """
    SETTINGS_VERIFY_CODE = '49uRJDj02skW'
    SETTINGS_PATH = 'settings.xml'

    # Load
    def load_settings(self):
        """Load all Settings data from the settings file and return it
        as a SettingsData object.
        """
        settings = SettingsData()

        # If the file is missing or corrupted, create a new one
        # and return the data from it instead.
        if is_valid_xml(self.SETTINGS_PATH,
                        self.SETTINGS_VERIFY_CODE,
                        'settings') == False:
            return self.create_new_file()

        settings_element = load_xml(self.SETTINGS_PATH, 'settings')
        settings.screen_scale = self.load_screen_scale(settings_element)
        settings.show_box_display = self.load_box_display(settings_element)

        player1_keys_element = settings_element.find('player1_keys')
        player2_keys_element = settings_element.find('player2_keys')
        self.load_key_bindings(settings.player1_keys, player1_keys_element)
        self.load_key_bindings(settings.player2_keys, player2_keys_element)

        # If any of the elements were missing, create a new file and
        # return its data instead.
        if has_null_attributes(settings) == True:
            return self.create_new_file()

        # All data from XML files are read as strings, even numbers and bools.
        # Only convert these values into their proper type after confirming
        # that they exist, through the attribute check above.
        settings.screen_scale = int(settings.screen_scale)
        settings.show_box_display = get_bool_string(settings.show_box_display)

        return settings

    def load_screen_scale(self, settings_element):
        """Load the screen magnification value from the specified
        settings XML element and return it as a String.

        Keyword arguments:
            settings_element    XML element containing settings data.
        """
        scale_element = settings_element.find('screen_scale')
        screen_scale = scale_element.text

        return screen_scale

    def load_box_display(self, settings_element):
        """Load the collision box display value from the specified
        settings XML element and return it as a String.

        Keyword arguments:
            settings_element    XML element containing settings data.
        """
        display_element = settings_element.find('show_box_display')
        show_box_display = display_element.text
        
        return show_box_display

    def load_key_bindings(self, key_dict, keys_element):
        """Load the key binding values from specified key list
        XML element and store them within the key binding Dictionary.
        Set the Dictionary equal to None if there is an error.

        Keyword arguments:
            key_dict        The key binding Dictionary that will store
                            the loaded data.
            keys_element    The XML element that contains a list of key
                            binding elements.
        """
        # Of course, if keys_element is None, which indicates a missing
        # element, an error should immediately be returned.
        if keys_element == None:
            key_dict = None
        else:
            for input_name in key_dict.keys():
                input_element = keys_element.find(input_name)

                # If find() returns None due to a missing element, the text
                # attribute can't be called.
                if input_element == None:
                    key_dict = None
                else:
                    key_dict[input_name] = input_element.text

    # Save
    def save_settings(self, settings_data):
        """Save all of the information within settings_data to the XML
        file specified by SETTINGS_PATH.

        Keyword arguments:
            settings_data       A SettingsData object that will have
                                its contents saved.
        """
        # To minimize the possibility of saving errors, the old file will be
        # deleted and replaced with an updated file.
        if os.path.isfile(self.SETTINGS_PATH):
            os.remove(self.SETTINGS_PATH)

        root_element = tree.Element('sidewalk_champion')
        settings_element = tree.SubElement(root_element, 'settings')

        self.save_screen_scale(settings_data, settings_element)
        self.save_box_display(settings_data, settings_element)
        self.save_key_bindings(settings_data.player1_keys, settings_element,
                               'player1_keys')
        self.save_key_bindings(settings_data.player2_keys, settings_element,
                               'player2_keys')

        verify_element = tree.SubElement(root_element, 'verification')
        verify_element.set('code', self.SETTINGS_VERIFY_CODE)

        new_xml = tree.ElementTree(root_element)
        new_xml.write(self.SETTINGS_PATH)

    def save_screen_scale(self, settings_data, parent_element):
        """Write the screen scale value to the file specified by
        CHARACTER_PATH.

        Keyword arguments:
            settings_data       The SettingsData object that contains
                                writeable data.
            parent_element      The parent XML element that will
                                contain the screen_scale element.
        """
        scale_element = tree.SubElement(parent_element, 'screen_scale')
        scale_element.text = str(settings_data.screen_scale)

    def save_box_display(self, settings_data, parent_element):
        """Write the show_box_display value to the file specified by
        CHARACTER_PATH.

        Keyword arguments:
            settings_data       The SettingsData object that contains
                                writeable data.
            parent_element      The parent XML element that will
                                contain the show_box_display element.
        """
        display_element = tree.SubElement(parent_element, 'show_box_display')
        display_element.text = str(settings_data.show_box_display)

    def save_key_bindings(self, keys_dict, parent_element, list_name):
        """Write the key bindings Dictionary to the file specified by
        CHARACTER_PATH.

        Keyword arguments:
            keys_dict           The Dictionary that contains data for
                                key bindings.
            parent_element      The parent XML element that will
                                contain the new element.
            list_name           The name of the XML element containing
                                the list of key bindings.
        """
        list_element = tree.SubElement(parent_element, list_name)

        for input_tag, key_binding in keys_dict.iteritems():
            new_binding = tree.SubElement(list_element, input_tag)
            new_binding.text = str(key_binding)

    # New File
    def create_new_file(self):
        """Create a new settings file with default values at the path
        specified by SETTINGS_PATH and return it. If the file already
        exists, it will be overwritten.
        """
        new_settings = SettingsData()

        self.set_default_bindings(new_settings.player1_keys, 1)
        self.set_default_bindings(new_settings.player2_keys, 2)

        self.save_settings(new_settings)

        return new_settings

    def set_default_bindings(self, key_dict, player):
        """Set the values in key_dict to the default key bindings
        for the player specified by player_num.

        Keyword arguments:
            key_dict        The Dictionary that will receive the
                            default bindings as values.
            player          Either 1 or 2, representing the player
                            whose key bindings key_dict belongs to.
                            This will alter the values as the players
                            should have different key bindings.
                            Note that if this value is not 1 or 2, it
                            will default to player 2's bindings.
        """
        if player == 1:
            key_dict['up'] = 'w'
            key_dict['back'] = 'a'
            key_dict['down'] = 's'
            key_dict['forward'] = 'd'
            key_dict['light_punch'] = 'r'
            key_dict['medium_punch'] = 't'
            key_dict['heavy_punch'] = 'y'
            key_dict['light_kick'] = 'f'
            key_dict['medium_kick'] = 'g'
            key_dict['heavy_kick'] = 'h'
            key_dict['start'] = 'left ctrl'
            key_dict['cancel'] = 'escape'
        else:
            key_dict['up'] = 'uo'
            key_dict['back'] = 'left'
            key_dict['down'] = 'down'
            key_dict['forward'] = 'right'
            key_dict['light_punch'] = '[7]'
            key_dict['medium_punch'] = '[8]'
            key_dict['heavy_punch'] = '[9]'
            key_dict['light_kick'] = '[4]'
            key_dict['medium_kick'] = '[5]'
            key_dict['heavy_kick'] = '[6]'
            key_dict['start'] = 'return'
            key_dict['cancel'] = 'backspace'