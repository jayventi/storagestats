# test_treetable

import unittest

from treetable import TreeTable

#  Basic creation and detection
class TestTreeTableBaicCre(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_init_1_table_table_full_dump_init(self):
        # setup
        new_dir_info_tree = TreeTable()
        #test
        actual = new_dir_info_tree.table_full_dump()
        expected = 'node_id: 1 root\t parent:1 chindren: []\t  \n'
        self.assertEqual(actual, expected)

    def test_init_2_add_child_Dump_to_json(self):
        # setup
        new_dir_info_tree = TreeTable()
        new_dir_info_tree.add_child('type 1', 1, {'stuff': 'info'})
        new_dir_info_tree.add_child('type 2', 1, {'stuff': 'info'})
        #test
        actual = new_dir_info_tree.to_json()
        expected = '''{"1": {"content": {}, "parent_id": 1, "node_id": 1, "name": "root", "children": [2, 3]}, "2": {"content": {"stuff": "info"}, "parent_id": 1, "node_id": 2, "name": "type 1", "children": []}, "3": {"content": {"stuff": "info"}, "parent_id": 1, "node_id": 3, "name": "type 2", "children": []}}'''
        self.assertEqual(actual, expected)

    def test_init_3_from_json(self):
        #setup
        new_dir_info_tree = TreeTable()
        new_dir_info_tree.add_child('type 1', 1, {'stuff': 'info'})
        new_dir_info_tree.add_child('type 2', 1, {'stuff': 'info'})
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
        self.new_dir_info_tree.add_child('type 1', 1, {'stuff': 'info'})
        self.new_dir_info_tree.add_child('type 2', 1, {'stuff': 'info'})

    def tearDown(self):
        pass

    def test_crud_01_get_children(self):
        #test
        actual = self.new_dir_info_tree.get_children(1)
        expected = [2,3]
        self.assertEqual(actual, expected)

    def test_crud_02_get_node_by_name(self):
        #test
        actual = str(self.new_dir_info_tree.get_node_by_name('type 1'))
        expected = 'type 1 : 2'
        self.assertEqual(actual, expected)

    def test_crud_03_get_node_by_id(self):
        #test
        actual = str(self.new_dir_info_tree.get_node_by_id(1))
        expected = 'root : 1'
        self.assertEqual(actual, expected)

    def test_crud_04_getnode_idByName(self):
        #test
        actual = self.new_dir_info_tree.getnode_idByName('type 1')
        expected = 2
        self.assertEqual(actual, expected)

    def test_crud_05_is_node_by_name_T(self):
        #test
        actual = self.new_dir_info_tree.is_node_by_name('type 1')
        expected = True
        self.assertEqual(actual, expected)

    def test_crud_05_is_node_by_name_F(self):
        #test
        actual = self.new_dir_info_tree.is_node_by_name('notaname')
        expected = False
        self.assertEqual(actual, expected)

    def test_crud_06_is_root_set_F(self):
        #test
        actual = self.new_dir_info_tree.is_root_set()
        expected = False
        self.assertEqual(actual, expected)

    def test_crud_06_set_root_name_is_root_set_T(self):
        # set root
        self.new_dir_info_tree.set_root_name('root_path_test', {})
        #test
        actual = self.new_dir_info_tree.is_root_set()
        expected = True
        self.assertEqual(actual, expected)

    def test_crud_07_upDateNode(self):
        #test
        self.new_dir_info_tree.up_date_node(2, {'stuff': 'new_info'})
        actual = self.new_dir_info_tree.get_node_by_id(2).content
        expected = {'stuff': 'new_info'}
        self.assertEqual(actual, expected)

    def test_crud_08_up_date_node_by_name(self):
        #test
        self.new_dir_info_tree.up_date_node_by_name('type 1', {'stuff2': 'newer info'})
        actual = self.new_dir_info_tree.get_node_by_name('type 1').content
        expected = {'stuff': 'info', 'stuff2': 'newer info'}
        self.assertEqual(actual, expected)

    def test_crud_09_node_count(self):
        #test
        actual = self.new_dir_info_tree.node_count()
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
