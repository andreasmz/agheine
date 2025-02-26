# Patch for quickPBSA
# Created by Andreas 2025-02-26
# 
# Problem: quickPBSA is not suited for numpy 2, as it uses np.float removed from version 2. This script identifies the current working enviorenment and removes and patches the line if necessary



import sys
from pathlib import Path

try:
    import quickpbsa
except ModuleNotFoundError:
    print("Your enviorenment does not have quickPBSA installed. Terminating...")
    exit()

quickpbsa_path = Path(sys.executable).parent / "Lib" / "site-packages" / "quickpbsa"
if not quickpbsa_path.exists():
    print(f"Can't find the quickPBSA module inside your environment. Searched at {quickpbsa_path}")
    exit()

refinement_lowlevel_file_path = quickpbsa_path / "steps_refinement" / "refinement_lowlevel.py"
if not refinement_lowlevel_file_path.exists():
    print(f"Can't find the refinement_lowlevel.py file inside your quickPBSA module. Searched at {quickpbsa_path}")
    exit()

with open(refinement_lowlevel_file_path, 'r') as file:
    refinement_lowlevel_content = file.read()

refinement_lowlevel_content = refinement_lowlevel_content.replace("np.float('Inf')", "np.inf")

with open(refinement_lowlevel_file_path, 'w') as file:
    file.write(refinement_lowlevel_content)

print("Successfully patched your quickPBSA installation")