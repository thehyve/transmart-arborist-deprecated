# Building an executable for Mac OS X
To build the code into a packaged executable for OS X you can use py2app. To do this, you can should run `python setup.py py2app` with all components required installed.

## Known issues
* When trying to build with py2app and you get stuck with an AttributeError on loading `<mf.scan_code>`, see this thread: [link](http://stackoverflow.com/questions/25394320/py2app-modulegraph-missing-scan-code)
