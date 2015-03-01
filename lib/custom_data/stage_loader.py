"""This module contains functions for loading Stage information from
external XML files into StageData objects that can be used by the game
engine.

Module Constants:
    STAGE_VERIFY_CODE (String): A string of characters that should be
        included within Stage files that are properly formatted.
    STAGE_LIST_PATH (String): The relative file path to the text file
        containing the file paths of all included Stages.
    FILEPATH_PREFIX (String): The relative file path prefix for the
        directory containing all Stage files.
"""
STAGE_VERIFY_CODE = 'sg9389hANa82'
STAGE_LIST_PATH = 'stages/stage_list.txt'
FILEPATH_PREFIX = 'stages/'
