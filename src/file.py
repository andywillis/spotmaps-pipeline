from os import path, remove


# `removeFile`
#
# If the file exists remove it
def removeFile(filePath):

    if path.isfile(filePath) is True:

        remove(filePath)
