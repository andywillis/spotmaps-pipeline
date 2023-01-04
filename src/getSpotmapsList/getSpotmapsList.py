import os
from removeSpotmapsList import removeSpotmapsList
from buildFileList import buildFileList

cwd = os.getcwd()

# Initialise
inputFolder = f'{cwd}\\files\\input\\'
outputFolder = f'{cwd}\\files\\output\\'
spotmapsListFile = 'spotmapsList.txt'
spotmapsListFilePath = f'{outputFolder}{spotmapsListFile}'

# Execute
removeSpotmapsList(spotmapsListFilePath)
buildFileList(inputFolder, spotmapsListFilePath)
