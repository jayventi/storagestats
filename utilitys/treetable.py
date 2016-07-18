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
    def __init__(self, node_id, name, parentid=None, content=None, children=None):  # TODO set all
        if children is None:
            children = []
        if content is None:
            content = {}
        self.node_id = node_id
        self.name = name
        self.content = content
        self.children = children
        self.parentid = parentid
        #self.updated = datetime.datetime # is not JSON serializable
        #self.created = datetime.datetime # is not JSON serializable

    def __repr__(self):
        return '{} : {}'.format(self.name, str(self.node_id))

    def add_child_id(self, childId):
        temp = self.children
        temp.append(childId)
        self.children = temp

    def full_repr(self):
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
    Main tree structure stores node in a dict as values and node_id as keys
    self.name is used as a index vaule self._name_to_node_id is the index hash
    """
    def __init__(self, name='defaultTree', treeid=1, parentTreeid=None):
        self.treeid = treeid
        self.name = name
        self.lastnode_id = 0
        self._node_table = {}
        self._name_to_node_id = {}
        self.add_child('root', 1)

    def add_child(self, name, parentid, content=None):
        """ Adds a child node, main mechanism of building a tree"""
        nextnode_id = self.lastnode_id + 1
        newNode = TreeTableNode(nextnode_id, name, parentid, content, [])
        self._node_table[nextnode_id] = newNode
        self.lastnode_id = nextnode_id
        # add child to parent node's chaiedren list
        parentNode = self._node_table[parentid]
        if nextnode_id != parentid:  # not root node
            parentNode.add_child_id(nextnode_id)
            self._node_table[parentid] = parentNode
        self._name_to_node_id[name] = nextnode_id

    def set_root_name(self, name, content={}):
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
        rootnode_id = 1
        rootNode = self._node_table[rootnode_id]
        rootNode.name = name
        rootNode.content = content
        self._node_table[rootnode_id] = rootNode
        self._name_to_node_id[name] = rootnode_id
        self._name_to_node_id.pop("root", None)

    def add_children(self,  parentid, children={}):
        """ adds a list of node_ids of children nodes to a node"""
        for child in children:
            self.add_child(child.name, parentid, child.content)

    def table_dump(self):
        print self._node_table

    def table_full_dump(self):
        for eachN in self._node_table:
            text = 'node_id: {} {} \n'.format(str(eachN), self._node_table[eachN].full_repr())
        return text

    def get_children(self, node_id):
        tempNode = self._node_table[node_id]
        return tempNode.children

    def get_node_by_name(self, name):
        try:
            node_id = self._name_to_node_id[name]
            return self._node_table[node_id]
        except:
            node_id = None
            return None

    def get_node_by_id(self, node_id):
        return self._node_table[node_id]

    def getnode_idByName(self, name):
        return self._name_to_node_id[name]

    def is_node_by_name(self, name):
        if name in self._name_to_node_id:
            return True
        else:
            return False

    def is_root_set(self):
        if 'root' in self._name_to_node_id:
            return False
        else:
            return True

    def up_date_node(self, node_id, updateContent):
        """" Updates notes content by node_id"""
        tempNode = self._node_table[node_id]
        tempNode.update(updateContent)
        self._node_table[node_id] = tempNode

    def up_date_node_by_name(self, name, updateContent):
        """" Updates notes content by nodes name"""
        node_id = self._name_to_node_id[name]
        tempNode = self._node_table[node_id]
        tempNode.update(updateContent)
        self._node_table[node_id] = tempNode

    def node_count(self):
        return len(self._node_table)

    def pretty_tree_table(self):
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
        print ('Start pretty_tree_table')
        level = str(0)
        node_id = 1
        StackONodes = [node_id, level]   # init StackONodes
        nodesToUpdate = {level: node_id}  # for walk prossess
        while StackONodes:
            # headid pointer points to the first item of stack, can be a level identifier or tree node_id
            headid = StackONodes.pop()
            if isinstance(headid, str):
                level = headid  # move towards the root up a level
            else:
                headNode = self._node_table[headid]  # move tword the leaf dowen a level
                self.__print_label__(headNode, StackONodes, level, self.__basic_lable__)
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

    def __print_label__(self, headNode, StackONodes, levelStr, labelFun):
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
                parentid = self.__get_parentid__(headNode.node_id, level - l)
                parentN = self._node_table[parentid]
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

    def __basic_lable__(self, headNode):
        return str(headNode.node_id)+' - ' + str(headNode.name)

    def __get_parentid__(self, headid, levelUp):
        while levelUp:
            parentnode = self._node_table[headid]
            headid = parentnode.parentid
            levelUp -= 1
        return headid

    def get_tree_stuff(self, headid=1):
        """stuff summer"""
        summedStuff = 1  # get stuff noraly 0 for inner
        innerNode = self._node_table[headid]
        for childnode_id in innerNode.children:  # hase children
            childNode = self._node_table[childnode_id]
            if childNode.children:  # if childNode has children follow
                summedStuff += self.get_tree_stuff(childnode_id)
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
        for node_id in self._node_table:
            to_jsonDict[node_id] = self._node_table[node_id].__dict__
        return dumps(to_jsonDict)

    def from_json(self, fromJson):
        """ Reconstitutes a tree object from a sterilized json of the same type"""
        fromDict = loads(fromJson)
        if len(fromDict) < 1:
            return 0
        for jsonnode_id, jsonNode in fromDict.iteritems():
            working_node = TreeTableNode(jsonNode['node_id'], jsonNode['name'],
                                         jsonNode['parentid'], jsonNode['content'],
                                         jsonNode['children']
                                         )
            self._node_table[int(jsonnode_id)] = working_node
        return self.node_count()
