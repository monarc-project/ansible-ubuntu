#!/usr/bin/env python

import os
import sys
import fnmatch

def rename_deliveries(directory):
    """
    Rename files recursively.
    """
    for root, dirnames, filenames in os.walk(directory):
        for filename in fnmatch.filter(filenames, '*.docx'):
            file_path = os.path.join(root, filename)

            new_filename = filename.split('_')[-1]
            new_file_path = os.path.join(root, new_filename)

            try:
                os.rename(file_path, new_file_path)
            except:
                continue

if __name__ == '__main__':
    if len(sys.argv) > 1:
        DIRECTORY = sys.argv[1]
    else:
        DIRECTORY = './deliveries/'
    rename_deliveries(DIRECTORY)
