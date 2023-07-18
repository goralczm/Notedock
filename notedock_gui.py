from datetime import date
from glob import glob
from typing import Tuple

import dearpygui.dearpygui as dpg
from screeninfo import get_monitors

from notedock.notedock import *
from notedock.helpers import create_dir

NOTEBOOK_SIZE: Tuple[int, int] = (300, 400)


def refresh() -> None:
    load_workspace_gui(0, None, current_workspace)


def hide_notebooks() -> None:
    for notebook in notes:
        dpg.delete_item(notebook)


def load_workspace_gui(sender, app_data, user_data: str) -> None:  # Requests loading notes from given workspace
    hide_notebooks()
    global notes
    notes = load_workspace(user_data)
    global current_workspace
    current_workspace = user_data
    reset_layout()


def reset_layout() -> None:  # Deletes all windows and creates new evenly spaced out
    x_offset, y_offset = 10, 30
    spacing = 10

    for notebook in notes:
        dpg.delete_item(notebook)
        for note_name in notes[notebook]:
            dpg.delete_item(f'{notebook}/{note_name}/Window')
        notebook_window(notebook, size=NOTEBOOK_SIZE, offset=(x_offset, y_offset))
        x_offset += NOTEBOOK_SIZE[0] + spacing

    dpg.delete_item('Create Note')
    dpg.delete_item('Edit Note')
    dpg.delete_item('Create Notebook')
    dpg.delete_item('Rename Notebook')


def load_fonts() -> None:  # Loads fonts in fonts folder
    with dpg.font_registry():
        fonts = glob('fonts/*.ttf')
        for font in fonts:
            global default_font
            default_font = dpg.add_font(font, 15)


def break_long_text(content: str, char_break_point: int = 80) -> str:  # Returns broken text considered by break point
    words_split = content.split(' ')
    output = words_split[0]

    char_count = len(words_split[0])
    for word in words_split[1:]:
        if char_count + len(word) <= char_break_point:
            output += f' {word}'
            char_count += len(word)
        else:
            output += f'\n{word}'
            char_count = 0

    return output


# Notebooks

def notebook_window(notebook_name: str, size: Tuple = (150, 150),
                    offset: Tuple = (0, 0)) -> None:  # Create notebook preview window
    with dpg.window(label=notebook_name, tag=notebook_name, width=size[0], height=size[1], pos=offset):
        with dpg.menu_bar():
            with dpg.menu(label='Notes'):
                pass
                dpg.add_menu_item(label='Create Note', callback=create_note_window, user_data=notebook_name)
            with dpg.menu(label='Options'):
                dpg.add_menu_item(label='Rename Notebook', callback=rename_notebook_window, user_data=notebook_name)
                dpg.add_menu_item(label='Delete Notebook', callback=lambda: delete_notebook_gui(notebook_name))

        notebook = get_notebook(notebook_name)
        for note in notebook:
            note_button(notebook_name, note)


def delete_notebook_gui(notebook_name: str) -> None:
    try:
        for note_name in notes[notebook_name]:
            dpg.delete_item(f'{notebook_name}/{note_name}/Window')
    except:
        pass
    delete_notebook(notebook_name)
    dpg.delete_item(notebook_name)
    reset_layout()


def rename_notebook_gui(sender, app_data, user_data: Dict) -> None:
    old_notebook_name = user_data.get('old_notebook_name')
    new_notebook_name = dpg.get_value(user_data.get('notebook_name_input'))

    rename_notebook(old_notebook_name, new_notebook_name)
    dpg.delete_item('Rename Notebook')
    reset_layout()


def rename_notebook_window(sender, app_data, user_data: str) -> None:
    dpg.delete_item('Rename Notebook')
    notebook_name = user_data

    with dpg.window(label='Rename Notebook', width=400, height=100, tag='Rename Notebook'):
        notebook_input = dpg.add_input_text(label='Notebook Name', default_value=notebook_name)
        dpg.add_button(label='Rename Notebook', callback=rename_notebook_gui,
                       user_data={'old_notebook_name': notebook_name,
                                  'notebook_name_input': notebook_input})


def add_notebook_gui(sender, app_data, user_data) -> None:  # Sends request to create new notebook
    notebook_name = dpg.get_value(user_data)
    notebook_name = add_notebook(notebook_name)
    notebook_window(notebook_name)
    dpg.delete_item('Create Notebook')
    reset_layout()


def create_notebook_window() -> None:  # Creates notebook creation window
    dpg.delete_item('Create Notebook')
    with dpg.window(label='Create Notebook', width=400, height=100, tag='Create Notebook'):
        notebook_input = dpg.add_input_text(label='Notebook Name', default_value='New Notebook')
        dpg.add_button(label='Create Notebook', callback=add_notebook_gui, user_data=notebook_input)


# Notes


def note_button(notebook_name: str, note_name: str) -> None:  # Create note button in notebook window
    note_button = dpg.add_button(label=note_name,
                                 tag=f'{notebook_name}/{note_name}',
                                 callback=lambda: note_window(notebook_name, note_name, (300, 400)),
                                 parent=notebook_name)
    with dpg.popup(note_button) as popup:
        dpg.add_button(label='Edit Note',
                       callback=edit_note_window,
                       user_data={'notebook_name': notebook_name,
                                  'note_name': note_name})
        dpg.add_button(label='Delete Note',
                       callback=delete_note_gui,
                       user_data={'notebook_name': notebook_name,
                                  'note_name': note_name,
                                  'popup_id': popup})


