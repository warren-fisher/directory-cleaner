import pytest
import sys, os
import string
import random
# Modify path so that files can be properly imported without having to install the setup.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from directory_clean import Directory
from test_File import create_temp_file
import errors

@pytest.fixture(scope="session")
def create_temp_dir(create_temp_file):
    
    def _random_name():
        letters = string.ascii_lowercase
        name = "".join(random.choice(letters) for i in range(10))
        return name

    def _temp_dir(tmp_path, dirname="", num_files_to_create=2):
        directory = tmp_path / "test_dir"
        directory.mkdir()
        file_names = []
        for i in range(num_files_to_create):
            name = _random_name()
            while name in file_names:
                name = _random_name()
            file_names.append(create_temp_file(tmp_path, name, file_extension=".txt", directory=directory))  
        return (directory, file_names)
        
    return _temp_dir

def test_get_files(tmp_path, create_temp_dir):
    """
    Tests the Directory class to make sure that the files in a directory are properly obtained.
    """
    dir_path, file_paths = create_temp_dir(tmp_path, "getFiles", 10)
    direct = Directory(dir_path, True, True, 1)
    direct.get_files()
    files = direct.files
    
    # Sort them so we can compare files at same index
    files = sorted(files)
    file_paths = sorted(file_paths)

    for i, f in enumerate(files):
        assert f == file_paths[i]