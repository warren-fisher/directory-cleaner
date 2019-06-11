import pytest
from directory_clean import File
import errors
from time import time, sleep


@pytest.fixture(scope="session")
def create_temp_file():
    # Returns a helper function to be used to generate files
    def _temp_file(tmp_path, file_name='', file_extension='', text_string='CONTENT'):
        directory = tmp_path / "sub"
        directory.mkdir()
        path = directory / "{}.{}".format(file_name, file_extension)
        path.write_text(text_string)  # This step creates the file at that location.
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
    assert File(path).extension == ''


def test_extension(tmp_path, create_temp_file):
    """
    Tests against the README.md file to make sure that its file extension is .md, using the File class.
    """
    temp_file = create_temp_file(tmp_path, file_extension='txt', file_name='txt')
    f = File(temp_file)
    assert f.extension == '.txt'


def test_fake_file():
    """
    Tests the File class to make sure that an exception is raised if its path does not direct to a file. 
    """
    with pytest.raises(errors.NotAFileError):
        File('./fake_file_name')


def test_file_age(tmp_path, create_temp_file):
    """
    Test to make sure that file age is correctly tested.
    """
    start_time = time()
    path = create_temp_file(tmp_path, file_name='age', file_extension='txt')
    sleep(0.1)
    f = File(path)
    end_time = time()
    time_taken = end_time - start_time
    # The os.stat() attribute st_mtime has a resolution of two seconds,
    # so the file age should be within 2 seconds of the time taken for the File to be initiated.
    assert f.age >= time_taken - 2 and f.age <= time_taken + 2


def test_file_init(tmp_path, create_temp_file):
    temp_file = create_temp_file(tmp_path, file_extension='txt', file_name='txt')
    f = File(temp_file)
    assert f.path == temp_file


def test_empty_file_init():
    with pytest.raises(TypeError):
        File()


def test_file_deletion(tmp_path, create_temp_file):
    temp_file = create_temp_file(tmp_path, file_extension='txt', file_name='txt')
    f = File(temp_file)
    f.delete()
    with pytest.raises(FileNotFoundError):
        f.delete()
