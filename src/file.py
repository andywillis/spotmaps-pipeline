import os, re


# `removeFile`
#
# If the file exists remove it
def removeFile(filePath):

    if os.path.isfile(filePath) is True:

        os.remove(filePath)


# `getListFromFileContents`
#
# Create an empty file if it doesn't exist, and return
# an empty array, or read the lines of the file if it does
# exist, and return a filled array
def getListFromFileContents(filePath):

    list = []

    if os.path.isfile(filePath) is False:

        createFile(filePath)

    else:

        file = open(filePath, 'r')
        line = file.readline()

        while line:

            list.append(line.rstrip('\n'))
            line = file.readline()

        file.close()

    return list


# `createFile`
#
# Create a new file
def createFile(filePath):

    with open(filePath, 'w+') as myfile:
        myfile.close()


# `appendToFile`
#
# Append some information to a file
def appendToFile(filePath, data):

    with open(filePath, 'a+') as myfile:
        myfile.write(f'{data}\n')
        myfile.close()

