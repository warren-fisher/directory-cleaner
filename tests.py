import unittest
from directory_clean import Directory, File 

class TestFileDeletion(unittest.TestCase):

    def SetUp(self):
        """Set up a sample directory structure."""
        self.D = Directory()

    def test_file_age(self):
        """Test if the program correctly identifies if a file is old enough"""

    def test_folder_age(self):
        """Test if the program correctly identifies if a folder is old enough"""

    def test_extension(self):
        """Test if the program correctly identifies if a file extension meets the requirements."""

    def test_dot_extensions(self):
        """Test to make sure that files of the form .name are not treated as extensions.
        
        For example a file named .gitignore is not of filetype gitignore."""

    def test_delete_file(self):
        """Test to make sure a file is deleted properly if it meets the requirements."""

    def test_delete_folder(self):
        """Test to make sure a folder is deleted properly if it meets the requirements."""

    def test_directory_paths(self):
        """Test to make to make sure that the script correctly identifies the paths for files."""

    def test_file_paths(self):
        """Test to make sure that the script correctly identifies the paths for folders.""" 

if __name__ == '__main__':
    unittest.main() 