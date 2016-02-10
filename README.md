# tranSMART Arborist
> An *arborist* [...] is a professional in the practice of arboriculture, which is the cultivation, management, and study of individual trees, shrubs, vines, and other perennial woody plants ([Wikipedia](https://en.wikipedia.org/wiki/Arborist))

Graphical tool to help you prepare your data for loading into the tranSMART data warehouse.

* * *
![Reordering the tranSMART data tree](/arborist/static/img/screenshot.png?raw=true "Reordering the tranSMART data tree")
* * *

## Functionality
* Browse your file system for tranSMART study folders or create a new one
* Create and edit your study and clinical parameter files
* Create and edit your study tree, as represented in the column mapping file
 * Adding data files to your study tree
 * Manually adding, deleting and drag-and-drop reordering of nodes in the tree
 * Editing the values in the columns file for each node

## Installation
Keep in mind the application has only been tested on Mac for now.
* Install the Python microframework Flask as described here: http://flask.pocoo.org/docs/0.10/installation/
* Download [the latest stable release](https://github.com/thehyve/transmart-arborist/releases/latest) from this repository

## Starting the application
* Run `python runserver.py` in your terminal, as described here: http://flask.pocoo.org/docs/0.10/quickstart
* Copy the URL from the terminal to your browser to open the application
 
## Loading data
Once your data is prepared we suggest using [transmart-batch](https://github.com/thehyve/transmart-batch) for loading it into tranSMART.
