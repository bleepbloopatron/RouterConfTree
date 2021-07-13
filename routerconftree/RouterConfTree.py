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
            currentnode.AppendChild(line)
        elif len(line) - len(line.lstrip(' ')) < currentdepth:
            depthdif = currentdepth - (len(line) - len(line.lstrip(' ')))
            while depthdif > 0:
                currentnode = currentnode.GetParent()
                depthdif -= 1
                currentdepth -=1 
            currentnode.AppendChild(line)

    return baseconf


if __name__=="__main__":
    unittest = NewConfTree('testconfig.txt')
    print(unittest.Print())

