import pytest
import os, sys
# Modify path so that files can be properly imported without having to install the setup.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from directory_clean import DirectoryManager
import errors
from test_File import create_temp_file as create_temp_file


def test_fake_file():
    with pytest.raises(errors.NotAFileError):
        DirectoryManager('./fake_file_name')


def test_not_a_settings_file(tmp_path, create_temp_file):
    with pytest.raises(errors.NotASettingsFile):
        path = create_temp_file(tmp_path, file_name='fake_settings_file',
                         file_extension='.fake')
        DirectoryManager(path)