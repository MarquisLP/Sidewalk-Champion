"""This module loads character data from XML files and stores them in
CharacterData objects that can be read by the game engine.

Attributes:
    CHARACTER_LIST_PATH (String): The filepath for the text file which
        lists the paths to all of the characters' XML files.
        Each path is separated by a new-line.
    FILEPATH_PREFIX (String): The file path of the root directory where
        all character data files are kept.
"""
import os
from lib.custom_data.xml_ops import load_xml_doc_as_object


CHARACTER_LIST_PATH = 'characters/character_list.txt'
CHARACTER_SCHEMA_PATH = os.path.join(os.path.dirname(os.path.realpath(
                                                     __file__)),
                                     'character.xsd')
FILEPATH_PREFIX = 'characters/'


def load_character(line_index):
    """Load a specific character from the list specified in the
    character list text file.

    Args:
        line_index: An integer for the line index of the character file's
            file path within the character list text file.
            Note that like most indexing schemes, this starts at 0.

    Returns:
        The specified character's data as a CharacterData object. If
        there was an error loading data, None is returned instead.
        None will also be returned if line_index exceeds the number of
        lines in the text file.
    """
    xml_paths = get_character_paths()
    if line_index > len(xml_paths) - 1:
        return None

    character_path = xml_paths[line_index]
    char_data = load_xml_doc_as_object(character_path, CHARACTER_SCHEMA_PATH)
    prepend_prefix_to_filepaths(char_data)
    return char_data


def get_character_paths():
    """Return a list of all of the filepaths to the XML files for
    playable characters.
    """
    with open(CHARACTER_LIST_PATH) as f:
        character_path_list = [line.rstrip('\n') for line in f]
        return character_path_list


def prepend_prefix_to_filepaths(character):
    """Preprend FILEPATH_PREFIX to all file path attributes of a
    CharacterData object.

    Args:
        character (CharacterData): A CharacterData instance.
    """
    character.mugshot_path = prepend_prefix(character.mugshot_path)
    for action in character.actions:
        action.spritesheet_path = prepend_prefix(action.spritesheet_path)


def prepend_prefix(filepath):
    """Return the filepath string prepended with FILEPATH_PREFIX."""
    return FILEPATH_PREFIX + filepath
