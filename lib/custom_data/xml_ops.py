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
