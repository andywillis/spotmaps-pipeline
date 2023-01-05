import os, datetime

from list import buildList
from file import createFile
from process import processList

cwd = os.getcwd()

# Initialise info
contributor = 'Andy Willis'
year = datetime.date.today().year

# Initialise files
logFile = 'log.txt'
processedLogFile = 'processedFiles.txt'
listFile = 'spotmapsList.txt'

# Initialise folders
inputFolder = f'{cwd}\\files\\input\\'
outputFolder = f'{cwd}\\files\\output\\'

# Initialise config
config = {
    'contributor': contributor,
    'year': year,
    'inputFolder': inputFolder,
    'outputFolder': outputFolder,
    'logFile': logFile,
    'listFile': listFile,
    'processedLogFile': processedLogFile
}

# Pipeline

createFile(f'{outputFolder}{logFile}')
createFile(f'{outputFolder}{processedLogFile}')

buildList(config)
processList(config)
