import re
import copy

class RouterTreeNode(object):
    def __init__(self, text= None):
        self.children = []
        self.parent = None
        if text == None:
            self.text = ''
            self.root = True
        else:
            self.text = text.lstrip()
            self.root = False
    #   _   _                      _                   _             
    #  | | | |                    | |                 (_)            
    #  | |_| | ___  _   _ ___  ___| | _____  ___ _ __  _ _ __   __ _ 
    #  |  _  |/ _ \| | | / __|/ _ \ |/ / _ \/ _ \ '_ \| | '_ \ / _` |
    #  | | | | (_) | |_| \__ \  __/   <  __/  __/ |_) | | | | | (_| |
    #  \_| |_/\___/ \__,_|___/\___|_|\_\___|\___| .__/|_|_| |_|\__, |
    #                                           | |             __/ |
    #                                           |_|            |___/ 


    def AppendChild(self, child):
        # Adds child
        if isinstance(child, RouterTreeNode):
            newchild = child
        else:
            newchild = RouterTreeNode(child)
        self.children.append(newchild)
        newchild.SetParent(self)
        return newchild

    def RemoveChild(self, child):
        # Removes child
        if isinstance(child, RouterTreeNode):
            if child in self.children:
                self.children.remove(child)
                child.RemoveParent()
        elif isinstance(child, str):
            for entry in self.ChildrenWith(child):
                self.children.remove(entry)
                entry.RemoveParent()

    def GetParent(self):
        # Returns Parent, if no Parent returns self.
        if self.parent:
            return self.parent
        else:
            return self

    def RemoveParent(self):
        # Remove Parent
        self.parent = None

    def SetParent(self, parent):
        # Set Parent
        self.parent = parent

    def InserttoParent(self, position, adoptchild):
        # Inserts to parent used by other functions
        if isinstance(adoptchild, RouterTreeNode):
            newchild = copy.deepcopy(adoptchild)
        else:
            newchild = RouterTreeNode(adoptchild)
        # I know this is silly.  Please fix and submit a PR
        self.parent.children.insert( self.parent.children.index(self) + position, newchild ) 
        newchild.SetParent(self.parent)

    def Insert(self, searchstring, position, child ):
        # Wraps InserttoParent
        parents = self.ChildrenWith(searchstring, -1)
        for parent in parents:
            parent.InserttoParent( position, child)

    def InsertAfter(self, searchstring, child):
        # Wraps Insert with position set for after.
        self.Insert(searchstring, 1, child)

    def InsertBefore(self, searchstring, child):
        # Wraps Insert with position set for before.
        self.Insert(searchstring, 0, child)

    def Replace(self, searchstring, replacestring):
        # allows regex substitution. 
        self.text = re.sub(searchstring, replacestring, self.text)

    def ReplaceAll(self, searchstring, replacestring):
        # use search to replace all instances in the tree via Replace. 
        for each in self.ChildrenWith(searchstring, -1):
            each.Replace(searchstring, replacestring)

    def SafeDeleteSelf(self):
        # Only remove self if there are no children. 
        if len(self.children) == 0:
            self.parent.RemoveChild(self)

    def HasChild(self, child):
        if child in self.children:
            return True
        else:
            return False

    def LastLine(self):
        if len(self.children) != 0:
            return self.children[-1].LastLine()
        else:
            return self

    def isRoot(self):
        if self.root or (self.parent == None):
            return True
        else:
            return False

    def isEmptyRoot(self):
        if (self.root or (self.parent == None)) and (self.text == ''):
            return True
        else:
            return False

    def GetAllChildren(self):
        return self.children

    def BuildHaritage(self):
        if self.isRoot() and self.isEmptyRoot():
            output = []
        elif self.isRoot() and not self.isEmptyRoot():
            output = [self.text]
        else:
            output = self.parent.BuildHaritage()
            output.append(self.text)
        return output

    def BuildLiniage(self):
        output = []
        for child in self.children:
            output += child.BuildLiniage()
        output += [self.BuildHaritage()]
        return output

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
            if self.HasChild(target):
                self.RemoveChild(target)
            else:
                targetliniage = target.BuildLiniage()
                for successor in targetliniage:
                    for result in self.SearchDaisyChain(*successor):
                        result.SafeDeleteSelf()
        elif isinstance(target, str):
            self.RemoveChild(target)

    #   _____       _               _    ______                _   _                 
    #  |  _  |     | |             | |   |  ___|              | | (_)                
    #  | | | |_   _| |_ _ __  _   _| |_  | |_ _   _ _ __   ___| |_ _  ___  _ __  ___ 
    #  | | | | | | | __| '_ \| | | | __| |  _| | | | '_ \ / __| __| |/ _ \| '_ \/ __|
    #  \ \_/ / |_| | |_| |_) | |_| | |_  | | | |_| | | | | (__| |_| | (_) | | | \__ \
    #   \___/ \__,_|\__| .__/ \__,_|\__| \_|  \__,_|_| |_|\___|\__|_|\___/|_| |_|___/
    #                  | |                                                           
    #                  |_|                                                          

    def PrintTree(self, indent = 0, printself = True):
        output = ''
        if printself:
            output += "{}{}\n".format( ' ' * indent, self.text)
        for child in self.children:
            output += child.PrintTree(indent+1)
        return output
    
    def Print(self):
        if self.isEmptyRoot():
            # don't print current node, but print all parts. 
            return self.PrintTree(-1, False)
        else:
            return self.PrintTree()


    #  ______                      _ _   _       _____                     _     _             
    #  |  ___|                    (_) | | |     /  ___|                   | |   (_)            
    #  | |_ _   _ _ __   __      ___| |_| |__   \ `--.  ___  __ _ _ __ ___| |__  _ _ __   __ _ 
    #  |  _| | | | '_ \  \ \ /\ / / | __| '_ \   `--. \/ _ \/ _` | '__/ __| '_ \| | '_ \ / _` |
    #  | | | |_| | | | |  \ V  V /| | |_| | | | /\__/ /  __/ (_| | | | (__| | | | | | | | (_| |
    #  \_|  \__,_|_| |_|   \_/\_/ |_|\__|_| |_| \____/ \___|\__,_|_|  \___|_| |_|_|_| |_|\__, |
    #                                                                                     __/ |
    #                                                                                    |___/ 

    def SearchSelf(self, searchstring):
        # Basic do I have text function
        if re.search(searchstring, self.text):
            return True
        else:
            return False
        
    def ChildrenWith(self, searchstring, searchdepth = 0):
        # returns a list of children that contain a search string, and will search further down the tree.
        # Used by other functions
        output = []
        for child in self.children:
            if child.SearchSelf(searchstring):
                output.append(child)
            if (searchdepth > 0) or (searchdepth <= -1):
                output += child.ChildrenWith(searchstring, searchdepth-1)
        return output

    def SearchDaisyChain(self, *searchstrings, **kwargs):
        # Search depth sets the inital find depth.  After that all matches must be direct children of the first match. 
        # returns a list of only objects that match all search strings. 
        output = []
        searchstrings = list(searchstrings)
        if 'searchdepth' in kwargs:
            searchdepth = kwargs['searchdepth']
        else:
            searchdepth = 0
        currentstring = searchstrings.pop(0)
        for child in self.ChildrenWith(currentstring, searchdepth):
            if len(searchstrings) > 0:
                output += child.SearchDaisyChain(*searchstrings)
            else:
                output.append(child)
        return output

    def SearchChildrenWith(self, *searchstrings, **kwargs):
        # Returns a list of objects that start with the first search string, and contain all the sub strings
        output = []
        search = self.SearchDaisyChain(*searchstrings, **kwargs)
        for child in search:
            for each in range(len(searchstrings) -1):
                child = child.GetParent()
            output.append(child)
        return output
    


        

