import os, glob, time
import cv2 as cv

import removeSpotmapsList
import iterateFilmFiles

# Initialise folders
inputFolder = 'files\\input\\'
outputFolder = 'files\\output\\'

# Initialise files
spotmapsListFile = 'spotmapsList.txt'
# logFile = 'log.txt'

# Initialise paths
spotmapsListFilePath = f'{outputFolder}\\{spotmapsListFile}'
# logFilePath = f'{outputFolder}\\{logFile}'

removeSpotmapsList(spotmapsListFilePath)
iterateFilmFiles(spotmapsListFilePath)
