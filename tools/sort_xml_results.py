#!/usr/bin/env python

import xml.etree.ElementTree as ET
import sys

def show_help():
    print('Syntax:')
    print('  sort_xml_results.py <result.xml>')
    sys.exit(1)

if len(sys.argv) == 1:
    show_help()

RESULT_XML = sys.argv[1]

tree = ET.parse(RESULT_XML)

def getkey(elem):
    location = elem.find("location")
    return (location.get("file"), location.get("line"), location.get("column"), elem.get("id"), elem.get("msg"))

container = tree.find("errors")

container[:] = sorted(container, key=getkey)

tree.write(RESULT_XML+".sorted")
