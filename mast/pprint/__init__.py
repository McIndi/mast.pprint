import xml.etree.cElementTree as etree
import json


def pretty_print(elem, level=0):
    """
    pretty_print: I took this from several places on the internet
        If you know where this originated, please email me at
        ilovetux@ymail.com and I will provide proper credits
        OPEN SOURCE RULES!!
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


class Outputer(object):
    """
    Outputer

    An object which can take information and output it in various
    formats.
    """
    def __init__(self, data):
        self.data = data

    def __json__(self):
        if isinstance(self.data, dict) or isinstance(self.data, list):
            return json.dumps(self.data)
        elif isinstance(self.data, basestring):
            return json.dumps(json.loads(self.data))
        else:
            raise NotImplementedError(
                "Cannot convert {} to json".format(type(self.data)))

    def __xml__(self):
        if isinstance(self.data, basestring):
            tree = etree.fromstring(self.data)
            pretty_print(tree)
            return etree.tostring(tree)
        elif isinstance(self.data, list):
            xml = "<root>{}</root>".format(
                "".join(["<item>{}</item>".format(str(x)) for x in self.data]))
            tree = etree.fromstring(xml)
            pretty_print(tree)
            return etree.tostring(tree)
        elif isinstance(self.data, dict):
            xml = "<root>{}</root>".format(
                    "".join(["<{0}>{1}</{0}>".format(
                        str(k), str(v)) for k, v in self.data.items()]))
            tree = etree.fromstring(xml)
            pretty_print(tree)
            return etree.tostring(tree)
        elif isinstance(self.data, etree.Element) \
                or isinstance(self.data, etree.ElementTree):
            pretty_print(self.data)
            return self.data
        else:
            raise NotImplementedError(
                "Cannot convert {} to xml".format(type(self.data)))
