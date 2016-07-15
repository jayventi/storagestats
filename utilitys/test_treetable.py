# test_treetable

import unittest

from treetable import TreeTable

#  Basic creation and detection
class TestTreeTableBaicCre(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_init_1_tableFullDump_TreeTable_init(self):
        # setup
        new_dir_info_tree = TreeTable()
        #test
        actual = new_dir_info_tree.tableFullDump()
        expected = 'nodeId: 1 root\t parent:1 chindren: []\t  \n'
        self.assertEqual(actual, expected)

    def test_init_2_addChild_Dump_to_json(self):
        # setup
        new_dir_info_tree = TreeTable()
        new_dir_info_tree.addChild('type 1', 1, {'stuff': 'info'})
        new_dir_info_tree.addChild('type 2', 1, {'stuff': 'info'})
        #test
        actual = new_dir_info_tree.to_json()
        expected = '{"1": {"content": {}, "parentid": 1, "children": [2, 3], "nodeid": 1, "name": "root"}, "2": {"content": {"stuff": "info"}, "parentid": 1, "children": [], "nodeid": 2, "name": "type 1"}, "3": {"content": {"stuff": "info"}, "parentid": 1, "children": [], "nodeid": 3, "name": "type 2"}}'
        self.assertEqual(actual, expected)

    def test_init_3_from_json(self):
        #setup
        new_dir_info_tree = TreeTable()
        new_dir_info_tree.addChild('type 1', 1, {'stuff': 'info'})
        new_dir_info_tree.addChild('type 2', 1, {'stuff': 'info'})
        json_str = new_dir_info_tree.to_json()
        # test
        newer_dir_info_tree = TreeTable()
        newer_dir_info_tree.from_json(json_str)
        actual = newer_dir_info_tree.to_json()
        expected = json_str
        self.assertEqual(actual, expected)

# Basic crud and index lookups
class TestTreeTable_crudTests(unittest.TestCase):
    def setUp(self):
        self.new_dir_info_tree = TreeTable()
        self.new_dir_info_tree.addChild('type 1', 1, {'stuff': 'info'})
        self.new_dir_info_tree.addChild('type 2', 1, {'stuff': 'info'})

    def tearDown(self):
        pass

    def test_crud_01_getChildren(self):
        #test
        actual = self.new_dir_info_tree.getChildren(1)
        expected = [2,3]
        self.assertEqual(actual, expected)

    def test_crud_02_getNodeByName(self):
        #test
        actual = str(self.new_dir_info_tree.getNodeByName('type 1'))
        expected = 'type 1 : 2'
        self.assertEqual(actual, expected)

    def test_crud_03_getNodeById(self):
        #test
        actual = str(self.new_dir_info_tree.getNodeById(1))
        expected = 'root : 1'
        self.assertEqual(actual, expected)

    def test_crud_04_getNodeIdByName(self):
        #test
        actual = self.new_dir_info_tree.getNodeIdByName('type 1')
        expected = 2
        self.assertEqual(actual, expected)

    def test_crud_05_isNodeByName_T(self):
        #test
        actual = self.new_dir_info_tree.isNodeByName('type 1')
        expected = True
        self.assertEqual(actual, expected)

    def test_crud_05_isNodeByName_F(self):
        #test
        actual = self.new_dir_info_tree.isNodeByName('notaname')
        expected = False
        self.assertEqual(actual, expected)

    def test_crud_06_isRootSet_F(self):
        #test
        actual = self.new_dir_info_tree.isRootSet()
        expected = False
        self.assertEqual(actual, expected)

    def test_crud_06_setRootName_isRootSet_T(self):
        # set root
        self.new_dir_info_tree.setRootName('root_path_test', {})
        #test
        actual = self.new_dir_info_tree.isRootSet()
        expected = True
        self.assertEqual(actual, expected)

    def test_crud_07_upDateNode(self):
        #test
        self.new_dir_info_tree.upDateNode(2, {'stuff': 'new_info'})
        actual = self.new_dir_info_tree.getNodeById(2).content
        expected = {'stuff': 'new_info'}
        self.assertEqual(actual, expected)

    def test_crud_08_upDateNodeByName(self):
        #test
        self.new_dir_info_tree.upDateNodeByName('type 1', {'stuff2': 'newer info'})
        actual = self.new_dir_info_tree.getNodeByName('type 1').content
        expected = {'stuff': 'info', 'stuff2': 'newer info'}
        self.assertEqual(actual, expected)

    def test_crud_09_nodeCount(self):
        #test
        actual = self.new_dir_info_tree.nodeCount()
        expected = 3
        self.assertEqual(actual, expected)

 # TODO chpcher staderOut from print in prettyTreeTable
 #    def test_crud_10_prettyTreeTable(self):
 #        actual = self.new_dir_info_tree.prettyTreeTable())
 #        expected = """Start prettyTreeTable
 # 1 - root
 # |___ 2 - type 1
 #      |___ 3 - type 2"""
 #        self.assertEqual(actual, expected)

if __name__ == "__main__":
    unittest.main(verbosity=2)
