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

    baseconf = routertreeobject.RouterTreeNode('BaseLayer')
    currentnode = baseconf
    currentdepth = 0
    for line in confdata:
        if len(line) - len(line.lstrip(' ')) > currentdepth:
            currentnode.AppendChild(line)
            currentnode = currentnode.