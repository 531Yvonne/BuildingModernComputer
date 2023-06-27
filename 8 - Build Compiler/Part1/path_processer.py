# Project 10: Compiler Part 1
#
# Yves Yang
#
# Path Class to process input path (a directory or a single .jack file)
import os


class Path:
    '''
    Attributes:
        path: a string for original user path input
        jack_files: a list storing paths for all .jack files


    Contain method to process input path (a directory or a single .jack file)
    '''

    def __init__(self, path):
        self.path = path
        self.filepaths = self.get_jack_files()

    def get_jack_files(self):
        '''
        Return a list of tuples storing (jack filename, jack filepath)
        When input path is a file, return the list directly;
        When the path is a folder (containg one or more .jack files), return
        the list for all valid .jack files in that folder.
        '''
        if os.path.isfile(self.path):
            # Input path is a .jack file, return the list with one path.
            return [self.path]
        else:
            # Input is a directory, store result for all jack files inside.
            # Here I refered to Python Documentation for os.scandir() usage.
            # Ref Link: https://docs.python.org/3/library/os.html#os.scandir
            filepaths = list(os.scandir(self.path))
            result = []
            for filepath in filepaths:
                if filepath.path[-5:] == ".jack":
                    # Is a .jack file
                    result.append((filepath.path))
            return result
