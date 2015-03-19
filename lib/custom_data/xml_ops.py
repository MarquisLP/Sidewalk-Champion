"""This module provides methods for loading XML files, as well checking
for potential errors that may result from reading XML data.
"""
from lxml import etree
from character_data import *


def load_xml_doc_as_object(xml_path, schema_path):
    """Return an object containing the contents of an XML document as
    attributes.

    Args:
        xml_path (String): The file path to a valid XML document.
        schema_path (String): The file path to an XML Schema that will be used
            to verify the XML document.

    Returns:
        An instance of a class with the same name as the XML document's
        root element.
        None is returned instead if there were any errors reading the
        specified files.
    """
    root_element = load_xml_from_file(xml_path, schema_path)
    if root_element is None:
        return None
    else:
        return convert_element_to_object(root_element)


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
        None is also returned if either of the file paths are faulty, or
        if either file had trouble being parsed.
    """
    parser = etree.XMLParser(remove_blank_text=True)

    try:
        xml_doc = etree.parse(xml_path, parser)
        schema_doc = etree.parse(schema_path, parser)
    except:
        return None

    schema = etree.XMLSchema(schema_doc)

    if schema.validate(xml_doc):
        return xml_doc.getroot()
    else:
        return None


def convert_element_to_object(element):
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


def convert_underscore_to_camel_case(text):
    """Return text converted into CamelCase.

    Args:
        text (String): A string with words separated by underscores.
    """
    words = text.split('_')
    words = [word.capitalize() for word in words]
    return ''.join(words)


def object_attributes(obj):
    """Return a dictionary containing the names and values of all attributes
    within an object.

    Args:
        obj (Object): An instance of some class.
    """
    return obj.__dict__.items()


def is_list_of_text_data(parent_element, list_name):
    """Return a Boolean indicating whether the specified XML element contains
    one or more child elements of the same tag and containing text data.

    Args:
        parent_element (Element): An XML element containing all of the child
            text elements.
        list_name (String): An appropriate list name for the child elements.
            For example, if the child elements have the tag 'box', then
            'boxes' should be passed for this parameter.
    """
    list_item_name = get_singular_from_plural(list_name)

    if parent_element.find(list_item_name) is None:
        return False

    return parent_element.find(list_item_name).text is not None


def load_xml_text_data(parent_element, text_list_name):
    """Load child elements containing text from a parent XML element.

    Args:
        list_name (String): An appropriate list name for the child elements.
            For example, if the child elements have the tag 'box', then
            'boxes' should be passed for this parameter.
        parent_element (Element): An XML element containing all of the child
            text elements.
    """
    data_from_text = []
    list_item_name = get_singular_from_plural(text_list_name)

    for text_element in parent_element.findall(list_item_name):
        new_data = convert_to_int_if_numeric(text_element.text)
        data_from_text.append(new_data)

    return data_from_text


def convert_to_int_if_numeric(original_string):
    """Cast a numeric string into an integer.

    Args:
        original_string (String): A text string.

    Returns:
        An integer containing the contents of original_string.
        If original_string is not numeric, original_string is returned
        unmodified as a String.
    """
    if original_string.isdigit():
        return int(original_string)
    else:
        return original_string


def load_attribute_dict(parent_element, tag_name):
    """Load all of the attribute names and values within an XML element into a
    dict.

    Args:
        parent_element (Element): The parent XML Element containing the desired
            Element as a child node.
        tag_name (String): The tag name of the desired XML element.
    """
    loaded_element = parent_element.find(tag_name)
    attribute_dict = {attr[0] : convert_to_int_if_numeric(attr[1])
                      for attr in loaded_element.items()}
    return attribute_dict


def load_child_objects(parent_element, child_list_name):
    """Load child elements of the same tag name from a parent XML element.

    Args:
        parent_element (Element): The XML element containing all of the child
            elements.
        child_list_name (String): An appropriate name for a list containing
            the child elements. For example, if the child elements' tag is
            'box', 'boxes' should be passed for this parameter.
    """
    children = []
    child_name = get_singular_from_plural(child_list_name)

    for child_element in parent_element.findall(child_name):
        child_object = convert_element_to_object(child_element)
        children.append(child_object)

    return children


def get_singular_from_plural(plural):
    """Convert a plural word into its singular form.

    Args:
        plural (String): A plural. For example, 'cats', 'potatoes', 'knives'.
    """
    if plural[-3:] in ['oes', 'xes']:
        return plural[:-2]
    elif plural[-3:] == 'ves':
        return plural[:-3] + 'fe'
    elif plural[-3:] == 'ies':
        return plural[:-3] + 'y'
    else:
        return plural[:-1]


def is_element_attribute(element, attribute_name):
    """Return a Boolean indicating whether the specified element has an
    attribute of the specified name.

    Args:
        element (Element): An XML element that will be searched.
        attribute_name (String): The name of the attribute to find.
    """
    return element.get(attribute_name) is not None


def load_element_attribute(element, attribute_name):
    """Return an attribute from an XML element.

    Args:
        element (Element): An XML element containing the desired attribute.
        attribute_name (String): The name of the attribute to load.
    """
    attribute_value = element.get(attribute_name)
    return convert_to_int_if_numeric(attribute_value)


def save_object_as_xml_doc(data_object, doc_filepath):
    """Save the attributes of an object to an XML document.

    Args:
        data_object (Object): An instance of some class.
        doc_filepath (String): The file path to an XML document. If the file
            doesn't exist, it will be created.
    """
    root = convert_object_to_element(data_object)
    xml_tree = etree.ElementTree(root)
    xml_tree.write(doc_filepath, pretty_print=True)


def convert_object_to_element(data_object):
    """Convert an object into an XML Element.

    Args:
        data_object (object): An instance of some class.

    Returns:
        An XML Element whose tag name is the same as data_object's class name,
        but in underscore_case. Its attributes and child Elements will contain
        data from all of data_object's attributes.
    """
    class_name = type(data_object).__name__
    element_name = convert_camel_case_to_underscore(class_name)
    new_element = etree.Element(element_name)

    for attribute_name, attribute_value in object_attributes(data_object):
        if type(attribute_value) is dict:
            dict_element = convert_dict_to_element(attribute_value,
                                                   attribute_name)
            new_element.append(dict_element)
        else:
            new_element.set(attribute_name, str(attribute_value))

    return new_element


def convert_camel_case_to_underscore(text):
    """Return text written in CamelCase converted to underscore_case.

    Args:
        text (String): A text string written in CamelCase.
    """
    words = []
    last_capital_index = 0

    for current_letter_index in xrange(1, len(text)):
        if text[current_letter_index].isupper():
            words.append(text[last_capital_index:current_letter_index])
            last_capital_index = current_letter_index
        elif current_letter_index == len(text) - 1:
            words.append(text[last_capital_index:])

    return '_'.join(words).lower()


def convert_dict_to_element(dictionary, element_name):
    """Convert a dict into an XML element.

    Args:
        dictionary (dict): A dict with one or more key-value pairs.
        element_name (String): The name given to the XML Element's tag.

    Returns:
        An Element with element_name as its tag and the key-value pairs in
        dictionary as its attributes.
    """
    new_element = etree.Element(element_name)

    for key, value in dictionary.items():
        new_element.set(key, str(value))

    return new_element
