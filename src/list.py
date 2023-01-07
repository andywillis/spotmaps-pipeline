from os import path
from glob import glob
from operator import itemgetter

from file import removeFile, appendToFile, getListFromFileContents

import cv2

from format import rinseFilename

# Global
listFile = 'spotmapsList.txt'


# `removeList`
#
# If the spotmapsList exists remove it
def removeList(config):

    outputFolder = itemgetter('outputFolder')(config)
    listFilePath = f'{outputFolder}{listFile}'
    removeFile(listFilePath)


# `buildList`
#
# Build a new spotmaps list by iterating
# over the files in the input folder, and adding
# them to the file
def buildList(config):

    inputFolder, outputFolder = itemgetter(
        'inputFolder', 'outputFolder'
    )(config)

    listFilePath = f'{outputFolder}{listFile}'

    spotmapsList = getListFromFileContents(listFilePath)

    for infile in glob(inputFolder + '*.*'):

        path_filename = path.split(infile)
        filename = rinseFilename(path_filename[1]).split('.')[0]

        if filename != 'README':

            print(f'Analysing: {filename}')

            if ' CD' in filename:

                print(f'Ignoring {filename}: file part of series')

            if filename in spotmapsList:

                print('Already processed.')

            else:

                capture = cv2.VideoCapture(infile)
                totalFrames = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))

                if totalFrames == 0:

                    print('Unable to read file.')

                else:

                    spotmapsList.append(f'{filename}\n')
                    appendToFile(listFilePath, filename)
