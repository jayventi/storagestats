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
    def __init__(self, node_id, name, parent_id=None, content=None, children=None):  # TODO set all
        if children is None:
            children = []
        if content is None:
            content = {}
        self.node_id = node_id
        self.name = name
        self.content = content
        self.children = children
        self.parent_id = parent_id
        #self.updated = datetime.datetime # is not JSON serializable
        #self.created = datetime.datetime # is not JSON serializable

    def __repr__(self):
        return '{} : {}'.format(self.name, str(self.node_id))

    def add_child_id(self, child_id):
        temp = self.children
        temp.append(child_id)
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
        return self.name + "\t parent:" + str(self.parent_id) + lStr + "\t" + retStr

    def update(self, new_content):
        for keys in new_content:
            self.content[keys] = new_content[keys]



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

    def add_child(self, name, parent_id, content=None):
        """ Adds a child node, main mechanism of building a tree"""
        nextnode_id = self.lastnode_id + 1
        new_node = TreeTableNode(nextnode_id, name, parent_id, content, [])
        self._node_table[nextnode_id] = new_node
        self.lastnode_id = nextnode_id
        # add child to parent node's chaiedren list
        parentNode = self._node_table[parent_id]
        if nextnode_id != parent_id:  # not root node
            parentNode.add_child_id(nextnode_id)
            self._node_table[parent_id] = parentNode
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
        root_node_id = 1
        root_node = self._node_table[root_node_id]
        root_node.name = name
        root_node.content = content
        self._node_table[root_node_id] = root_node
        self._name_to_node_id[name] = root_node_id
        self._name_to_node_id.pop("root", None)

    def add_children(self,  parent_id, children={}):
        """ adds a list of node_ids of children nodes to a node"""
        for child in children:
            self.add_child(child.name, parent_id, child.content)

    def table_dump(self):
        print(self._node_table)

    def table_full_dump(self):
        for each_nd in self._node_table:
            text = 'node_id: {} {} \n'.format(str(each_nd), self._node_table[each_nd].full_repr())
        return text

    def get_children(self, node_id):
        temp_node = self._node_table[node_id]
        return temp_node.children

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

    def up_date_node(self, node_id, update_content):
        """" Updates notes content by node_id"""
        tempNode = self._node_table[node_id]
        tempNode.update(update_content)
        self._node_table[node_id] = tempNode

    def up_date_node_by_name(self, name, update_content):
        """" Updates notes content by nodes name"""
        node_id = self._name_to_node_id[name]
        tempNode = self._node_table[node_id]
        tempNode.update(update_content)
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
        stack_of_nodes = [node_id, level]   # init stack_of_nodes
        nodes_to_dpdate = {level: node_id}  # for walk prossess
        while stack_of_nodes:
            # head_id pointer points to the first item of stack, can be a level identifier or tree node_id
            head_id = stack_of_nodes.pop()
            if isinstance(head_id, str):
                level = head_id  # move towards the root up a level
            else:
                head_node = self._node_table[head_id]  # move tword the leaf dowen a level
                self.__print_label__(head_node, stack_of_nodes, level, self.__basic_lable__)
                children = head_node.children
                children.reverse()
                if stack_of_nodes:
                    # push level info seens a head_id was just pop from stack_of_nodes, the level at now
                    stack_of_nodes.append(level)
                    nodes_to_dpdate[level] = head_id

                if children:  # add children if has children nodes
                    stack_of_nodes.extend(children)
                    level = str(1 + int(level))
                    stack_of_nodes.append(level)

    def __print_label__(self, head_node, stack_of_nodes, level_str, label_fun):
        """
        Print a each node as a line with branch marks
        """
        leading = ' '
        lasting = '|___ '
        label = label_fun(head_node)
        level = int(level_str)
        if level == 0:
            print (leading + label)
        else:
            for l in range(0, level - 1):
                sibling = False
                parent_id = self.__get_parent_id__(head_node.node_id, level - l)
                parentN = self._node_table[parent_id]
                for c in parentN.children:
                    if c in stack_of_nodes:
                        sibling = True
                        break
                if sibling:
                    leading += '|     '
                else:
                    leading += '     '

            if label.strip() != '-':
                print('{0}{1}{2}'.format(leading, lasting, label))

    def __basic_lable__(self, head_node):
        return str(head_node.node_id)+' - ' + str(head_node.name)

    def __get_parent_id__(self, head_id, level_up):
        while level_up:
            parentnode = self._node_table[head_id]
            head_id = parentnode.parent_id
            level_up -= 1
        return head_id

    def get_tree_stuff(self, head_id=1):
        """stuff summer"""
        summed_stuff = 1  # get stuff noraly 0 for inner
        innerNode = self._node_table[head_id]
        for childnode_id in innerNode.children:  # hase children
            childNode = self._node_table[childnode_id]
            if childNode.children:  # if childNode has children follow
                summed_stuff += self.get_tree_stuff(childnode_id)
            else:
                stuff = 1  # get stuff
                summed_stuff += stuff
                # childNode.content =  Stuff
                print('leaf node: ' + str(childNode)+" stuff: "+str(stuff))
        # innerNode.content =  summed_stuff
        print('inner node: ' + str(head_id)+" stuff: "+str(summed_stuff))
        return summed_stuff

    def to_json(self):
        """ Sterilizes to json contents of the TreeTable"""
        to_json_dict = {}
        for node_id in self._node_table:
            to_json_dict[node_id] = self._node_table[node_id].__dict__
        return dumps(to_json_dict)

    def from_json(self, from_json):
        """ Reconstitutes a tree object from a sterilized json of the same type"""
        from_dict = loads(from_json)
        if len(from_dict) < 1:
            return 0
        for jsonnode_id, json_node in from_dict.items():
            working_node = TreeTableNode(json_node['node_id'], json_node['name'],
                                         json_node['parent_id'], json_node['content'],
                                         json_node['children']
                                         )
            self._node_table[int(jsonnode_id)] = working_node
        return self.node_count()
