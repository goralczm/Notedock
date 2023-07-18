import shlex
from dataclasses import dataclass
from datetime import date
from glob import glob
from inspect import signature
from typing import Callable

from notedock.notedock import *
from notedock.helpers import create_dir

def refresh() -> None:
    global notes
    notes = load_workspace(current_workspace)


def list_workspaces() -> None:
    workspaces = glob(path.join(notes_folder, '*.json'))
    print('--- Workspaces ---')
    for workspace in workspaces:
        formatted_name = workspace.split('\\')[1]
        no_ext_name = formatted_name.split('.')[0]
        if no_ext_name == current_workspace:
            print(f'{no_ext_name} *')
        else:
            print(no_ext_name)


def list_notebooks() -> None:
    print('--- Notebooks ---')
    for notebook in notes:
        print(notebook)


def list_all() -> None:
    list_workspaces()
    print()
    print('--- Notebooks ---')
    for notebook in notes:
        print(notebook)
        for note in notes[notebook]:
            print(f' - {note}')


def show_note(notebook_name: str, note_name: str) -> None:
    notebook = get_notebook(notebook_name)
    if notebook is None:
        return

    if note_name not in notebook.keys():
        logger.logger.warning(f'Could not find {note_name} note in {notebook_name} notebook')
        return

    print(f'--- {notebook_name}/{note_name} ---')
    print(notebook[note_name])


def help() -> None:
    for command_name in commands:
        command = commands[command_name]
        params = signature(command.function).parameters
        formatted_params = [f'<{param}>' for param in params]
        print(f'- {command_name} {" ".join(formatted_params)}: {command.description}')


def load_workspace_cli(workspace_name) -> None:
    global notes
    notes = load_workspace(workspace_name)

    if not workspace_name:
        return

    global current_workspace
    current_workspace = workspace_name


@dataclass
class Command:
    function: Callable
    description: str


commands = {
    'help': Command(help, 'Displays all available commands'),
    'refresh': Command(refresh, 'Refreshed data'),
    'workspaces_ls': Command(list_workspaces, 'Lists all workspaces'),
    'notebooks_ls': Command(list_notebooks, 'Lists all notebooks'),
    'ls': Command(list_all, 'Lists all notebooks with their notes'),
    'change_workspace': Command(load_workspace_cli, 'Changes current workspace'),
    'add_notebook': Command(add_notebook, 'Adds new notebook'),
    'rename_notebook': Command(rename_notebook, 'Renames notebook'),
    'delete_notebook': Command(delete_notebook, 'Delets notebook'),
    'add_note': Command(add_note, 'Adds note to the notebook'),
    'edit_note': Command(edit_note, 'Edits note'),
    'delete_note': Command(delete_note, 'Deletes notes'),
    'show_note': Command(show_note, 'Previews note content')
}

if __name__ == '__main__':
    create_dir('logs')
    create_dir('logs/Notedock CLI')
    logger.enable_logger('Notedock', f'logs/Notedock CLI/{date.today()}.log')
    load_workspace_cli('basic_template')

    print()
    user_input = shlex.split(input('Please type a command: ').strip())
    command_name, flags = user_input[0], user_input[1:]
    while command_name.lower() != 'exit':
        try:
            command = commands[command_name]
        except KeyError:
            logger.logger.warning(f'Could not find {command_name} command')
        else:
            args = signature(command.function).parameters

            if len(args) == 0:
                command.function()
            else:
                try:
                    command.function(*flags)
                except TypeError:
                    logger.logger.warning('Number of required parameters for this command does not match')
                    print()
                    help()
            print()

        print()
        user_input = shlex.split(input('Please type a command: ').strip())
        command_name, flags = user_input[0], user_input[1:]