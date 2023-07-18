import json
from os import path
from typing import Dict

from notedock.basic_template import get_basic_template
from notedock.logger import Logger
from notedock.helpers import create_dir

indents = 4

notes_folder = 'workspaces'
notes_path = ''
notes = {}

logger = Logger()


def load_workspace(workspace_name) -> Dict:
    if not workspace_name:
        logger.logger.warning('Cannot load workspace without a name')
        return

    global notes_path
    notes_path = path.join(notes_folder, f'{workspace_name}.json')
    global notes
    notes = load_json_notes()
    logger.logger.info(f'Loaded \"{workspace_name}\" workspace')
    return notes


def load_json_notes() -> Dict:
    try:
        with open(notes_path, 'r') as notes_file:
            logger.logger.debug(f'Workspace file found, loading notes from {notes_path}')
            return json.load(notes_file)
    except:
        logger.logger.debug('No workspace file found, initializing empty')
        if not path.exists(notes_folder):
            create_dir(notes_folder)
        with open(notes_path, 'w') as notes_file:
            json.dump({}, notes_file, indent=indents)
        return {}


def get_valid_name(d: Dict, name: str) -> str:
    name_split = name.split(' ')
    if name_split[-1].isnumeric():
        original_name = ' '.join(name_split[:-1])
    else:
        original_name = name
    index = 1
    while name in list(d.keys()):
        name = f'{original_name} {index}'
        index += 1

    return name


def save_notes() -> None:
    with open(notes_path, 'w') as notes_file:
        json.dump(notes, notes_file, indent=indents)
    logger.logger.debug('Saving notes')


def get_notebook(notebook_name: str) -> Dict:
    try:
        notebook = notes[notebook_name]
    except KeyError:
        logger.logger.warning(f'Cannot find \"{notebook_name}\" notebook')
        return
    else:
        return notebook


def add_notebook(notebook_name: str) -> str:
    if not notebook_name:
        logger.logger.warning('Cannot create notebook without name')
        return

    notebook_name = get_valid_name(notes, notebook_name)

    logger.logger.info(f'Created new \"{notebook_name}\" notebook')

    notes[notebook_name] = {}
    save_notes()

    return notebook_name


def delete_notebook(notebook_name: str) -> None:
    try:
        del (notes[notebook_name])
    except KeyError:
        logger.logger.warning(f'Cannot find \"{notebook_name}\" notebook')
    else:
        logger.logger.info(f'Deleted \"{notebook_name}\" notebook')
        save_notes()


def rename_notebook(old_notebook_name: str, new_notebook_name: str) -> None:
    try:
        notes[new_notebook_name] = notes[old_notebook_name]
        del (notes[old_notebook_name])
    except KeyError:
        logger.logger.warning(f'Cannot find \"{old_notebook_name}\" notebook')
    else:
        logger.logger.info(f'Renamed \"{old_notebook_name}\" notebook to \"{new_notebook_name}\"')
        save_notes()


def add_note(notebook_name: str, note_name: str, note_content: str) -> str:
    notebook = get_notebook(notebook_name)
    if notebook is None:
        return

    note_name = get_valid_name(notebook, note_name)
    notebook[note_name] = note_content
    logger.logger.info(f'Created \"{note_name}\" note in \"{notebook_name}\" notebook')
    save_notes()
    return note_name


def edit_note(notebook_name: str, old_note_name: str, new_note_name: str, note_content: str) -> None:
    notebook = get_notebook(notebook_name)
    if notebook is None:
        return

    try:
        del (notebook[old_note_name])
    except KeyError:
        logger.logger.warning(f'Note \"{old_note_name}\" cannot be found in \"{notebook_name}\" notebook')

    new_note_name = get_valid_name(notebook, new_note_name)
    notebook[new_note_name] = note_content
    logger.logger.info(f'Edited \"{old_note_name}\" note')
    save_notes()


def delete_note(notebook_name: str, note_name: str) -> None:
    notebook = get_notebook(notebook_name)
    if notebook is None:
        return

    try:
        del (notebook[note_name])
    except KeyError:
        logger.logger.warning(f'Cannot find {note_name} note in {notebook_name} notebook')
    else:
        save_notes()
        logger.logger.info(f'Deleted {note_name} note from {notebook_name} notebook')


get_basic_template()