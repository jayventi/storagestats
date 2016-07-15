## python 2.7
"""
treeTable: A dict-derived TREE data structure in Python
Created on Jun 21, 2016
@author: jayventi
"""

#import datetime
from json import dumps, loads


class TreeTableNode(object):
    """
    Tree node object contains all need data to mantane a tree
    """
    def __init__(self, nodeid, name, parentid=None, content=None, children=None):  # TODO set all
        if children is None:
            children = []
        if content is None:
            content = {}
        self.nodeid = nodeid
        self.name = name
        self.content = content
        self.children = children
        self.parentid = parentid
        #self.updated = datetime.datetime # is not JSON serializable
        #self.created = datetime.datetime # is not JSON serializable

    def __repr__(self):
        return '{} : {}'.format(self.name, str(self.nodeid))

    def addChildId(self, childId):
        temp = self.children
        temp.append(childId)
        self.children = temp

    def fullRepr(self):
        lStr = ' chindren: ['
        if self.children:
            comm = ''
            for child in self.children:
                lStr += comm + str(child)
                comm = ','
        lStr += ']'
        retStr = ' '
        if self.content:
            for k in sorted(self.content):
                retStr += '\t' + k + ':\t' + str(self.content[k]) + '\n'
        return self.name + "\t parent:" + str(self.parentid) + lStr + "\t" + retStr

    def update(self, newContent):
        for keys in newContent:
            self.content[keys] = newContent[keys]