def note_window(notebook_name: str, note_name: str, size: Tuple = (150, 150),
                offset: Tuple = (0, 0)) -> None:  # Creates notes window with content
    dpg.delete_item(f'{notebook_name}/{note_name}/Window')
    with dpg.window(label=f'{notebook_name}/{note_name}', width=size[0], height=size[1], pos=offset,
                    tag=f'{notebook_name}/{note_name}/Window'):
        note_content = notes[notebook_name][note_name]

        dpg.add_text(note_name)
        dpg.add_text(break_long_text(note_content, 25))


def delete_note_gui(sender, app_data, user_data: Dict) -> None:
    notebook_name = user_data.get('notebook_name')
    note_name = user_data.get('note_name')
    popup_id = user_data.get('popup_id', 0)

    delete_note(notebook_name, note_name)
    dpg.delete_item(f'{notebook_name}/{note_name}')
    if popup_id != 0:
        dpg.delete_item(popup_id)


def edit_note_window(sender, app_data, user_data: Dict) -> None:
    dpg.delete_item('Edit Note')
    notebook_name = user_data.get('notebook_name')
    note_name = user_data.get('note_name')
    note_content = notes[notebook_name][note_name]

    with dpg.window(label='Edit Note', width=400, height=300, tag='Edit Note'):
        dpg.add_text(f'Notebook: {notebook_name}')
        name_input = dpg.add_input_text(label='Note Name', default_value=note_name)
        content_input = dpg.add_input_text(label='Note Content', default_value=note_content)
        dpg.add_button(label='Edit Note', callback=edit_note_gui, user_data={'notebook_name': notebook_name,
                                                                             'old_note_name': note_name,
                                                                             'note_name_input': name_input,
                                                                             'note_content_input': content_input})


def edit_note_gui(sender, app_data, user_data: Dict) -> None:
    notebook_name = user_data.get('notebook_name')
    old_note_name = user_data.get('old_note_name')
    note_name = dpg.get_value(user_data.get('note_name_input'))
    note_content = dpg.get_value(user_data.get('note_content_input'))

    delete_note_gui(sender, app_data, {'notebook_name': notebook_name,
                                       'note_name': old_note_name})
    note_name = add_note(notebook_name, note_name, note_content)
    dpg.delete_item(f'{notebook_name}/{old_note_name}/Window')
    note_button(notebook_name, note_name)
    dpg.delete_item('Edit Note')


def create_note_window(sender, app_data, user_data: str) -> None:
    dpg.delete_item('Create Note')
    notebook_name = user_data

    with dpg.window(label='Create Note', width=400, height=300, tag='Create Note'):
        dpg.add_text(f'Notebook: {notebook_name}')
        note_name_input = dpg.add_input_text(label='Note Name', default_value='New Note')
        note_content_input = dpg.add_input_text(label='Note Content', default_value='Content')
        dpg.add_button(label='Create Note', callback=add_note_gui, user_data={'notebook_name': notebook_name,
                                                                              'note_name_input': note_name_input,
                                                                              'note_content_input': note_content_input})


def add_note_gui(sender, app_data, user_data: Dict) -> None:
    notebook_name = user_data.get('notebook_name')
    note_name = dpg.get_value(user_data.get('note_name_input'))
    note_content = dpg.get_value(user_data.get('note_content_input'))

    note_name = add_note(notebook_name, note_name, note_content)
    note_button(notebook_name, note_name)
    dpg.delete_item('Create Note')


dpg.create_context()

load_fonts()
with dpg.viewport_menu_bar():
    dpg.bind_font(default_font)
    with dpg.menu(label='File'):
        dpg.add_menu_item(label='Add Notebook', callback=lambda: create_notebook_window())

    with dpg.menu(label='Workspaces'):
        workspaces = glob(f'{notes_folder}/*.json')
        for workspace in workspaces:
            workspace_name = workspace.split('\\')[-1]
            workspace_name_no_ext = workspace_name.split('.')[0]
            dpg.add_menu_item(label=workspace_name_no_ext, callback=load_workspace_gui, user_data=workspace_name_no_ext)

    with dpg.menu(label='View'):
        dpg.add_menu_item(label='Reset Layout', callback=lambda: reset_layout())
        dpg.add_menu_item(label='Refresh Data', callback=lambda: refresh())

    with dpg.menu(label='Extras'):
        dpg.add_menu_item(label='Style Editor', callback=lambda: dpg.show_style_editor())
        dpg.add_menu_item(label='Font Manager', callback=lambda: dpg.show_font_manager())
        dpg.add_menu_item(label='Item Registry', callback=lambda: dpg.show_item_registry())


create_dir('logs')
create_dir('logs/Notedock GUI')
logger.enable_logger('Notedock', f'logs/Notedock GUI/{date.today()}.log')
load_workspace_gui(0, None, 'basic_template')

screen_resolution = get_monitors()[0]
dpg.create_viewport(title='Notedock GUI', width=screen_resolution.width - 200, height=screen_resolution.height - 200)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()