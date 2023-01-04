import os, glob, time
import cv2 as cv

# Initialise array
spotmapsList = []

def buildFileList(inputFolder, spotmapsListFilePath):

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

                with open(spotmapsListFilePath, 'a') as myfile:
                    myfile.write(f'{filename}\n')
                    myfile.close()
