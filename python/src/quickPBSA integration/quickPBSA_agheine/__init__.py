# Created by Andreas Brilka for internal use at the AG Heine
# C 06.02.2025

import tempfile
from pathlib import Path
import subprocess, os, platform
import shutil

def Start():
    print("---QuickPBSA Integration for AG Heine---\n")

    path_src = (Path(__file__).parent / "src").resolve()
    
    with tempfile.TemporaryDirectory(prefix="quickpbsa_integration") as temp_dir:
        shutil.copytree(str(path_src), str(Path(temp_dir) / "src"))
        notebook_path = (Path(temp_dir) / "src" / "quickPBSA notebook.ipynb")

        if platform.system() == 'Darwin':       # macOS
            subprocess.call(('open', notebook_path))
        elif platform.system() == 'Windows':    # Windows
            os.startfile(notebook_path)
        else:                                   # linux variants
            subprocess.call(('xdg-open', notebook_path))
        print(f"There should have opened a Python notebook in a seperate window. If not, try to follow this path: {notebook_path.resolve()}")
        input(f"To clean up the directory, press any KEY to continue...")

        print("---Terminating QuickPBSA Integration for AG Heine---")


if __name__ == "__main__":
    Start()