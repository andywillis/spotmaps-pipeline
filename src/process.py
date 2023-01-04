from __future__ import division
from operator import itemgetter

import os, glob, math, sys, time

import cv2 as cv
from PIL import Image, ImageDraw
import numpy as np

from file import removeFile

def processList(config):

    os.system('cls')

    contributor, year, inputFolder, outputFolder = itemgetter(
        'contributor', 'year', 'inputFolder', 'outputFolder'
    )(config)

    logFile = 'spotmaps.log'
    logFilePath = f'{outputFolder}{logFile}'

    removeFile(logFilePath)

    # Get the file list
    newlist = []

    if os.path.isfile('newlist.txt') is False:

        smcf = open('newlist.txt', 'w')
        smcf.write('')

    else:

        smcf = open('newlist.txt', 'r')
        line = smcf.readline()

        while line:

            newlist.append(line.rstrip('\n'))
            line = smcf.readline()

    smcf.close()

    print('Retrieved new file information.')

    # Get the processed file list
    processedlist = []

    if os.path.isfile('processedFiles.txt') is False:

        smcf = open('processedFiles.txt', 'w')
        smcf.write('')

    else:

        smcf = open('processedFiles.txt', 'r')
        line = smcf.readline()

        while line:

            processedlist.append(line.rstrip('\n'))
            line = smcf.readline()

    smcf.close()

    print('Retrieved processed files information.')

    for infile in glob.glob(inputFolder + '*.*'):

        startTime = time.time()

        path_filename = os.path.split(infile)
        filename = path_filename[1].split('.')[0]

        if filename in processedlist:

            print(f'{filename} - already completed.')

        else:

            if filename in newlist:

                capture = cv.CaptureFromFile(infile)
                totalFrames = int(cv.GetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_COUNT))

                if totalFrames == 0:

                    print('filename - unable to read avi.')

                    with open('processedFiles.txt', 'a') as myfile:

                        myfile.write(f'{filename}\n')
                        myfile.close()

                else:

                    try:

                        print('********')
                        fps = int(cv.GetCaptureProperty(capture, cv.CV_CAP_PROP_FPS))

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

                            snapshot = cv.QueryFrame(capture)
                            point = cv.CreateImage((1, 1), cv.IPL_DEPTH_8U, 3)
                            cv.Resize(snapshot, point, cv.CV_INTER_AREA)
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
                        minute = 1
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

                        # Save information
                        jsonName = filename + '.json'
                        mapFile = open(outputFolder + jsonName, 'w')
                        mapFile.write('{')
                        mapFile.write('"title": "' + filename + '",')
                        mapFile.write('"numberOfSpots": ' + str(completeNumberOfSpots) + ',')
                        mapFile.write('"contributor": "' + contributor + '",')
                        mapFile.write('"rgba": "')
                        mapFile.write(str(rgbData.tolist()) + '"')
                        mapFile.write('}')
                        mapFile.close()

                        # Update the processed files list
                        with open('processedFiles.txt', 'a') as myfile:

                            myfile.write(filename + '\n')
                            myfile.close()

                        endTime = time.time() - startTime
                        minutes = str("%.2f" % (endTime / 60))
                        msg1 = 'Completed in ' + minutes + ' minutes.'

                        print(msg1)

                        with open(logFilePath, 'a') as myfile:

                            myfile.write(filename + ': ' + msg1 + '\n')
                            myfile.close()

                        print('********')

                    except RuntimeError as runtime_error:

                        msg2 = 'Error processing file'
                        print(msg2)

                        with open(logFilePath, 'a') as myfile:

                            myfile.write(msg2 + ': ' + filename + '\n')
                            myfile.close()

                        print('********')

            else:

                msg3 = filename + ' - cannot be processed.'

                print(msg3)

                with open(logFilePath, 'a') as myfile:

                    myfile.write(msg3 + '\n')
                    myfile.close()
