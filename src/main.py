import os, datetime

from list import removeList, buildList
from process import processList

cwd = os.getcwd()

# Initialise info
author = 'Andy Willis'
year = datetime.date.today().year

# Initialise folders
inputFolder = f'{cwd}\\files\\input\\'
outputFolder = f'{cwd}\\files\\output\\'

# Initialise config
config = {
    'author': author,
    'year': year,
    'inputFolder': inputFolder,
    'outputFolder': outputFolder
}

# Pipeline
removeList(config)
buildList(config)
# processList(config)
