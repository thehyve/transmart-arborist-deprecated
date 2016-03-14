# Building an executable for Windows
To build the code into a packaged executable for Windows you can use py2exe. To do this, you can should run `python setup.py py2exe` with all components required installed.

## Tips
* Building is recommended when having installed 32bit Python (Windows version should not matter). Building on 64bit Python as not been tested. Furthermore, the executable would not be able to run on 32 bit Windows while not providing any benefits to the user.
