import sys
from cx_Freeze import setup, Executable

build_exe_options = {
    "packages": ["tkinter", "sqlite3", "random"],
    "include_files": ["jogar.png", "exit.png", "check.png", "repetir.png", "capitais.db"]
}

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="GeoQuiz",
    version="1.0",
    description="GeoQuiz game converted to executable",
    options={"build_exe": build_exe_options},
    executables=[Executable("geoquiz.py", base=base)]
)
