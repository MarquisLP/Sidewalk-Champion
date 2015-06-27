"""This module contains functions for loading Stage information from
external XML files into StageData objects that can be used by the game
engine.

Module Constants:
    STAGE_LIST_PATH (String): The relative file path to the text file
        containing the file paths of all included Stages.
    STAGE_SCHEMA_PATH: The file path to the XML Schema document that
        will be used to validate stage files.
    FILEPATH_PREFIX (String): The relative file path prefix for the
        directory containing all Stage files.
"""
import os
from lib.custom_data.xml_ops import load_xml_doc_as_object


STAGE_LIST_PATH = 'stages/stage_list.txt'
STAGE_SCHEMA_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                 'stage.xsd')
FILEPATH_PREFIX = 'stages/'


def load_stage(line_index):
    """Load a specific stage from the list specified in the Stage list
    text file.

    Args:
        line_index (int): The line index of the stage file's file
            path within the stage list text file.
            Note that like indexing in other parts of Python, this also
            starts at 0.

    Returns:
        The specified stage's data as a StageData object. If there was
        an error loading data, None is returned instead.
        None will also be returned if line_index exceeds the number of
        lines in the text file.
    """
    stage_paths = get_stage_paths()
    if line_index > len(stage_paths) - 1:
        return None

    stage_path = stage_paths[line_index]
    stage_data = load_xml_doc_as_object(stage_path, STAGE_SCHEMA_PATH)

    if stage_data is None:
        return None
    else:
        prepend_prefix_to_filepaths(stage_data)
        return stage_data


def get_stage_paths():
    """Return a list of all of the file paths to the XML files for
    battle Stages.
    """
    with open(STAGE_LIST_PATH) as f:
        stage_paths = [FILEPATH_PREFIX + line.rstrip('\n') for line in f]
        return stage_paths


def prepend_prefix_to_filepaths(stage_data):
    """Preprend FILEPATH_PREFIX to all file path attributes of a
    StageData object.

    Args:
        stage_data (StageData): A StageData instance.
    """
    stage_data.background.spritesheet_path = (FILEPATH_PREFIX +
        stage_data.background.spritesheet_path)
    stage_data.parallax.spritesheet_path = (FILEPATH_PREFIX +
        stage_data.parallax.spritesheet_path)
    for front_prop in stage_data.front_props:
        front_prop.spritesheet_path = (FILEPATH_PREFIX +
            front_prop.spritesheet_path)
    for back_prop in stage_data.back_props:
        back_prop.spritesheet_path = (FILEPATH_PREFIX +
            back_prop.spritesheet_path)
    if stage_data.music is not None:
        stage_data.music = FILEPATH_PREFIX + stage_data.music
