"""This module provides functions for saving to and loading data from
the settings XML file.

Attributes:
    SETTINGS_PATH (String): The file path for the settings file.
    SETTINGS_SCHEMA_PATH (String): The file path for the settings'
        XML Schema.
"""
from lib.custom_data.xml_ops import load_xml_doc_as_object


SETTINGS_PATH = 'settings.xml'
SETTINGS_SCHEMA_PATH = 'settings.xsd'


def load_settings():
    """Load all Settings data from the settings file and return it as a
    SettingsData object.

    Returns:
        A SettingsData object, or None if errors were encountered while
        reading the settings file.
    """
    return load_xml_doc_as_object(SETTINGS_PATH, SETTINGS_SCHEMA_PATH)
