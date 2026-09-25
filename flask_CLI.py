import cmd, os, subprocess, re
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

__version__ = "1.1.0"

available_cmds = {
    'create': "Create a basic folder structure for your flask app.",
    'custom': "Build on top of framework and add customization to flask app like additional scripts, blueprints, etc.",
    'install': "Install dependencies to your app's virtual environment",
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
        if len(args) < 2:
            for arg in args:
                match arg:
                    case '-v' | '--version':
                        print(__version__)
                    case 'create':
                        create_folder_structure()
                    case 'custom':
                        create_custom_structure()
                    case 'install':
                        install()
                    case 'exit':
                        exit()
                    case 'help':
                        self.do_help(arg)
                    case _:
                        print("Unknown command. Please type help to see available commands.")
        else:
            print("Too many arguments. Type flaskapp help to see list of available commands.")

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

def get_cwdirs():
    dirs = os.listdir(os.getcwd())
    for dir in dirs:
        if dir.endswith('.py') or dir.startswith('.env'):
            dirs.remove(dir)

    return dirs

def verify_pip_is_installed():
    try:
        pip_check = subprocess.run("pip --version", capture_output=True)
        output = pip_check.stdout
        pattern = rb"pip (\d{2,3}.\d{1,2}.\d{1,2})"
        match1 = re.match(pattern, output)
        if match1:
            print("pip found on local machine.")
            return True
        else:
            return False
    except subprocess.CalledProcessError:
        return False

def create_venv():
    #TODO: check if venv already exists
    try:
        subprocess.run("python -m venv .env")
        print("Creating virtual environment...")
    except (BaseException, Exception, subprocess.CalledProcessError) as e:
        print(f"Error creating virtual environment: {type(e)}: {e}")

    print("Creating venv finished.")

def verfiy_requirements_txt():
    '''Verify requirements.txt exists. If not, raise error. Verify file is not empty. If it is raise error.'''
    dirs = get_cwdirs()

    try:
        filepath = os.path.join(os.getcwd(), dirs[1], 'requirements.txt')
        if os.path.exists(filepath) and os.path.getsize(filepath) > 0:
            print("requirements.txt found.")
            return True
    except IndexError:
        print("Project folder not found. Please create project folder before attempting pip install.")
    except FileNotFoundError:
        print("requirements.txt file not found. Please check project folder.")

    return False

def run_pip_install():
    dirs = get_cwdirs()
    filepath = os.path.join(os.getcwd(), dirs[1], 'requirements.txt')

    try:
        subprocess.run(f"pip install -r {filepath}")
    except Exception as e:
        print(f"Unexpected error: {type(e)}: {e}")

    print("Installing dependencies process finished")

def install():
    with ThreadPoolExecutor(max_workers=1) as executor:
        tasks = [verify_pip_is_installed, create_venv, verfiy_requirements_txt, run_pip_install]
        for i, task in enumerate(tasks, 1):
            future = executor.submit(task)
            try:
                future.result()
            except Exception as e:
                print(f"Error: stopped at task {i}: {type(e)}: {e}")
                break
            else:
                print("Task completed successfully.") 

if __name__ == "__main__":
    FlaskCLI().cmdloop()