if __name__=='__main__':
    # build a test routerconfig
    TestRouter = RouterTreeNode()
    for interface in range(4):
        intobj = RouterTreeNode('interface ethernet {}'.format(interface + 1))
        intobj.AppendChild(RouterTreeNode('no switchport'))
        TestRouter.AppendChild(intobj)

    TestRouter.AppendChild(RouterTreeNode('router bgp 6500'))
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


    for line in TestRouter.SearchDaisyChain('router bgp 6500', r'ipv', r'192.168.0.[1-3]'):
        print(line)
        print(TestRouter.SearchDaisyChain(*line.BuildHaritage()))

    TestRouter.ReplaceAll('yeppers', 'interface config')

    print(TestRouter.ChildrenWith('router-id'))
    print(TestRouter.ChildrenWith('router-id', -1))
    print(TestRouter.ChildrenWith('ipv6', -1)[0].BuildLiniage())

    TestSub = RouterTreeNode('router bgp 6500')
    TestSub.AppendChild('address-family ipv6 unicast')
    TestSub.ChildrenWith('ipv6', -1)[0].AppendChild('neighbor 192.168.0.3 activate')

    TestRouter - TestSub

    print(TestSub.Print())

    print(TestRouter.Print())

    for each in TestRouter.SearchChildrenWith('bgp', 'ipv4', 'activate'):
        print(each.Print())