import click
from directory_clean import Directory, DirectoryManager

directory_storage = r'c:\Users\warren\Downloads\settings.pkl'

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
    d = Directory(path, files, folders, age, **kwargs)
    dm = DirectoryManager(r'c:\Users\warren\Downloads\settings.pkl')
    dm.save_directory(d)

@main.command()
def clean():
    dm = DirectoryManager(r'c:\Users\warren\Downloads\settings.pkl')
    dm.clean_directories()

if __name__ == '__main__':
    main()