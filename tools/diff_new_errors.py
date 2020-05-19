#!/usr/bin/env python

import xml.etree.ElementTree as ET
import sys

def show_help():
    print('Syntax:')
    print('  diff_new_errors.py <old_result.xml> <new_result.xml>')
    sys.exit(1)

if len(sys.argv) < 3:
    show_help()

OLD_RESULT_XML = sys.argv[1]
NEW_RESULT_XML = sys.argv[2]

old_tree = ET.parse(OLD_RESULT_XML)
new_tree = ET.parse(NEW_RESULT_XML)

class CppCheckError(object):
    def __init__(self, elem_error):
        self.id=elem_error.get("id")
        self.msg=elem_error.get("msg")
        self.elem_error=elem_error
        location = elem_error.find("location")
        self.file=location.get("file")
        self.line=location.get("line")
    
    def is_same(self, other):
        return self.id == other.id and self.msg == other.msg and self.file == other.file

def getkey(error):
    return (error.id, error.msg, error.line)

class ErrorsInFile(object):
    def __init__(self, file):
        self.errors = []
        self.file = file

    def diff_new(self, old_errors_in_file, new_errors):
        for error in self.errors:
            if not old_errors_in_file.have_error(error):
                new_errors.append(error)
    
    def have_error(self, other_error):
        for error in self.errors[:]:
            if error.is_same(other_error):
                self.errors.remove(error)
                return True
        
        return False
    
    def add_error(self, error):
        self.errors.append(error)
    
    def sort(self):
        self.errors[:] = sorted(self.errors, key=getkey)    
        

class ErrorsInResult(object):
    def __init__(self, tree):
        self.tree = tree
        self.errors_in_files = {} # key: file, value: ErrorsInFile

        elem_errors = tree.find("errors")
        for elem_error in elem_errors:
            error = CppCheckError(elem_error)
            self.add_error(error)
        
        for errors_in_file in self.errors_in_files.values():
            errors_in_file.sort()
    
    def add_error(self, error):
        errors_in_file = self.errors_in_files.get(error.file)
        if not errors_in_file:
            errors_in_file = ErrorsInFile(error.file)
            errors_in_file.add_error(error)
            self.errors_in_files[error.file] = errors_in_file
            return

        errors_in_file.add_error(error)

    def diff_new(self, old_errors_in_result):
        new_errors = []
        for errors_in_file in self.errors_in_files.values():
            old_errors_in_file = old_errors_in_result.find_file(errors_in_file.file)
            if old_errors_in_file:
                errors_in_file.diff_new(old_errors_in_file, new_errors)
            else:
                errors_in_file.diff_new(ErrorsInFile(""), new_errors)
        
        container = self.tree.find("errors")
        container.clear()

        for error in new_errors:
            container.append(error.elem_error)
        
        self.tree.write(NEW_RESULT_XML+".new_errors")

    def find_file(self, file):
        return self.errors_in_files.get(file)

old_errors_in_result = ErrorsInResult(old_tree)
new_errors_in_result = ErrorsInResult(new_tree)

new_errors_in_result.diff_new(old_errors_in_result)
