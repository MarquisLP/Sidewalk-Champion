"""This module provides methods for loading XML files, as well checking
for potential errors that may result from reading XML data.
"""
import os.path
import xml.etree.ElementTree as tree

def load_xml(filepath, element_name):
        """Parse an XML file, retrieve the specified element, and
        return it. Return None if the element could not be found.

        Keyword arguments:
            filepath        The filepath for the XMl file to parse. All
                            XML files should be kept in the characters
                            folder, so 'characters/' will be appended
                            to the beginning of the filepath when
                            parsing it.
            element_name    The name of the XML element to retrieve.
        """
        xml_tree = tree.parse(filepath)
        xml_root = xml_tree.getroot()
        xml_element = xml_root.find(element_name)

        return xml_element

def is_valid_xml(filepath, verification_string, base_element):
        """Return True if the specified XML file exists and has a
        proper formatting code.

        Keyword arguments:
        filepath                The filepath to the XML that will be
                                verified.
        verification_string     The XML file will be checked for a
                                'code' attribute within a
                                'verification' element that matches
                                this String.
        base_element            The base XML element that contains all
                                other data elements. If it is missing,
                                False is returned.
        """
        if filepath == None:
            return False

        if os.path.isfile(filepath) == False:
            return False
        try:
            xml_doc = tree.parse(filepath)
        except:
            return False

        xml_root = xml_doc.getroot()
        file_code = xml_root.find('verification').get('code')
        if file_code != verification_string:
            return False

        if xml_root.find(base_element) == None:
            return False

        return True

def has_null_attributes(obj):
        """Returns False if any of the attributes in the specified
        object are empty or set to None.

        This may happen when loading data from XML file, as None will
        be returned if a specific element or attribute isn't found.
        """
        # __dict__ is a Dictionary with all of the object's attribute names
        # and their corresponding values.
        attribute_list = obj.__dict__.values()
        for attribute in attribute_list:
            if attribute == None:
                return True

        return False

def has_null_items_in_list(list_to_check):
        """Return True if any of the items in the List are None.

        Keyword arguments:
            list_to_check   The list that will be verified.
        """
        for item in list_to_check:
            if item == None:
                return True

        return False

def get_bool_string(str):
    """Return True if str reads 'True'. This is useful for retrieving
    Boolean values from XML data.

    Keyword arguments:
        str     The String to evaluate.
    """
    if str == "True":
        return True
    else:
        return False