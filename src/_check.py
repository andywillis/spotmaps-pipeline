# import cv2
import pytesseract

import os

from pathlib import Path

# Remove any file without one of these extensions
# ^.*\.(?!jpg$|gif|jpe|jpeg$)[^.]+$

os.environ['OMP_THREAD_LIMIT'] = '1'

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

# Set input path
inputPath = 'vef\\'
filteredPath = 'filtered\\'

log = '_log.txt'

if (os.path.isfile(log)):
    os.remove(log)

with open(log, 'a+') as logFile:

    imgNo = 1

    # Recurse over all jpg files
    for path in Path(inputPath).rglob('*.jpg'):

        # Get its file path, and name
        filepath, filename = os.path.split(path)
        subfilePath = filepath.split('\\')[1]
        file = path.as_posix()

        print('####')
        print(f'# Image: {imgNo}')
        print(f'# Path: {subfilePath}\\{filename}')

        # img = cv2.imread(file)
        try:

            text = pytesseract.image_to_string(file, timeout=30)

        except RuntimeError as timeout_error:

            print(f'# Error: {timeout_error}')
            logFile.write(f'RuntimeError: {subfilePath}\\{filename}\n')

        except UnicodeDecodeError as unicode_error:

            print(f'# Error: {unicode_error}')
            logFile.write('UnicodeDecodeError: {subfilePath}\\{filename}\n')

        else:

            arrLen = len(text.split(' '))

            if arrLen == 1:

                print(f'# Contains {arrLen} word')

            else:

                print(f'# Contains {arrLen} words')

            if arrLen > 100:

                print('# Moving file')

                outputFilePath = f'{filteredPath}{subfilePath}\\'

                if not os.path.exists(f'{outputFilePath}'):

                    os.makedirs(f'{outputFilePath}')

                try:

                    os.rename(file, f'{outputFilePath}{filename}')

                except FileExistsError as fileexists_error:

                    print(f'# Error: {fileexists_error}')
                    logFile.write(f'FileExistsError {subfilePath}\\{filename}\n')

        print('####')
        print('')

        imgNo += 1

logFile.close()
