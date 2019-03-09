import click
from directory_clean import Directory, DirectoryManager
from directory_clean import directory_storage as directory_storage

@click.group()
def main():
    pass

@main.command()
@click.option('--path', required=True, type=str, help='Directory path')
@click.option('--files', required=True, type=bool)
@click.option('--folders', required=True, type=bool)
@click.option('--age', required=True, type=int)
@click.option('--blocklist', default=None, type=bool)
@click.option('--extensions', default=None)
@click.option('--recursive', default=False, type=bool)
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