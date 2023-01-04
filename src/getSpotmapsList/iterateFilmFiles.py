import os, glob, time
import cv2 as cv

spotmapsList = []

def iterateFilmFiles(spotmapsListFilePath):

    for infile in glob.glob(input + '*.*'):

        startTime = time.time()

        path, filename = os.path.split(infile)
        filename = filename.split('.')[0]

        print(f'Analysing: {filename}')

        if filename in spotmapsList:

            print('Already completed.')

        if ' CD' in filename:

            print(f'Ignoring {filename}: file part of series')

        else:

            capture = cv.CaptureFromFile(infile)

            totalFrames = int(cv.GetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_COUNT))

            if totalFrames == 0:

                print('Unable to read file.')

            else:

                spotmapsList.append(f'{filename}\n')

                with open(spotmapsListFilePath, 'a') as myfile:
                    myfile.write(f'{filename}\n')
                    myfile.close()
