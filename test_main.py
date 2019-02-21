import pytest
from directory_clean import Directory, File 
import errors
import os

def test_dotfiles_extension(tmp_path):
    """
    Creates a temporary .txt file and tests that the File class treats it as having no extension.
    
    Using the pytest tmp_path feature a temporary pathlib object is created for the base temporary directory.
    Subsequently a empty file '.txt.' is created in this directory. 
    Using the File class, if its file extension is empty, as expected, the test passes. 
    """
    d = tmp_path / "sub"
    d.mkdir()
    p = d / ".txt"
    assert File(p).extension == ''

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




