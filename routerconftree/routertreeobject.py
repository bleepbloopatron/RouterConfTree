import re

class RouterTreeNode(object):
    def __init__(self, text):
        self.children = []
        self.parent = None
        self.text = text
    
    def AppendChild(self, child):
        if isinstance(child, RouterTreeNode):
            newchild = child
        else:
            newchild = RouterTreeNode(child)
        self.children.append(newchild)
        newchild.SetParent(self)

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
        # don't print current node, but print all parts. 
        return self.PrintTree(-1, False)

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


if __name__=='__main__':
    # build a test routerconfig
    TestRouter = RouterTreeNode('Root Node')
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


