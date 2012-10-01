# -*- coding: utf-8 -*-

import os
import re


# Each textual line (and, sadly, some non-textual lines) begins with a
# string representing the details of the text and the
# line. Unfortunately the format of this line varies in the crucial
# ending character(s). In 2682, at least, || is used; this is not
# handled in the regular expression below.
line_prefix_re = re.compile(ur'^T[^║:∥]*[║:∥](.*)$')
# I do not understand what these are, but the spec called for them not
# to be used in the n-grams, and it is easier to remove them here than
# discard them in the tokenisation process, though presumably they are
# part of the text.
raw_code_removal_re = re.compile(r'&[^;]*;')


class Stripper (object):

    """Class used for preprocessing a corpus of texts by stripping out
    all material that is not the textual material proper.

    The intention is to keep the stripped text as close in formatting
    to the original as possible, including whitespace."""

    def __init__ (self, input_dir, output_dir):
        self._input_dir = os.path.abspath(input_dir)
        self._output_dir = os.path.abspath(output_dir)

    def strip_files (self):
        for filename in os.listdir(self._input_dir):
            self.strip_file(filename)

    def strip_file (self, filename):
        file_path = os.path.join(self._input_dir, filename)
        stripped_file_path = os.path.join(self._output_dir, filename)
        with open(file_path, 'rU') as input_file:
            with open(stripped_file_path, 'w') as output_file:
                for line in input_file:
                    stripped_line = self.strip_line(line.decode('utf-8'))
                    if stripped_line:
                        output_file.write(stripped_line.encode('utf-8') + '\n')

    def strip_line (self, line):
        new_line = ''
        match = line_prefix_re.search(line)
        if match:
            new_line = match.group(1)
            new_line = raw_code_removal_re.subn('', new_line)[0]
        return new_line