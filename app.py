import streamlit as st
import os
import sys
import importlib.util

# Set the folder to the current working directory
folder = os.path.abspath(os.getcwd())

# Get folder names for all directories containing a main.py file
this_file = os.path.abspath(__file__)
project_folders = []

for subdir in os.listdir(folder):
    subdir_path = os.path.join(folder, subdir)
    if os.path.isdir(subdir_path):
        main_file_path = os.path.join(subdir_path, 'main.py')
        if os.path.exists(main_file_path) and main_file_path != this_file:
            project_folders.append(subdir)

# Make a UI to run different files
selected_project = st.sidebar.selectbox('Select an app', project_folders)

# Create module from filepath and put in sys.modules, so Streamlit knows to watch it for changes
fake_module_count = 0

def load_module(filepath):
    global fake_module_count
    modulename = '_dont_care_%s' % fake_module_count
    spec = importlib.util.spec_from_file_location(modulename, filepath)
    module = importlib.util.module_from_spec(spec)
    sys.modules[modulename] = module
    fake_module_count += 1

# Run the selected project's main.py file
if selected_project:
    project_path = os.path.join(folder, selected_project, 'main.py')
    with open(project_path) as f:
        load_module(project_path)
        filebody = f.read()
    compiled_code = compile(filebody, filename=project_path, mode='exec')
    exec(compiled_code, {})
