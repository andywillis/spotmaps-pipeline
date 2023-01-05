from __future__ import division
from operator import itemgetter

import os, glob, math, sys, time, json

import cv2 as cv
from PIL import Image, ImageDraw
import numpy as np

from file import getListFromFileContents, appendToFile


# `processList`
#
# Iterate over the files and produce spotmap images
# and JSON
def processList(config):

    os.system('cls')

    (contributor,
     inputFolder,
     outputFolder,
     logFile,
     processedLogFile,
     listFile) = itemgetter(
        'contributor', 'inputFolder', 'outputFolder',
        'logFile', 'processedLogFile', 'listFile'
    )(config)

    logFilePath = f'{outputFolder}{logFile}'
    listFilePath = f'{outputFolder}{listFile}'
    processedLogPath = f'{outputFolder}{processedLogFile}'

    # removeFile(logFilePath)
    fileList = getListFromFileContents(listFilePath)
    processedList = getListFromFileContents(processedLogPath)

    print('Retrieved lists')

    for currentFile in glob.glob(inputFolder + '*.*'):

        startTime = time.time()

        path_filename = os.path.split(currentFile)
        filename = path_filename[1].split('.')[0]

        if filename in processedList:

            print(f'{filename} - already completed.')

        else:

            if filename in fileList:

                capture = cv.VideoCapture(currentFile)
                totalFrames = int(capture.get(cv.CAP_PROP_FRAME_COUNT))

                try:

                    print('********')

                    fps = int(capture.get(cv.CAP_PROP_FPS))

                    print(f'Analysing: {filename} / {str(totalFrames)} frames / {str(fps)} fps')

                    numberOfSpots = int(math.floor(totalFrames / fps))
                    numberOfMinutes = int(math.ceil(numberOfSpots / 60))
                    trimFrames = numberOfSpots * fps
                    missing = 60 - numberOfSpots % 60
                    completeNumberOfSpots = numberOfSpots + missing

                    if missing == 60:

                        missing = 0

                    # Build rgbArray, 4 columns because we're using RGBA instead of plain RGB.
                    rgbData = np.zeros((completeNumberOfSpots, 3), dtype=np.int32)

                    frame = 1
                    spot = 1
                    frameInSecond = 1
                    spotR = spotG = spotB = 0

                    while frame <= trimFrames:

                        ret, snapshot = capture.read()

                        if not ret:

                            print('Frame could not be read')

                        # create an image 1 pixel wide
                        point = cv.CreateImage((1, 1), cv.IPL_DEPTH_8U, 3)
                        
                        # resize the frame to the point
                        cv.Resize(snapshot, point, cv.INTER_AREA)

                        # get the rgb data from that point
                        r = int(point[0, 0][2])
                        g = int(point[0, 0][1])
                        b = int(point[0, 0][0])

                        if frameInSecond > 1:

                            spotR = spotR + r
                            spotG = spotG + g
                            spotB = spotB + b

                        if frameInSecond == fps:

                            percent = spot / numberOfSpots * 100
                            sys.stdout.write("Completed: %d%% \r" % (percent))
                            spotR = int(spotR / fps)
                            spotG = int(spotG / fps)
                            spotB = int(spotB / fps)

                            # NOTE: the full opacity value here '1' not '255'
                            # since the color array is used for Canvas rather than Python.
                            rgbData[spot - 1] = (spotR, spotG, spotB)
                            frameInSecond = 0
                            spot += 1
                            spotR = spotG = spotB = 0

                        frame += 1
                        frameInSecond += 1

                    second = 1

                    while second <= missing:

                        rgbData[spot - 1] = (spotR, spotG, spotB)
                        spot += 1
                        second += 1

                    # Build image
                    spotW = 50
                    spotH = 50
                    spotG = 2

                    canvasW = (spotW * 60) + (59 * spotG)
                    canvasH = (spotH * numberOfMinutes) + (numberOfMinutes - 1 * spotG)

                    print(f'Canvas is {str(canvasW)} x {str(canvasH)}')

                    im = Image.new('RGB', (canvasW, canvasH), (255, 255, 255))
                    draw = ImageDraw.Draw(im)

                    x = 0
                    y = 0

                    spot = 1
                    second = 1

                    while spot <= completeNumberOfSpots:

                        if second == 61:

                            x = 0
                            y += spotH + spotG
                            second = 1

                        draw.rectangle((
                            x, y, x + spotW,
                            y + spotH
                        ), fill=(
                            rgbData[spot - 1][0],
                            rgbData[spot - 1][1],
                            rgbData[spot - 1][2]
                        ))

                        x += spotW + spotG
                        spot += 1
                        second += 1

                    second = 1
                    imageName = filename + '.tif'
                    im.save(outputFolder + imageName, 'TIFF')

                    # Build thumbnail
                    imageThumbName = filename + '_thumb.png'

                    im_thumb = im.resize((
                        int(math.ceil(im.size[0] / 100 * 8)),
                        int(math.ceil(im.size[1] / 100 * 8))
                    ), Image.ANTIALIAS)

                    im_thumb.save(outputFolder + imageThumbName, 'PNG')

                    dictionary = {
                        'title': filename,
                        'numberOfSpots': str(completeNumberOfSpots),
                        'contributor': contributor,
                        'rgba': str(rgbData.tolist())
                    }

                    # Save JSON
                    jsonFilePath = f'{outputFolder}{filename}.json'
                    jsonFile = open(jsonFilePath, 'w')
                    json.dump(dictionary, jsonFile, indent=2)
                    jsonFile.close()

                    # Update the processed files list
                    appendToFile(processedLogPath, filename)

                    endTime = time.time() - startTime
                    minutes = str("%.2f" % (endTime / 60))

                    message = f'Completed {filename} in {minutes} minutes.'
                    print(message)
                    appendToFile(logFilePath, message)
                    print('********')

                except FileExistsError:

                    message = f'Error processing file: {filename}'
                    print(message)
                    appendToFile(logFilePath, message)
                    print('********')

            else:

                message = f'{filename}  - cannot be processed.'

                print(message)
                appendToFile(logFilePath, message)
