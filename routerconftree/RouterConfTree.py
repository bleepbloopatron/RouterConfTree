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
    ConfLineList = list()

    for line in range(len(confdata)):
        nextline = routertreeobject.RouterTreeNode(confdata[line])
        # Depth is set to number of spaces prepending the line. 
        depth = len(confdata[line]) - len(confdata[line].lstrip(' '))
        # builds a list of RouterTreeNodes to search back through for liniage. 
        ConfLineList.append((nextline, depth))
        searchparents = True
        # Starts the backwards search at the last line.
        index = -1
        while searchparents:
            # Checks last line for liniage depth. 
            if (line + index) > -1:
                # Keep checking up stream for liniage.
                if ConfLineList[line + index][1] > depth:
                    index -=1
                # Find next closest sibling, and connect to it's parent.
                elif ConfLineList[line + index][1] == depth:
                    ConfLineList[line + index][0].GetParent().AppendChild(nextline)
                    searchparents = False
                # Find parent and connect to that. 
                elif ConfLineList[line + index][1] < depth:
                    ConfLineList[line + index][0].AppendChild(nextline)
                    searchparents = False
            # Fall back for first line
            else:
                baseconf.AppendChild(nextline)
                searchparents = False


    return baseconf


if __name__=="__main__":
    unittest = NewConfTree('testconfig.txt')
    print(unittest.Print())

    unittest - 'Root thing'
    print(unittest.Print())

