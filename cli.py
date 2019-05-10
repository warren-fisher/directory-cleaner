import click
from directory_clean import Directory, DirectoryManager
from directory_clean import directory_storage as directory_storage

@click.group()
def main():
    """
    Simple script that can be used to manage and deleted files and/or folders from specified directories over a certain age and/or of a specific file type.
    """
    pass

@main.command()
@click.option('--path', required=True, type=str, help='Directory path to add to tracking.')
@click.option('--files', required=True, type=bool, help='Should this script delete files?')
@click.option('--folders', required=True, type=bool, help='Should this script delete folders?')
@click.option('--age', required=True, type=int, help='Minimum age to delete folders and/or files.')
@click.option('--blocklist', default=None, type=bool, help="Set to true to enable whitelist, false for blacklist and leave empty for neither. Used in conjunction with --extensions.")
@click.option('--extensions', default=None, help="The extensions to delete/not delete depending on what --blocklist is set to.")
@click.option('--recursive', default=False, type=bool, help="Whether to search subdirectories recursively")
def track(path, files, folders, age, **kwargs):
    global directory_storage
    dm = DirectoryManager(directory_storage)
    d = Directory(path, files, folders, age, **kwargs)
    dm.save_directory(d)

@main.command()
def clean():
    global directory_storage
    dm = DirectoryManager(directory_storage)
    dm.clean_directories()

@click.option('--path', required=True,type=str,help='Directory path')
@main.command()
def remove(path):
    global directory_storage
    dm = DirectoryManager(directory_storage)
    dm.remove_directory(path)

if __name__ == '__main__':
    main()