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
import xml.etree.ElementTree as tree
from lib.custom_data.xml_ops import *
from lib.custom_data.stage_data import StageData


STAGE_VERIFY_CODE = 'sg9389hANa82'
STAGE_LIST_PATH = 'stages/stage_list.txt'
FILEPATH_PREFIX = 'stages/'


def get_stage_paths():
    """Return a list of all of the file paths to the XML files for
    battle Stages.
    """
    with open(STAGE_LIST_PATH) as f:
        stage_paths = [line.rstrip('\n') for line in f]
        return stage_paths

def load_stage_data(stage_element):
    """Retrieve Stage data from an XML element and return it as a
    StageData object.

    Args:
        stage_element (Element): An XML element with sub-elements that
            specify Stage data.

    Returns:
        A StageData object containing the loaded information.
        None will be returned if at least one of the Stage parameters
        couldn't be loaded.
    """
    new_stage = StageData()

    new_stage.name = stage_element.find('name').text
    new_stage.subtitle = stage_element.find('subtitle').text
    new_stage.background = stage_element.find('background').text
    new_stage.parallax = stage_element.find('parallax').text
    new_stage.x_offset = stage_element.find('x_offset').text
    new_stage.ground_level = stage_element.find('ground_level').text
    new_stage.music = stage_element.find('music').text

    if has_null_attributes(new_stage):
        return None
    else:
        # These attributes can only be converted from String to int
        # after verifying that they were loaded. Otherwise, an error will
        # occur when trying to convert a None object.
        new_stage.x_offset = int(new_stage.x_offset)
        new_stage.ground_level = int(new_stage.ground_level)
        return new_stage
