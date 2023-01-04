import os, glob
import cv2 as cv
from operator import itemgetter


listFile = 'spotmapsList.txt'

# `removeList`
#
# If the spotmapsList exists remove it
def removeList(config):

    outputFolder = itemgetter('outputFolder')(config)

    listFilePath = f'{outputFolder}{listFile}'

    if os.path.isfile(listFilePath) is True:

        os.remove(listFilePath)


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
    spotmapsList = []

    for infile in glob.glob(inputFolder + '*.*'):

        path_filename = os.path.split(infile)
        filename = path_filename[1].split('.')[0]

        print(f'Analysing: {filename}')

        if filename in spotmapsList:

            print('Already completed.')

        if ' CD' in filename:

            print(f'Ignoring {filename}: file part of series')

        else:

            capture = cv.VideoCapture(infile)
            totalFrames = int(capture.get(cv.CAP_PROP_FRAME_COUNT))

            if totalFrames == 0:

                print('Unable to read file.')

            else:

                spotmapsList.append(f'{filename}\n')

                with open(listFilePath, 'a') as myfile:
                    myfile.write(f'{filename}\n')
                    myfile.close()
