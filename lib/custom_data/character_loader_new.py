"""This module loads character data from XML files and stores them in
CharacterData objects that can be read by the game engine.

Attributes:
    CHARACTER_LIST_PATH (String): The filepath for the text file which
        lists the paths to all of the characters' XML files.
        Each path is separated by a new-line.
    FILEPATH_PREFIX (String): The file path of the root directory where
        all character data files are kept.
"""
CHARACTER_LIST_PATH = 'characters/character_list.txt'
FILEPATH_PREFIX = 'characters/'


def get_character_paths():
    """Return a list of all of the filepaths to the XML files for
    playable characters.
    """
    with open(CHARACTER_LIST_PATH) as f:
        character_path_list = [line.rstrip('\n') for line in f]
        return character_path_list
