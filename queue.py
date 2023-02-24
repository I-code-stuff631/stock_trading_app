import unittest


class _Node:
    def __init__(self, elem, prio):
        self.next: _Node | None = None
        self.elem = elem
        self.prio = prio

    def __str__(self) -> str:
        return f"({self.elem}, {self.prio})" + " -> " if self.next is not None else ""


class PQueue:
    """A priority queue implemented with a linked list for some reason"""
    def __init__(self):
        self._head: _Node | None = None  # Should only need a head

    def push(self, item, priority):  # enqueue(data, priority):
        new = _Node(item, priority)
        if self._head is None or self._head.prio < new.prio:  # The list is empty
            new.next = self._head
            self._head = new
            return
        before: _Node = self._head  # The node before the new one
        while before.next is not None and before.next.prio >= new.prio:  # Equal as well to satisfy FIFO better
            before = before.next
        after: _Node | None = before.next  # The node after the new one
        before.next = new
        new.next = after

    # noinspection PyShadowingBuiltins
    def pop(self):  # dequeue():
        """Removes an item with the highest priority from the list"""
        if self._head is None:  # The list is empty
            return None
        elem = self._head.elem
        self._head = self._head.next
        return elem

    def is_empty(self):
        return self._head is None

    def clear(self):
        self._head = None

    def __iter__(self):
        # noinspection PyShadowingBuiltins
        def generator():
            next = self._head
            while next is not None:
                yield next.elem
                next = next.next

        return generator()

    # noinspection PyShadowingBuiltins
    def __str__(self) -> str:
        fmted_nodes = ''
        next = self._head
        while next is not None:
            fmted_nodes += str(next)
            next = next.next
        return fmted_nodes


class Test(unittest.TestCase):
    def check_exhaustion(self, queue: PQueue):  # Exhaustion
        self.assertTrue(queue.is_empty())
        self.assertEqual(queue.pop(), None)

    def test_basics(self):
        queue = PQueue()
        self.check_exhaustion(queue)

        # Priorirty
        queue.push(6, 5)
        queue.push(9, 7)
        queue.push(5, 3)
        queue.push(2, 9)
        queue.push(1, 6)
        queue.push(0, 8)
        queue.push(6, 4)
        queue.push(4, 1)
        queue.push(0, 0)
        queue.push(7, 2)
        self.assertEqual(queue.pop(), 2)
        self.assertEqual(queue.pop(), 0)
        self.assertEqual(queue.pop(), 9)
        self.assertEqual(queue.pop(), 1)
        self.assertEqual(queue.pop(), 6)
        self.assertEqual(queue.pop(), 6)
        self.assertEqual(queue.pop(), 5)
        self.assertEqual(queue.pop(), 7)
        self.assertEqual(queue.pop(), 4)
        self.assertEqual(queue.pop(), 0)
        self.check_exhaustion(queue)

        # Duplicates
        queue.push(3, 5)
        queue.push(1, 1)
        queue.push(2, 10)
        queue.push(3, 5)
        queue.push(2, 10)
        queue.push(1, 1)
        self.assertEqual(queue.pop(), 2)
        self.assertEqual(queue.pop(), 2)
        self.assertEqual(queue.pop(), 3)
        self.assertEqual(queue.pop(), 3)
        self.assertEqual(queue.pop(), 1)
        self.assertEqual(queue.pop(), 1)
        self.check_exhaustion(queue)

        # FIFO
        queue.push(1, 10)
        queue.push(2, 10)
        queue.push(3, 10)
        queue.push(4, 10)
        self.assertEqual(queue.pop(), 1)
        self.assertEqual(queue.pop(), 2)
        self.assertEqual(queue.pop(), 3)
        self.assertEqual(queue.pop(), 4)
        self.check_exhaustion(queue)

        # Clear
        queue.push(0, 0)
        queue.push(0, 1)
        queue.push(0, 2)
        queue.push(0, 3)
        queue.clear()
        self.check_exhaustion(queue)

    def test_iter(self):
        queue = PQueue()
        self.check_exhaustion(queue)

        queue.push(6, 3)
        queue.push(10, 0)
        queue.push(10, 0)  #
        queue.push(9, 0)  #
        queue.push(0, 7)
        queue.push(2, 9)
        queue.push(3, 8)
        queue.push(0, 6)
        queue_iter = iter(queue)
        self.assertEqual(next(queue_iter), 2)
        self.assertEqual(next(queue_iter), 3)
        self.assertEqual(next(queue_iter), 0)
        self.assertEqual(next(queue_iter), 0)
        self.assertEqual(next(queue_iter), 6)
        self.assertEqual(next(queue_iter), 10)
        self.assertEqual(next(queue_iter), 10)
        self.assertEqual(next(queue_iter), 9)
        self.assertRaises(StopIteration, queue_iter.__next__)  # The iteration is complete

    def test_print(self):
        queue = PQueue()
        queue.push(2, 10)
        queue.push(2, 10)
        queue.push(1, 1)
        queue.push(3, 5)
        self.assertEqual("(2, 10) -> (2, 10) -> (3, 5) -> (1, 1)", str(queue))


if __name__ == '__main__':
    unittest.main()
