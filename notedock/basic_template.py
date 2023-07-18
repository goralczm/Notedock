import json
import os

def get_basic_template():
    basic_template = {
        "Starting Up": {
            "Welcome!": "Say hi to Notedock! Slick and easy note app you have ever needed!",
            "Notebooks": "You can group notes in \"notebooks\", to create one, select File > Create Notebook",
            "Notes": "To create new one, select Options > Create Note in notebook. Afterwards, you can view, edit and delete them. Simply right-click or select Options menu in note preview",
            "Workspaces": "You can change workspace by clicking Workspaces menu item and selecting one! This is just a base template and all the changes here, won't be saved, to keep your notes, please select other workspace."
        },
        "Personal": {},
        "Work": {},
        "Ideas": {},
        "Dreams": {}
    }

    workspaces_folder = 'workspaces'

    if not os.path.exists(workspaces_folder):
        os.mkdir(workspaces_folder)
        for i in range(1, 4):
            with open(f'{workspaces_folder}/workspace{i}.json', 'w') as base_file:
                json.dump({}, base_file)
    with open(f'{workspaces_folder}/basic_template.json', 'w') as basic_template_file:
        json.dump(basic_template, basic_template_file, indent=4)