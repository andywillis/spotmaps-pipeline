import os

def removeSpotmapsList(spotmapsListFilePath):

    if os.path.isfile(spotmapsListFilePath) is True:

        os.remove(spotmapsListFilePath)
