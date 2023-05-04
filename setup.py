import sys
from cx_Freeze import setup, Executable

build_exe_options = {
    "build_exe": "dist",
    "include_files": ["Styles", "Assets", "PluginWidgets", "Saves"],
}

# base="Win32GUI" should be used only for Windows GUI app
base = "Win32GUI" if sys.platform == "win32" else None

setup(
    name="OpenNote",
    version="1",
    description="An open source, extensible, cross-platform note-taking application",
    options={"build_exe": build_exe_options},
    executables=[Executable("main.py", 
                    base=base, 
                    target_name="OpenNote", 
                    icon="./Assets/icons/OpenNoteLogo.ico"
                )],
)

