from os import mkdir, remove
from shutil import rmtree

def create_dir(path: str) -> None:
    try:
        mkdir(path)
    except FileExistsError:
        pass


def remove_file(path: str) -> None:
    try:
        remove(path)
    except FileNotFoundError:
        pass


def remove_tree(path: str) -> None:
    try:
        rmtree(path)
    except:
        pass