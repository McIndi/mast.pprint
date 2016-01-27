"""
_module_: mast.pprint

This module contains a single function which accepts an
`xml.etree.ElementTree.Element` instance and inserts spaces
to indent the xml.
"""
import json
from cStringIO import StringIO
from term_utils import *
from pprint import pprint
import xml.etree.cElementTree as etree


def term_highlight(text):
    """
    _function_: `mast.pprint.term_highlight(text)`

    DESCRIPTION:

    Use ANSI escape sequences to syntax highlight text. Will handle most
    formats like XML, XSLT, Python, JSON etc. for a full list of supported
    languages see [this page](http://pygments.org/languages/).

    When run on Windows, `sys.stdout.write` is overriden with a function
    which filters ANSI Escape Sequences and substitutes Win32 API calls

    RETRUNS:

    `str`

    USAGE:

        :::python
        >>> xml = '<root><child key="value">text</child></root>'
        >>> print(term_highlight(xml))

    PARAMETERS:

    * `text`: The text to syntax highlight, should be a `str`

    NOTE:

    This function can have strange side effects when run in IPython
    interactive mode.
    """
    from pygments.util import ClassNotFound
    from pygments import highlight
    from pygments.lexers import guess_lexer, JsonLexer
    from pygments.formatters import TerminalFormatter
    try:
        json.loads(text)
        ret = highlight(text,
                        JsonLexer(),
                        TerminalFormatter())
        import colorama; colorama.init()
        return ret
    except ValueError:
        pass
    try:
        ret = highlight(text,
                        guess_lexer(text),
                        TerminalFormatter())
        print guess_lexer(text)
    except ClassNotFound:
        return text
    # Don't want to init if we couldn't guess the language
    import colorama; colorama.init()
    return ret


def print_table(seq, clear_screen=False):
    """
    _function_: `mast.pprint.print_table(seq)`

    DESCRIPTION:

    Send a formatted table to stdout. seq should be a sequence
    of sequences with the first sequence being the header.

    RETURNS:

    `None`

    USAGE:

        :::python
        >>> seq = [["this", "that", "the other"], [1,2,3], [4,5,6]]
        >>> print_table(seq)

    PARAMETERS:

    * `seq`: `seq` should be a sequence of sequences (ie. a list of lists
    or tuple of tuples)
    """
    from time import time, ctime
    from functools import partial
    import os
    clear = partial(os.system, 'cls' if os.name == 'nt' else 'clear')

    # Make a copy of the list so we don't modify the original
    _table = list(seq)
    _header_row = _table.pop(0)
    _template = ""
    for index, field in enumerate(_header_row):
        column = [field] + [str(x[index]) for x in _table]
        column_width = len(max(column, key=len))
        _template += " {%s: <%s} " % (index, column_width)
    if clear_screen:
        clear()
    print(ctime(time()) + "\n")
    header_row = _template.format(*_header_row)
    print header_row
    print("-" * len(header_row))
    for row in _table:
        print(_template.format(*row))


def pprint_plus(obj, color=True, page_output=False):
    """
    _function_: `mast.pprint.pprint_plus(text)`

    DESCRIPTION:

    Attempt to pretty-print obj and send to `stdout`. If `color` is
    True (the default) attempt to syntax-highlight the output. If
    `page_output` is set to True, the output will be paged.

    RETRUNS:

    `None`

    USAGE:

        :::python
        >>> obj = ["this", "that", "the other"]
        >>> pprint_plus(obj)

    PARAMETERS:

    * `obj`: Arbitrary Python object to attempt to serialize and pretty-print
    * `color`: Attempt syntax highlighing on the output
    * `page_output`: If True, page the output to `stdout`

    NOTE:

    This function can have strange side effects when run in IPython
    interactive mode.
    """
    try:
        text = json.dumps(text, indent=4)
    except ValueError:
        f = StringIO()
        pprint(text, stream=f)
        f.seek(0)
        text = f.read()
    if color:
        text = term_highlight(text)
    if page_output:
        page(text)
    else:
        print text

def pprint_xml(elem, color=True, page_output=False):
    """
    _function_: `mast.pprint.pprint_xml`

    DESCRIPTION:

    Send a pretty-printed version of elem to `stdout`.

    RETURNS:

    `None`

    USAGE:

        :::python
        >>> elem = etree.fromstring(xml)
        >>> pprint_xml(elem, color=False, page=True)

    PARAMETERS:

    * `elem`: An `xml.etree.Element` or `xml.etree.ElementTree` instance to
    send to stdout
    * `color`: If True the XML will be syntax highlighted
    * `page`: If True, the output will be paged
    """
    pretty_print(elem)
    text = etree.tostring(elem)
    if color:
        text = term_highlight(text)
    if page_output:
        page(text)
    else:
        print text


def pprint_xml_str(text, color=True, page_output=False):
    """
    _function_: `mast.pprint.pprint_xml_str`

    DESCRIPTION:

    Send a pretty-printed version of XML string to `stdout`.

    RETURNS:

    `None`

    USAGE:

        :::python
        >>> pprint_xml(xml, color=False, page=True)

    PARAMETERS:

    * `text`: A Python `str` containing XML
    * `color`: If True the XML will be syntax highlighted
    * `page`: If True, the output will be paged
    """
    elem = etree.fromstring(text)
    pretty_print(elem)
    text = etree.tostring(elem)
    if color:
        text = term_highlight(text)
    if page_output:
        page(text)
    else:
        print text


def pretty_print(elem, level=0):
    """
    _function_: `mast.pprint.pretty_print(elem, level=0)`

    Insert spaces into an `xml.etree.ElementTree.Element` instance
    in order to "pretty print" it.

    Returns:

    `None`

    USAGE:

        :::python
        >>> elem = etree.fromstring(xml)
        >>> print pretty_print(elem)

    Parameters:

    * `elem`: The element to pretty-print
    * `level`: FOR INTERNAL RECURSIVE USE. Do not set yourself. Controls
    current indentation level.
    """
    i = "\n" + "  " * level
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            pretty_print(elem, level + 1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i


# Work in progress (Leave commented out for production until ready)
#
#class Outputer(object):
#    """
#    Outputer
#
#    An object which can take information and output it in various
#    formats.
#    """
#    def __init__(self, data):
#        self.data = data
#
#    def __json__(self):
#        if isinstance(self.data, dict) or isinstance(self.data, list):
#            return json.dumps(self.data)
#        elif isinstance(self.data, basestring):
#            return json.dumps(json.loads(self.data))
#        else:
#            raise NotImplementedError(
#                "Cannot convert {} to json".format(type(self.data)))
#
#    def __xml__(self):
#        if isinstance(self.data, basestring):
#            tree = etree.fromstring(self.data)
#            pretty_print(tree)
#            return etree.tostring(tree)
#        elif isinstance(self.data, list):
#            xml = "<root>{}</root>".format(
#                "".join(["<item>{}</item>".format(str(x)) for x in self.data]))
#            tree = etree.fromstring(xml)
#            pretty_print(tree)
#            return etree.tostring(tree)
#        elif isinstance(self.data, dict):
#            xml = "<root>{}</root>".format(
#                    "".join(["<{0}>{1}</{0}>".format(
#                        str(k), str(v)) for k, v in self.data.items()]))
#            tree = etree.fromstring(xml)
#            pretty_print(tree)
#            return etree.tostring(tree)
#        elif isinstance(self.data, etree.Element) \
#                or isinstance(self.data, etree.ElementTree):
#            pretty_print(self.data)
#            return self.data
#        else:
#            raise NotImplementedError(
#                "Cannot convert {} to xml".format(type(self.data)))