class TreeTable(object):
    """
    Main tree structure stores node in a dict as values and nodeId as keys
    self.name is used as a index vaule self._nameToNodeid is the index hash
    """
    def __init__(self, name='defaultTree', treeid=1, parentTreeid=None):
        self.treeid = treeid
        self.name = name
        self.parentTreeid = parentTreeid
        self.lastNodeid = 0
        self._NodeTable = {}
        self._nameToNodeid = {}
        self.addChild('root', 1)

    def addChild(self, name, parentid, content=None):
        """ Adds a child node, main mechanism of building a tree"""
        nextNodeid = self.lastNodeid + 1
        newNode = TreeTableNode(nextNodeid, name, parentid, content, [])
        self._NodeTable[nextNodeid] = newNode
        self.lastNodeid = nextNodeid
        # add child to parent node's chaiedren list
        parentNode = self._NodeTable[parentid]
        if nextNodeid != parentid:  # not root node
            parentNode.addChildId(nextNodeid)
            self._NodeTable[parentid] = parentNode
        self._nameToNodeid[name] = nextNodeid

    def setRootName(self, name, content={}):
        """
        Tets the roots name and content
        when a TreeTable is created one root node is generated
        and name set to 'root'. having a root node with name
        root means that it has never been initialized to any
        meaningful content and is the definition of a created but
        uninitialized tree. This special routine is used to
        set the root node to some specific name.
        This is the only function which changes the name
        of a node after it has been created.
        """
        rootNodeId = 1
        rootNode = self._NodeTable[rootNodeId]
        rootNode.name = name
        rootNode.content = content
        self._NodeTable[rootNodeId] = rootNode
        self._nameToNodeid[name] = rootNodeId
        self._nameToNodeid.pop("root", None)

    def addChildren(self,  parentid, children={}):
        """ adds a list of nodeIds of children nodes to a node"""
        for child in children:
            self.addChild(child.name, parentid, child.content)

    def tableDump(self):
        print self._NodeTable

    def tableFullDump(self):
        for eachN in self._NodeTable:
            text = 'nodeId: {} {} \n'.format(str(eachN), self._NodeTable[eachN].fullRepr())
        return text

    def getChildren(self, nodeId):
        tempNode = self._NodeTable[nodeId]
        return tempNode.children

    def getNodeByName(self, name):
        try:
            nodeId = self._nameToNodeid[name]
            return self._NodeTable[nodeId]
        except:
            nodeId = None
            return None

    def getNodeById(self, nodeid):
        return self._NodeTable[nodeid]

    def getNodeIdByName(self, name):
        return self._nameToNodeid[name]

    def isNodeByName(self, name):
        if name in self._nameToNodeid:
            return True
        else:
            return False

    def isRootSet(self):
        if 'root' in self._nameToNodeid:
            return False
        else:
            return True

    def upDateNode(self, nodeId, updateContent):
        """" Updates notes content by nodeId"""
        tempNode = self._NodeTable[nodeId]
        tempNode.update(updateContent)
        self._NodeTable[nodeId] = tempNode

    def upDateNodeByName(self, name, updateContent):
        """" Updates notes content by nodes name"""
        nodeId = self._nameToNodeid[name]
        tempNode = self._NodeTable[nodeId]
        tempNode.update(updateContent)
        self._NodeTable[nodeId] = tempNode

    def nodeCount(self):
        return len(self._NodeTable)

    def prettyTreeTable(self):
        """"
        An implementation of printing tree using Stack Print
        tree structure in hierarchy style.
        For example:
            Root
            |___ 1
            |     |___ 2
            |          |___ 4
            |          |___ 5
            |___ 3
            |___ 6
            |     |___ 7
        Uses Stack structure, push and pop nodes with additional level info.
        """
        print ('Start prettyTreeTable')
        level = str(0)
        nodeId = 1
        StackONodes = [nodeId, level]   # init StackONodes
        nodesToUpdate = {level: nodeId}  # for walk prossess
        while StackONodes:
            # headid pointer points to the first item of stack, can be a level identifier or tree nodeid
            headid = StackONodes.pop()
            if isinstance(headid, str):
                level = headid  # move towards the root up a level
            else:
                headNode = self._NodeTable[headid]  # move tword the leaf dowen a level
                self.__printLabel__(headNode, StackONodes, level, self.__basicLable__)
                children = headNode.children
                children.reverse()
                if StackONodes:
                    # push level info seens a headid was just pop from StackONodes, the level at now
                    StackONodes.append(level)
                    nodesToUpdate[level] = headid

                if children:  # add children if has children nodes
                    StackONodes.extend(children)
                    level = str(1 + int(level))
                    StackONodes.append(level)

    def __printLabel__(self, headNode, StackONodes, levelStr, labelFun):
        """
        Print a each node as a line with branch marks
        """
        leading = ' '
        lasting = '|___ '
        label = labelFun(headNode)
        level = int(levelStr)
        #print levelStr
        #print StackONodes
        if level == 0:
            print leading + label
        else:
            for l in range(0, level - 1):
                sibling = False
                parentid = self.__getParentid__(headNode.nodeid, level - l)
                parentN = self._NodeTable[parentid]
                for c in parentN.children:
                    if c in StackONodes:
                        sibling = True
                        break
                if sibling:
                    leading += '|     '
                else:
                    leading += '     '

            if label.strip() != '-':
                print('{0}{1}{2}'.format(leading, lasting, label))

    def __basicLable__(self, headNode):
        return str(headNode.nodeid)+' - ' + str(headNode.name)

    def __getParentid__(self, headid, levelUp):
        while levelUp:
            parentnode = self._NodeTable[headid]
            headid = parentnode.parentid
            levelUp -= 1
        return headid

    def get_tree_stuff(self, headid=1):
        """stuff summer"""
        summedStuff = 1  # get stuff noraly 0 for inner
        innerNode = self._NodeTable[headid]
        for childNodeid in innerNode.children:  # hase children
            childNode = self._NodeTable[childNodeid]
            if childNode.children:  # if childNode has children follow
                summedStuff += self.get_tree_stuff(childNodeid)
            else:
                stuff = 1  # get stuff
                summedStuff += stuff
                # childNode.content =  Stuff
                print('leaf node: ' + str(childNode)+" stuff: "+str(stuff))
        # innerNode.content =  summedStuff
        print('inner node: ' + str(headid)+" stuff: "+str(summedStuff))
        return summedStuff

    def to_json(self):
        """ Sterilizes to json contents of the TreeTable"""
        to_jsonDict = {}
        for nodeId in self._NodeTable:
            to_jsonDict[nodeId] = self._NodeTable[nodeId].__dict__
        return dumps(to_jsonDict)

    def from_json(self, fromJson):
        """ Reconstitutes a tree object from a sterilized json of the same type"""
        fromDict = loads(fromJson)
        if len(fromDict) < 1:
            return 0
        for jsonNodeId, jsonNode in fromDict.iteritems():
            working_node = TreeTableNode(jsonNode['nodeid'], jsonNode['name'],
                                         jsonNode['parentid'], jsonNode['content'],
                                         jsonNode['children']
                                         )
            self._NodeTable[int(jsonNodeId)] = working_node
        return self.nodeCount()
