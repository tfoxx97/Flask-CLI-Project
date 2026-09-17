"""This CLI is designed to make setting up a Flask app much easier with the use of command prompts.
Features include:
- build base Flask template (includes routes, model dB setup, app config, utilities script, forms, etc.)
- build custom Flask template
    - specify what you're building
    - schema of dB
    - need blueprints?
    - CLI will go in depth to create folder structure + scripts you'll need based on your specs for the app
        you're building.
- install needed dependencies for project
    - provide requirements.txt file and it'll pip install for you.
"""
import cmd
from pathlib import Path
import os

__version__ = "1.0.0"

available_cmds = {
    'create': "Create a basic folder structure for your flask app.",
    'custom': "Build on top of framework and add customization to flask app like additional scripts, blueprints, etc.",
    'pip install': "Install dependencies to your app's virtual environment",
    'exit': "Exit the CLI. Come back again soon!"
}

arguments = {
    '-v or --version': 'Get the version number of the CLI'
}

class FlaskCLI(cmd.Cmd):
    intro = "Welcome to the Flask CLI. Use this to create a template based on your Flask app needs."
    prompt = ">>> "

    def do_flaskapp(self, arg):
        args = arg.split()
        for arg in args:
            match arg:
                case '-v' | '--version':
                    print(__version__)
                case 'create':
                    create_folder_structure()
                case 'custom':
                    create_custom_structure()
                case 'exit':
                    exit()
                case 'help':
                    self.do_help(arg)
                case _:
                    print("Unknown command. Please type help to see available commands")

    def do_help(self, arg):
        print("Available commands: ", sep='\n')
        print("--------------------", sep='\n')
        for cmd, description in available_cmds.items():
            print(f"flaskapp {cmd}: {description}")

        print("\nAdditional arguments: ",sep='\n')
        for arg_, desc in arguments.items():
            print(f"flaskapp {arg_}: {desc}")

def create_custom_structure(path='src'):
    skip_options = ['SKIP', 'no', 'n', 'N']
    print("Press `SKIP`, `no`, or `n` if you do not wish to change folder name")
    new_src = input("Enter name for file path (optional): ")
    if new_src and new_src not in skip_options:
        path = new_src
        path = os.path.join(os.getcwd(), path)
    else:
        path = os.path.join(os.getcwd(), path)

    structure = [
            f"{path}/run.py", 
            f"{path}/requirements.txt",
            f"{path}/README.md", 
            f"{path}/.gitignore",
            f"{path}/__init__.py",
            f"{path}/config/__init__.py",
            f"{path}/config/config.py",
            f"{path}/models.py",
            f"{path}/utils.py",
            f"{path}/routes.py",
            f"{path}/templates/base.html",
            f"{path}/static/main.css"
        ]
    
    for item in structure:
        path = Path(item)

        file_dir, file_name = os.path.split(path)

        if file_dir != "":
            os.makedirs(file_dir, exist_ok=True)
            print(f"Creating directory: {file_dir} for file {file_name}")

        if not os.path.exists(path) or os.path.getsize(path) == 0:
            with open(path, "w") as f:
                pass
            print(f"Creating empty file: {path}")
        else:
            print(f"File already exists: {path}")

    print("Done. Project folder structure created")

def create_folder_structure(path='src'):
    path = os.path.join(os.getcwd(), path)
    structure = [
        f"{path}/run.py", 
        f"{path}/requirements.txt",
        f"{path}/README.md", 
        f"{path}/.gitignore",
        f"{path}/__init__.py",
        f"{path}/config/__init__.py",
        f"{path}/config/config.py",
        f"{path}/models.py",
        f"{path}/utils.py",
        f"{path}/routes.py",
        f"{path}/templates/base.html",
        f"{path}/static/main.css"
    ]

    for item in structure:
        path = Path(item)

        file_dir, file_name = os.path.split(path)

        if file_dir != "":
            os.makedirs(file_dir, exist_ok=True)
            print(f"Creating directory: {file_dir} for file {file_name}")

        if not os.path.exists(path) or os.path.getsize(path) == 0:
            with open(path, "w") as f:
                pass
            print(f"Creating empty file: {path}")
        else:
            print(f"File already exists: {path}")

    print("Done. Project folder structure created")

if __name__ == "__main__":
    FlaskCLI().cmdloop()