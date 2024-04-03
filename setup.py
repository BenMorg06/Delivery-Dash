from cx_Freeze import setup, Executable

setup(
       name="Delivery Dash",
       version="1.0",

       description="Computer Science NEA",

       executables=[Executable("menu.py")],
   )   