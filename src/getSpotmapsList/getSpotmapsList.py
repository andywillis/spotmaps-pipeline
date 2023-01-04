import removeSpotmapsList
import iterateFilmFiles

# Initialise
inputFolder = 'files\\input\\'
outputFolder = 'files\\output\\'
spotmapsListFile = 'spotmapsList.txt'
spotmapsListFilePath = f'{outputFolder}\\{spotmapsListFile}'

# Execute
removeSpotmapsList(spotmapsListFilePath)
iterateFilmFiles(spotmapsListFilePath)
