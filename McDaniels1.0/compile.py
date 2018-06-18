import cx_Freeze, os

executables  = [cx_Freeze.Executable("main.py")]



os.environ['TCL_LIBRARY'] = r'C:\Users\Daniel\AppData\Local\Programs\Python\Python36\tcl\tcl8.6'
os.environ['TK_LIBRARY'] = r'C:\Users\Daniel\AppData\Local\Programs\Python\Python36\tcl\tk8.6'

cx_Freeze.setup(
    name="Wcdonald Game",
    options={"build_exe": {"packages":["pygame"],
                           "include_files":['data']}},

    executables =executables 
)
