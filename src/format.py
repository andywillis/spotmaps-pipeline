import re

regexes = [

    # S01E01
    # /S[0-9]{2}E[0-9]{2}/,

    # 720p or 1024p
    r'\d{3}[a-z]|\d{4}[a-z]',

    # HDTV
    r'HDTV',

    # x265
    r'x\d{3}',

    # Alternating case letters
    r'^[A-Z]?([a-z][A-Z])*[a-z]?$'

]

def isNotMatch(str):

    result = [str for pattern in regexes if re.search(pattern, str)]

    return all(v is None for v in result)

def rinseFilename(filename):

    split = filename.split('.')
    ext = split.pop()

    result = [str for str in split if isNotMatch(str)]

    rinsedFilename = f'{" ".join(result)}.{ext}'

    return rinsedFilename
