"""This module provides methods for working with and performing various
operations on text files.
"""
def get_prefixed_lines_from_txt(txt_path, prefix=''):
    """Return a tuple containing all of the lines within a text file.
    Each line can be prefixed with a specific String.

    Args:
        txt_path (String): The file path to a text file containing one
            or more lines of text.
        prefix (String): Optional. A String segment that will be
            prepended to the start of each line.
    """
    with open(txt_path, 'U') as f:
        lines = [prefix + line.rstrip('\n') for line in f]
        return tuple(lines)


def num_of_lines_in_txt(txt_path):
    """Return the number of lines in a text file. None is returned if
    the file path is invalid.

    Args:
        txt_path (String): The file path to a text file.
    """
    try:
        return sum(1 for line in open(txt_path))
    except:
        return None
