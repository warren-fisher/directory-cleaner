import click
import directory_clean as dc 

@click.command()
@click.option('--path', required=True, type=str, help='Directory path')
@click.option('--files', required=True, type=bool)
@click.option('--folders', required=True, type=bool)
@click.option('--age', required=True, type=int)
@click.option('--blocklist', default=None, type=bool)
@click.option('--extensions', default=None)
@click.option('--recursive', default=False, type=bool)
def track_directory(path, files, folders, age, **kwargs):
    d = dc.Directory(path, files, folders, age, **kwargs)
    d.deletion_process()

if __name__ == '__main__':
    track_directory()