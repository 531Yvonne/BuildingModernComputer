# Project 8: VM Translator Part 2
#
# Yves Yang
#
# Path Class to process input path (a directory or a single .vm file)
import os


class Path:
    '''
    Attributes:
        path: a string for original user path input
        vm_files: a list storing (.vm filename, path) for all .vm files
        output_path: a string for .asm output path
        folder_name: name of the folder when input is a directory

    Contain method to process input path (a directory or a single .vm file)
    '''

    def __init__(self, path):
        self.path = path
        self.vm_files = self.get_vm_files()
        self.output_path = self.get_output_path()

    def get_vm_files(self):
        '''
        Return a list of tuples storing (.vm filename, .vm filepath)
        When input path is a file, return the list directly;
        When the path is a folder (containg one or more .vm files), return
        the list for all valid .vm files in that folder.
        '''
        if os.path.isfile(self.path):
            # Input path is a .vm file, return the list with one original path.
            return [(os.path.basename(self.path), self.path)]
        else:
            # Input path is a directory, store result for all .vm files inside.
            # Here I refered to Python Documentation for os.scandir() usage.
            # Ref Link: https://docs.python.org/3/library/os.html#os.scandir
            filepaths = list(os.scandir(self.path))
            result = []
            for filepath in filepaths:
                if filepath.path[-3:] == ".vm":
                    # Is a .vm file
                    filename = os.path.basename(filepath.path)
                    result.append((filename, filepath.path))
            return result

    def get_output_path(self):
        '''Return the final .asm file path.'''
        if os.path.isfile(self.path):
            # Input path is Xxx.vm file, output file should be Xxx.asm and
            # should be saved in the same directory
            return self.path[:-2] + "asm"
        else:
            self.folder_name = os.path.basename(self.path)
            # Input path is a directory Xxx, output file should be Xxx.asm
            # and be saved under this directory
            # Use path for any sample.vm and replace sample.vm with Xxx.asm
            filename, path = self.vm_files[0]
            i = len(filename)
            return path[:-i] + self.folder_name + ".asm"
