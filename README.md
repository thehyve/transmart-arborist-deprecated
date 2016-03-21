# tranSMART Arborist
> An *arborist* [...] is a professional in the practice of arboriculture, which is the cultivation, management, and study of individual trees, shrubs, vines, and other perennial woody plants ([Wikipedia](https://en.wikipedia.org/wiki/Arborist))

Graphical tool to help you prepare your data for loading into the tranSMART data warehouse.

* * *
![Boris](/resources/images/boris_full.svg "Boris!")
![Reordering the tranSMART data tree](/resources/images/screenshot.png?raw=true "Reordering the tranSMART data tree")
* * *

## Functionality
* Browse your file system for tranSMART study folders or create a new one
* Create and edit your study and clinical parameter files
* Create and edit your study tree, as represented in the column mapping file
 * Adding data files to your study tree
 * Manually adding, deleting and drag-and-drop reordering of nodes in the tree
 * Editing the values in the columns file for each node

## Installation
Keep in mind the application has only been tested on Mac OS X 10.10 or newer, and Windows 7 or newer.  Although for now the application runs on both Python2 and Python3 we recommend the latter.
* Clone this repository and run the setup with `python3 setup.py install`.
 * Use `git clone --recursive` OR run `git module init` and `git module update` to also download a transmart test dataset.
* Download [the latest stable release](https://github.com/thehyve/transmart-arborist/releases/latest) from this repository

## Starting the application
* Run `python3 runserver.py` in your terminal, this should open The Arborist in your default webbrowser.
* Additional running options can be viewed by running `python3 runserver.py --help`

## Loading data
Once your data is prepared we suggest using [transmart-batch](https://github.com/thehyve/transmart-batch) for loading it into tranSMART.

## For additional documentation
See these [docs](docs).
