#!/usr/bin/python3

"""
@author: Eduardo Romero
"""

import zipfile
import sys
import psutil


def check_process_done(pid):
    try:
        process = psutil.Process(pid)
        return process.is_running()
    except:
        return False


if __name__ == "__main__":
    pid = int(sys.argv[1])
    filename = sys.argv[2]
    unzipDirectory = sys.argv[3]
    while check_process_done(pid):
        pass

    if zipfile.is_zipfile(filename):
        with zipfile.ZipFile(filename, 'r') as zip_ref:
            zip_ref.extractall(unzipDirectory)
