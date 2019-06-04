import time
import shutil
import os 
import pickle
import pathlib

import errors

#TODO: Tests

"""
The following are user settings.

Dirname should be equal to r'your_path'

percent_full_delete_threshold is a float value between 0 and 1 to be used
as a percentage threshold until we allow files to be less old before deleting.

delete_older_than is the list responsible for deciding how old a file has to be before being deleted.
The first value applies always and the second value is applied for when the disk is more than x% full
as set in percent_full_delete_threshold

incl_folders and incl_files are for setting whether script will delete folders,
files or both
"""
dirname = r'c:\Users\warren\Downloads\temp'
directory_storage = r'c:\Users\warren\Downloads\settings.pkl'

# If disk passes this threshold use second value for delete_older_than.
percent_full_delete_threshold = 0.95 

delete_older_than = 1  # Time, in seconds, before a file is deleted.
incl_folders = False  # Should this delete folders
incl_files = True  # Should this delete files 

# Should probably only choose one of the following options, not both
extensions = ['.txt']  # File extensions to use in blacklist OR whitelist
blocklist = None  # True = whitelist. False = Blacklist. None = no blocklist.


class DirectoryManager():
    def __init__(self, path):
        """
        A class to manage the user settings, namely multiple directories.

        Arguments:
            path {pathlib path object} -- The path to the .pkl file where user settings are serialized.
        """
        self.path = pathlib.Path(path)

    def save_directory(self, directory_obj):
        """
        A function to save a Directory object to the user settings file.

        Arguments:
            directory_obj {Directory} -- A directory object to be serialized.
        """
        with self.path.open(mode='ba') as output:
            pickle.dump(directory_obj, output, pickle.HIGHEST_PROTOCOL)

    def load_directories(self):
        """
        A function to return a list of Directory objects saved to the user settings file.
        """
        with self.path.open(mode='rb') as input:
            objs = []
            while True:
                try:
                    # We could also run the Directory deletion_process() at this point.
                    # However, then when using remove_directory() it will clean the directory before removing it
                    # from being tracked - presumably the user does not want to clean that directory anymore!
                    objs.append(pickle.load(input)) 
                except EOFError:
                    break
        return objs

    def clean_directories(self):
        """
        A method to clean all directories of unwanted files/folders. 
        """
        for obj in self.load_directories():
            obj.deletion_process()

    def remove_directory(self, directory_path):
        """
        Function to unpickle and then repickle all but the desired object.

        Arguments:
            directory_obj {Directory} -- An instance of the Directory object.

        Errors:
            FileNotFoundError -- When the pickle file used to save directories
            is not present at the path then this error is thrown.
        """
        obj_to_save = []
        for obj in self.load_directories():
            if obj.path.lower() == directory_path.lower():
                continue
            else:
                obj_to_save.append(obj)

        os.remove(str(self.path))
        for obj in obj_to_save:
            self.save_directory(obj)


