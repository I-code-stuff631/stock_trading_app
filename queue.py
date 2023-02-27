import unittest


class _Node:
    def __init__(self, elem, prio):
        self.next: _Node | None = None
        self.elem = elem
        self.prio = prio

    def __str__(self) -> str:
        return f"({self.elem}, {self.prio})" + (" -> " if self.next is not None else "")


class PQueue:
    """A priority queue implemented with a linked list for some reason"""
    def __init__(self, priority_determiner=lambda new_prio, old_prio: new_prio > old_prio):
        """Priority determiner takes two priorities returning True if the first prioritie is higher than the second
        and False if it is not"""
        self._head: _Node | None = None  # Should only need a head
        self._new_has_priority = priority_determiner
        self._length = 0

    def push(self, item, priority):  # enqueue(data, priority):
        """Pushes an item onto the queue based on the priority"""
        new = _Node(item, priority)
        if self._head is None or self._new_has_priority(new.prio, self._head.prio):  # The list is empty
            new.next = self._head
            self._head = new
            self._length += 1
            return
        before: _Node = self._head  # The node before the new one
        while before.next is not None and not self._new_has_priority(new.prio, before.next.prio):
            before = before.next
        after: _Node | None = before.next  # The node after the new one
        before.next = new
        new.next = after
        self._length += 1

    # noinspection PyShadowingBuiltins
    def pop(self):  # dequeue():
        """Removes an item with the highest priority from the list"""
        if self._head is None:  # The list is empty
            return None
        elem = self._head.elem
        self._head = self._head.next
        self._length -= 1
        return elem

    def is_empty(self):
        return self._head is None

    def clear(self):
        self._head = None
        self._length = 0

    def peek(self):
        """Returns the next element to be popped without actually removing it from the list"""
        if self._head is not None:
            return self._head.elem

    def __len__(self):
        return self._length

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
        fmted_nodes = ""
        next = self._head
        while next is not None:
            fmted_nodes += str(next)
            next = next.next
        return fmted_nodes


class Test(unittest.TestCase):
    def setUp(self) -> None:
        self.queue = PQueue(lambda new_prio, old_prio: new_prio >= old_prio)

    def test_empty_queue_behavior(self):
        self.assertEqual(None, self.queue.pop())
        self.assertEqual(None, self.queue.peek())
        self.assertTrue(self.queue.is_empty())
        self.assertEqual(0, len(self.queue))

    def test_priority(self):
        self.queue.push(6, 5)
        self.queue.push(9, 7)
        self.queue.push(5, 3)
        self.queue.push(2, 9)
        self.queue.push(1, 6)
        self.queue.push(0, 8)
        self.queue.push(6, 4)
        self.queue.push(4, 1)
        self.queue.push(0, 0)
        self.queue.push(7, 2)
        self.assertEqual(2, self.queue.pop())
        self.assertEqual(0, self.queue.pop())
        self.assertEqual(9, self.queue.pop())
        self.assertEqual(1, self.queue.pop())
        self.assertEqual(6, self.queue.pop())
        self.assertEqual(6, self.queue.pop())
        self.assertEqual(5, self.queue.pop())
        self.assertEqual(7, self.queue.pop())
        self.assertEqual(4, self.queue.pop())
        self.assertEqual(0, self.queue.pop())

    def test_duplicates(self):
        self.queue.push(3, 5)
        self.queue.push(1, 1)
        self.queue.push(2, 10)
        self.queue.push(3, 5)
        self.queue.push(2, 10)
        self.queue.push(1, 1)
        self.assertEqual(2, self.queue.pop())
        self.assertEqual(2, self.queue.pop())
        self.assertEqual(3, self.queue.pop())
        self.assertEqual(3, self.queue.pop())
        self.assertEqual(1, self.queue.pop())
        self.assertEqual(1, self.queue.pop())

    def test_length_tracking(self):
        self.queue.push(None, 0)
        self.assertEqual(1, len(self.queue))

        for _ in range(10):
            self.queue.push(None, 0)
        self.assertEqual(11, len(self.queue))

        self.queue.pop()
        self.assertEqual(10, len(self.queue))
        self.queue.peek()
        self.assertEqual(10, len(self.queue))

        for _ in range(5):
            self.queue.pop()
        self.assertEqual(5, len(self.queue))

        self.queue.clear()
        self.assertEqual(0, len(self.queue))
        self.queue.pop()
        self.assertEqual(0, len(self.queue))

    def test_other(self):
        self.assertEqual(None, self.queue.peek())
        self.queue.push(0, 0)
        self.assertEqual(0, self.queue.peek())
        self.assertEqual(0, self.queue.peek())  # Was not removed

        self.assertFalse(self.queue.is_empty())

        self.queue.push(0, 1)
        self.queue.push(0, 2)
        self.queue.push(0, 3)
        self.queue.push(0, 4)
        self.queue.clear()
        self.test_empty_queue_behavior()

    def test_iter(self):
        self.queue.push(6, 3)
        self.queue.push(10, 0)
        self.queue.push(10, 0)
        self.queue.push(0, 7)
        self.queue.push(2, 9)
        self.queue.push(3, 8)
        self.queue.push(0, 6)
        queue_iter = iter(self.queue)
        self.assertEqual(2, next(queue_iter))
        self.assertEqual(3, next(queue_iter))
        self.assertEqual(0, next(queue_iter))
        self.assertEqual(0, next(queue_iter))
        self.assertEqual(6, next(queue_iter))
        self.assertEqual(10, next(queue_iter))
        self.assertEqual(10, next(queue_iter))
        self.assertRaises(StopIteration, queue_iter.__next__)  # The iteration is complete

    def test_print(self):
        self.queue.push(2, 10)
        self.queue.push(2, 10)
        self.queue.push(1, 1)
        self.queue.push(3, 5)
        self.assertEqual("(2, 10) -> (2, 10) -> (3, 5) -> (1, 1)", str(self.queue))


if __name__ == '__main__':
    unittest.main()
