import cx_Freeze
import sys

base = None
if sys.platform == "win32":
    base = "Win32GUI"
shortcut_table = [
    ("DesktopShortcut", 
    "DesktopFolder",
    "snake game",
    "TARGETDIR",
    "[TARGETDIR]\\snakegame.exe", #target
    None, #Arguments
    None, #description
    None, #hotkey
    None, #Icon
    None, #Iconindex
    None, #ShowCmd
    "TARGETDIR",
    )
]
msi_data = {"Shortcut": shortcut_table}

bdist_msi_option = {'data': msi_data}

executables = [cx_Freeze.Executable(script="snakegame.py", icon='snake.ico', base=base)]

cx_Freeze.setup(
    version="6.4.2",
    description="Snake game",
    aurthor="MrSnake",
    options={"build_exe": {"packages":["pygame"],
                          "include_files":['snake.ico']},
             "bdist_msi":bdist_msi_option,
             },            
    executables = executables
)