class Directory():
    def __init__(self, path, incl_files, incl_folders, delete_older_than,
                 extensions=None, blocklist=None, recursive=None, **kwargs):
        """
        A directory class is created so that class instances can be created
        to track user preferences of multiple directories.

        Arguments:
            path {str} -- The directory path.
            incl_files {bool} -- Whether or not to include files in the deletion process.
            incl_folders {bool} -- Whether or not to include folders in the deletion process.
            delete_older_than {int} -- The file age required for a file to be deleted.
            extensions {list} -- A list of strings which are file extensions to not delete. 
            The extensions must start with a period. 

        Keyword Arguments:
            blocklist {bool} -- Setting whether to use a whitelist (True)
            or a blacklist (False) for file extensions. (default: {None})

            recursive {bool} -- Whether or not to recursively apply
            the same deletion process to sub-directories. (default: {None})
        """

        self.path = pathlib.Path(path)
        if not self.path.is_dir():
            raise errors.NotADirectoryError

        self.incl_files = incl_files
        self.incl_folders = incl_folders

        # A whitelist takes priority over a blacklist
        self.extensions = extensions
        self.blocklist = blocklist

        disk_info = shutil.disk_usage(str(self.path))  # Named tuple = usage(total, used, free)
        self.percent_full = disk_info[2]/disk_info[0]

        self.delete_older_than = delete_older_than

        st = self.path.stat()  # Creates a temporary named tuple

        # We run the age on __init__ because we will not save the file objects,
        # rather they will be initiated each time the script is run. 
        self.age = time.mktime(time.gmtime())-st.st_mtime

        for key, value in kwargs.items():
            setattr(self, key, value)

    def deletion_process(self):
        """
        The main functions that starts the process of deleting all files, directories and subdirectories as specified by the user.

        Initially it sets the folder attribute by calling the get_folders() function. 
        If the user specified to recursively search directories it calls itself on those directories upto a depth of 5. 
        Subsequently all files are deleted in the directory, and the directory itself is deleted if specified, as long as it's not the base directory. 
        """
        self.get_folders()
        for folder in self.folders:
            try:
                if folder.recursive and folder.depth < 5: 
                    folder.deletion_process()
                elif not folder.recursive: 
                    return
            except AttributeError:
                pass

        if self.incl_files: 
            self.delete_files()

        try:
            self.depth
            if self.incl_folders: 	
                self.delete()
        except AttributeError: 
            # If we get an attribute error we know that this is the base directory,
            # since the depth is not set yet - we don't want to delete it! 
            pass

    def get_folders(self):
        """
        Method to append all the Directory objects of the folders in the base directory to a class attribute.

        For each folder in the directory a Directory class instance is created and then appended to the folders class attribute of the Directory instance. 
        By default the Directory instances inherit the same directory specifications as defined in __init__. 
        This method is only called directly before doing anything with the folder because it initiates a class instance and therefore determines the Directory instance age.  
        """
        #TODO: make it possible for the subDirectory class instances to not neccesarily take the same arguments as the base instance
        self.folders = [] 
        for f in self.path.list_dir():
            if f.is_dir():
                try:
                    self.depth
                    self.folders.append(Directory(f, self.incl_files,
                                                  self.incl_folders, self.delete_older_than,
                                                  self.extensions, depth=self.depth+1,
                                                  recursive=True, blocklist=self.blocklist))
                # We get this error if there is no self.depth attribute (e.g it is the base directory and we haven't set its depth yet)
                except AttributeError: 
                    self.folders.append(Directory(f, self.incl_files,
                                                  self.incl_folders, self.delete_older_than,
                                                  self.extensions, depth = 1, recursive=True,
                                                  blocklist=self.blocklist))

    def delete_files(self):
        """
        Method to delete files if they meet the criteria defined in the Directory instance.

        Calls get_files() so that the files class attribute is populated with File instances. 
        For each File instance it checks that it meets the file age and blacklist/
        whitelist criteria for file extension, as defined in the Directory instance, and then deletes the file.
        """
        self.get_files()

        for f in self.files:
            delete = False

            if f.age >= self.delete_older_than:
                delete = True

            if self.blocklist:  # If true it is a whitelist
                if f.extension not in self.extensions:
                        delete = False

            elif self.blocklist:  # If false it is a blacklist
                if f.extension in self.extensions:
                    delete = False

            if delete:
                try:
                    f.delete()
                except errors.NotAFileError:
                    pass

    def get_files(self):
        """
        Method to append all the File objects of the files in the base directory to a class attribute. 

        For each file in the directory a File class instance is created and then appended to the files class attribute of the Directory instance.
        This is only called directly before deleting files because when creating the class instance for each file the File age is set. 
        """
        self.files = []
        for f in self.path.iterdir(): 
            if f.is_file(): 
                self.files.append(File(f))

    def delete(self):
        """Method to delete the directory."""
        try:
            shutil.rmtree(str(self.path))
        except OSError as e:  # If the folder does not exist we will get this error. 
            print("No folder error: {} - {}".format(e.filename, e.strerror))

    def __eq__(self, other):
        """
        Function to compare the class attributes between two Directory instances.

        Arguments:
            other {Directory} -- A Directory class instance.

        Returns:
            Bool -- Returns True or False dependant on if the class instances have the same attributes.
        """
        return self.__dict__ == other.__dict__

    def __str__(self):
        """
        String method to provide the command line utility to display to the user.
        """
        return str(self.path)


class File():
    def __init__(self, path):
        """
        A file class to store attributes such as age, path, and extension type. 

        For finding the extension of a file if it starts with a leading period, e.g: '.gitignore', 
        the period is ignored since it's not a file extension. 

        Arguments:
            path {string or pathlib object} -- The file path.
        """

        self.path = pathlib.Path(path)
        if not self.path.is_file():
            raise errors.NotAFileError

        _, self.extension = os.path.splitext(str(self.path)) # The root of the file is not important

        st = self.path.stat()  # Creates a temporary named tuple

        # We run the age on __init__ because we will not save the file objects,
        # rather they will be initiated each time the script is run. 
        self.age = time.mktime(time.localtime())-st.st_mtime # Must use local time since st_mtime is in local time

    def delete(self):
        """
        Method to delete the file.
        """
        os.remove(str(self.path)) 


if __name__ == '__main__':
    dir = Directory(dirname, incl_files, incl_folders, delete_older_than, 
                    extensions=extensions, blocklist=blocklist, recursive=True)
    dm = DirectoryManager(directory_storage)
    dm.save_directory(dir)
    dm.clean_directories()