import pytest
from directory_clean import Directory, File 
import errors
import os

@pytest.fixture(scope="session")
def create_temp_file():
    # Returns a helper function to be used to generate files
    def _temp_file(tmp_path, file_name='', file_extension='', text_string='CONTENT'):
        directory = tmp_path / "sub"
        directory.mkdir()
        path = directory / "{}.{}".format(file_name,file_extension)
        path.write_text(text_string) # This step creates the file at that location.
        return path
    return _temp_file

def test_dotfiles_extension(tmp_path, create_temp_file):
    """
    Creates a temporary .txt file and tests that the File class treats it as having no extension.
    
    Using the pytest tmp_path feature a temporary pathlib object is created for the base temporary directory.
    Subsequently a file named '.txt' is created.
    Using the File class, if its file extension is empty, as expected, the test passes. 
    """
    path = create_temp_file(tmp_path, file_extension='txt')
    print(path)
    assert File(path).extension == ''

def test_extension():
    """
    Tests against the README.md file to make sure that its file extension is .md, using the File class.
    """
    f = File('./README.md')
    assert f.extension == '.md'

def test_fake_file():
    """
    Tests the File class to make sure that an exception is raised if its path does not direct to a file. 
    """
    with pytest.raises(errors.NotAFileError):
        File('./fake_file_name')

def test_file_age():
    """
    Test to make sure that only files of the appropriate age are deleted. 
    
    [description]
    """
    pass
    



