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
