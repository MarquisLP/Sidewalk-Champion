"""This module provides functions for saving to and loading data from
the settings XML file.

Attributes:
    SETTINGS_PATH (String): The file path for the settings file.
    SETTINGS_SCHEMA_PATH (String): The file path for the settings'
        XML Schema.
"""
from lib.custom_data.settings_data import SettingsData
from lib.custom_data.xml_ops import (load_xml_doc_as_object,
    save_object_as_xml_doc)


SETTINGS_PATH = 'settings.xml'
SETTINGS_SCHEMA_PATH = 'settings.xsd'


def load_settings():
    """Load all Settings data from the settings file and return it as a
    SettingsData object.

    If errors were encountered while reading the settings file, a
    SettingsData object with default values is returned instead.
    """
    settings = load_xml_doc_as_object(SETTINGS_PATH, SETTINGS_SCHEMA_PATH)
    if settings is None:
        return SettingsData()
    else:
        return settings


def save_settings(save_data):
    """Save all of the information within settings_data to the XML file
    specified by SETTINGS_PATH.

    Args:
        save_data (SettingsData): Contains the data that will be saved.
    """
    save_object_as_xml_doc(save_data, SETTINGS_PATH)
