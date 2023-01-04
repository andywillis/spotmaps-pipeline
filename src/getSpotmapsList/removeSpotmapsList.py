import os

def removeSpotmapList(spotmapsListFilePath):

    if os.path.isfile(spotmapsListFilePath) is True:

        os.remove(spotmapsListFilePath)
