import os
from pathlib import Path

project_name = "Chatbot"

list_of_files = [

    f"{project_name}/__init__.py",
    f"{project_name}/langchain_service/__init__.py",
    f"{project_name}/langchain_service/langchain_service.py",
    f"{project_name}/config/__init__.py",
    f"{project_name}/exception/__init__.py",
    f"{project_name}/logger/__init__.py",
    f"{project_name}/utils/__init__.py",
    f"{project_name}/utils/main_utils.py",
    "app.py",
    "requirements.txt",
    "setup.py",
    "Dockerfile",
    ".dockerignore"
]



for filepath in list_of_files:
    filepath = Path(filepath)
    filedir, filename = os.path.split(filepath)
    if filedir != "":
        os.makedirs(filedir, exist_ok=True)
    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        with open(filepath, "w") as f:
            pass
    else:
        print(f"file is already present at: {filepath}")
