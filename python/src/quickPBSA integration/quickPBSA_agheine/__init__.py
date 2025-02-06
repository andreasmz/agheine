# Created by Andreas Brilka for internal use at the AG Heine
# C 06.02.2025

import tempfile
from pathlib import Path
import subprocess, os, platform

def Start():
    print("---QuickPBSA Integration for AG Heine---\n")
    if not (notebook_local_path := (Path(__file__).parent / "quickPBSA notebook.ipynb").resolve()).exists():
        raise RuntimeError(f"Can't find the notebook in the installation directory ({notebook_local_path}). Try to reinstall the package.")

    with open(notebook_local_path, "rb") as f:
        notebook_local_content = f.read()

    if len(notebook_local_content) == 0:
        raise RuntimeError(f"The shipped notebook is empty. Try to reinstall the package")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        with open(notebook_path := (Path(temp_dir) / "quickPBSA notebook.ipynb"), "wb+") as f:
            f.write(notebook_local_content)
        if platform.system() == 'Darwin':       # macOS
            subprocess.call(('open', notebook_path))
        elif platform.system() == 'Windows':    # Windows
            os.startfile(notebook_path)
        else:                                   # linux variants
            subprocess.call(('xdg-open', notebook_path))
        print(f"There should have opened a Python notebook in a seperate window. If not, try to follow this path: {notebook_path.resolve()}")
        input(f"To clean up the directory, press any KEY to continue...")


if __name__ == "__main__":
    Start()