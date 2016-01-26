# tranSMART Arborist
> An arborist, or (less commonly) arboriculturist, is a professional in the practice of arboriculture, which is the cultivation, management, and study of individual trees, shrubs, vines, and other perennial woody plants ([Wikipedia](https://en.wikipedia.org/wiki/Arborist))

Graphical tool for preparing your data for loading into the tranSMART data warehouse.

* * *
![Reordering the tranSMART data tree](/static/img/screenshot.png?raw=true "Reordering the tranSMART data tree")
* * *

## Functionality
* Uploading existing columns file
* Adding, deleting and reordering nodes in the tree
* Editing the values in the columns file for each node
* Downloading adjusted columns file

## Usage
Runs locally in the browser with the Python microframework Flask:
* Install Flask as described here: http://flask.pocoo.org/docs/0.10/installation/
* Then run `python curator.py` in your terminal, as described here: http://flask.pocoo.org/docs/0.10/quickstart
* Copy the URL from the terminal to your browser to open the application
 
## Loading data
Once your data is prepared we suggest using [transmart-batch](https://github.com/thehyve/transmart-batch) for loading it into tranSMART.
