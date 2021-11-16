import routertreeobject
import difflib

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


#  ___  ___            _       ______ _  __  __ 
#  |  \/  |           (_)      |  _  (_)/ _|/ _|
#  | .  . | __ _  __ _ _  ___  | | | |_| |_| |_ 
#  | |\/| |/ _` |/ _` | |/ __| | | | | |  _|  _|
#  | |  | | (_| | (_| | | (__  | |/ /| | | | |  
#  \_|  |_/\__,_|\__, |_|\___| |___/ |_|_| |_|  
#                 __/ |                         
#                |___/                          

def Diff(old: routertreeobject.RouterTreeNode, new: routertreeobject.RouterTreeNode):
    # the idea here is to parse out a small diff between the old and new.  We want to discard any non relevant changes
    # and only get a diff between what the new section has and the specific section in old
    
    # first make a new copy of both old and new to avoid messing up the existing trees.
    # also make sure you filter out empty lines... 
    newnew = NewConfTree(list(filter(('').__ne__, new.Print().split('\n'))))
    oldold = NewConfTree(list(filter(('').__ne__, old.Print().split('\n'))))

    # New blank tree
    output = routertreeobject.RouterTreeNode()

    # Narrow the field to just what's in the new tree
    for newchild in newnew.GetChildren():
        print(f'This is in NewChild: {newchild.GetText()}')
        for oldchild in oldold.ChildrenWith(newchild.GetText()):
            print(f'This is in oldold search: {oldchild.GetText()}')
            output.AppendChild(oldchild)

    delta = difflib.unified_diff(output.Print(), newnew.Print())

    print(''.join(delta))

if __name__=="__main__":
    unittest = NewConfTree('testconfig.txt')
    print(unittest.Print())

    unittest - 'Root thing'
    print(unittest.Print())



    TestRouter = routertreeobject.RouterTreeNode()
    for interface in range(4):
        intobj = routertreeobject.RouterTreeNode('interface ethernet {}'.format(interface + 1))
        intobj.AppendChild(routertreeobject.RouterTreeNode('no switchport'))
        TestRouter.AppendChild(intobj)

    TestRouter.AppendChild(routertreeobject.RouterTreeNode('router bgp 6500'))
    TestRouter.InsertAfter('no switchport', 'shutdown')
    TestRouter.InsertBefore('no switchport', 'description test port' )
    for each in TestRouter.ChildrenWith('description', -1):
        each.Replace('port', 'yeppers')
    #print(TestRouter.ChildrenWith(r'bgp'))
    bgp = TestRouter.ChildrenWith('bgp')[0]
    bgp.AppendChild('router-id 172.16.0.1')
    bgp.AppendChild('neighbor 192.168.0.2 remote-as 65001')
    bgp.AppendChild('address-family ipv4 unicast')
    bgp.AppendChild('address-family ipv6 unicast')
    addrfam = bgp.ChildrenWith('family')[0]
    addrfam.AppendChild('neighbor 192.168.0.2 activate')
    bgp.ChildrenWith('v6')[0].AppendChild('neighbor 192.168.0.3 activate')

    NewTest = routertreeobject.RouterTreeNode()
    interface = NewTest.AppendChild('interface ethernet 2')
    interface.AppendChild('description here we go')
    interface.AppendChild('no shutdown')

    print(NewTest.Print().split('\n'))
    Diff(TestRouter, NewTest)
