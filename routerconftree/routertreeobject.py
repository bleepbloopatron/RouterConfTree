import re

class RouterTreeNode(object):
    def __init__(self, text= None):
        self.children = []
        self.parent = None
        if text == None:
            self.text = 'Root Node'
        else:
            self.text = text
    
    def AppendChild(self, child):
        if isinstance(child, RouterTreeNode):
            newchild = child
        else:
            newchild = RouterTreeNode(child)
        self.children.append(newchild)
        newchild.SetParent(self)

    def RemoveChild(self, child):
        if isinstance(child, RouterTreeNode):
            if child in self.children:
                self.children.remove(child)
                child.RemoveParent()
        elif isinstance(child, str):
            for entry in self.ChildrenWith(child):
                self.children.remove(entry)
                entry.RemoveParent()

    def RemoveParent(self):
        self.parent = None

    def SetParent(self, parent):
        self.parent = parent

    def PrintTree(self, indent = 0, printself = True):
        output = ''
        if printself:
            output += "{}{}\n".format( ' ' * indent, self.text)
        for child in self.children:
            output += child.PrintTree(indent+1)
        return output
    
    def Print(self):
        if self.isRoot():
            # don't print current node, but print all parts. 
            return self.PrintTree(-1, False)
        else:
            return self.PrintTree()

    def SearchSelf(self, searchstring):
        if re.search(searchstring, self.text):
            return True
            print(self.text, searchstring)

    def ChildrenWith(self, searchstring, searchdepth = 0):
        output = []
        for child in self.children:
            if child.SearchSelf(searchstring):
                output.append(child)
            if (searchdepth > 0) or (searchdepth <= -1):
                output += child.ChildrenWith(searchstring, searchdepth-1)
        return output
    
    def LastLine(self):
        if len(self.children) != 0:
            return self.children[-1].LastLine()
        else:
            return self

    def isRoot(self):
        if self.text == "Root Node":
            return True

    def GetAllChildren(self):
        return self.children

    def __add__(self, target):
        if isinstance(target, RouterTreeNode):
            if target.isRoot():
                for child in target.GetAllChildren():
                    self.AppendChild(child)
            else:
                self.AppendChild(target)
        elif isinstance(target, str):
            self.AppendChild(target)

    def __sub__(self, target):
        if isinstance(target, RouterTreeNode):
            if target.isRoot():
                for child in target.GetAllChildren():
                    self.RemoveChild(child)
            else:
                self.RemoveChild(target)
        elif isinstance(target, str):
            self.RemoveChild(target)
        




if __name__=='__main__':
    # build a test routerconfig
    TestRouter = RouterTreeNode()
    for interface in range(4):
        intobj = RouterTreeNode('interface ethernet {}'.format(interface + 1))
        intobj.AppendChild(RouterTreeNode('no switchport'))
        TestRouter.AppendChild(intobj)

    TestRouter.AppendChild(RouterTreeNode('router bgp 6500'))
    #print(TestRouter.ChildrenWith(r'bgp'))
    bgp = TestRouter.ChildrenWith('bgp')[0]
    bgp.AppendChild('router-id 172.16.0.1')
    bgp.AppendChild('neighbor 192.168.0.2 remote-as 65001')
    bgp.AppendChild('address-family ipv4 unicast')
    addrfam = bgp.ChildrenWith('family')[0]
    addrfam.AppendChild('neighbor 192.168.0.2 activate')
    print(TestRouter.Print())

    print(TestRouter.ChildrenWith('activate', -1)[0].text)

    AddTest = RouterTreeNode('New Tree')
    AddTest.AppendChild('With branch')
    TestRouter + AddTest
    print(TestRouter.Print())

    TestRouter - AddTest
    TestRouter - 'interface ethernet 3'

    TestRouter + 'no domain lookup'


    print(TestRouter.Print())



