"""This module provides methods for loading XML files, as well checking
for potential errors that may result from reading XML data.
"""
from lxml import etree
from character_data import *


def load_xml_from_file(xml_path, schema_path):
    """Retrieve the entire contents of an XML document.

    Args:
        xml_path (String): The file path to a valid XML document.
        schema_path (String): The file path to an XML Schema that will be used
            to verify the XML document.

    Returns:
        The root XML element of the specified document.
        If the document was deemed invalid according to the specified XML
        Schema, None is returned instead.
    """
    parser = etree.XMLParser(remove_blank_text=True)
    xml_doc = etree.parse(xml_path, parser)
    schema_doc = etree.parse(schema_path, parser)
    schema = etree.XMLSchema(schema_doc)

    if schema.validate(xml_doc):
        return xml_doc.getroot()
    else:
        return None


def load_data_from_element(element):
    """Load all of an XML element's data into an object.

    Args:
        element (lxml.XML): An XML element.

    Returns:
        An instance of a class with the same name as element's tag, containing
        all of element's attributes, text, and child elements.
    """
    data_object = instantiate_from_string(element.tag)

    for attr_name, attr_value in object_attributes(data_object):
        if is_list_of_text_data(element, attr_name):
            loaded_data = load_xml_text_data(element, attr_name)
        elif type(attr_value) is dict:
            loaded_data = load_attribute_dict(element, attr_name)
        elif type(attr_value) is list:
            loaded_data = load_child_objects(element, attr_name)
        elif is_element_attribute(element, attr_name):
            loaded_data = load_element_attribute(element, attr_name)
        else:   # Optional attribute was omitted.
            loaded_data = attr_value

        setattr(data_object, attr_name, loaded_data)

    return data_object


def instantiate_from_string(class_name):
    """Return an instance of the specified class.

    Args:
        class_name (String): The name of a class included in this module's
            namespace. It will automatically be converted into CamelCase to
            match the class naming convention.
    """
    class_name = convert_underscore_to_camel_case(class_name)
    return globals()[class_name]()
