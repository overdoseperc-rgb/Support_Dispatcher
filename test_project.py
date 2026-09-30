"""Контрольные и граничные проверки: python -m unittest -v."""
import contextlib
import io
import random
import unittest
import main as app


class ProjectTests(unittest.TestCase):
    def test_document_controls(self):
        with contextlib.redirect_stdout(io.StringIO()):
            app.main()

    def test_empty(self):
        self.assertEqual(app.height(None), 0)
        self.assertEqual(app.count_nodes(None), 0)
        self.assertEqual(app.count_leaves(None), 0)
        self.assertTrue(app.validate_bst(None))
        for traversal in (app.preorder, app.inorder, app.postorder, app.levelorder):
            self.assertEqual(traversal(None), [])
        self.assertEqual(app.search(None, 1), (None, []))
        self.assertIsNone(app.get_depth(None, 1))
        self.assertIsNone(app.find_min(None))
        self.assertIsNone(app.find_max(None))
        self.assertIsNone(app.delete(None, 1))

    def test_root_deletion_and_record_transfer(self):
        root = app.make_initial_tree()
        successor = app.search(root, 55)[0]
        root = app.delete(root, 50)
        self.assertEqual(root.request, successor)
        self.assertEqual(app.count_nodes(root), 14)
        self.assertTrue(app.validate_bst(root))
        root = app.TreeNode(app.Request(2, "Корень", 3),
                            app.TreeNode(app.Request(1, "Потомок", 4)))
        root = app.delete(root, 2)
        self.assertEqual(root.request.id, 1)
        self.assertIsNone(app.delete(root, 1))

    def test_duplicate_and_missing_deletion(self):
        root = app.make_initial_tree()
        before = app.preorder(root)
        root = app.insert(root, app.Request(50, "Замена", 100))
        root = app.delete(root, 999)
        self.assertEqual(app.preorder(root), before)

    def test_global_bst_bounds(self):
        root = app.TreeNode(app.Request(10,"",1),
            app.TreeNode(app.Request(5,"",1), right=app.TreeNode(app.Request(12,"",1))))
        self.assertFalse(app.validate_bst(root))
        root.left.right.request = app.Request(10,"Дубликат",1)
        self.assertFalse(app.validate_bst(root))

    def test_heap_and_sort(self):
        rng = random.Random(2026)
        for size in (0,1,2,3,13,50,100):
            for _ in range(10):
                data = [app.Request(i, str(i), rng.randrange(5)) for i in range(size)]
                rng.shuffle(data)
                expected = sorted(data, key=app.request_key)  # Только эталон в тесте.
                identity = id(data)
                app.build_max_heap(data)
                self.assertTrue(app.is_max_heap(data))
                self.assertEqual(sorted(data,key=app.request_key), expected)
                self.assertIsNone(app.heap_sort(data))
                self.assertEqual(id(data), identity)
                self.assertEqual(data, expected)
        data = [app.Request(1,"",5), app.Request(2,"",5)]
        self.assertFalse(app.is_max_heap(data))
        app.build_max_heap(data)
        self.assertEqual(data[0].id, 2)


if __name__ == "__main__":
    unittest.main()
