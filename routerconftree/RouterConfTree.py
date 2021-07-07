import routertreeobject

def openfile(filename):
    with open(filename) as f:
        lines = f.read().splitlines()
    return lines


def NewConfTree(data):
    if isinstance(data, list):
        #use list
        confdata = data

    elif isinstance(data,str):
        confdata = openfile(data)

    baseconf = routertreeobject.RouterTreeNode()
    currentnode = baseconf
    currentdepth = 0
    for line in confdata:
        if len(line) - len(line.lstrip(' ')) > currentdepth:
            nextline = routertreeobject.RouterTreeNode(line)
            currentnode.AppendChild(nextline)
            currentnode = nextline
            currentdepth += 1
        elif len(line) - len(line.lstrip(' ')) == currentdepth:
            