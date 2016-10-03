from ftw.chameleon.utils import get_subclasses
from unittest2 import TestCase


class TestGetSubclasses(TestCase):

    def test(self):
        class A(object): pass
        class B(A): pass
        class C(B): pass

        self.assertEqual(
            [A, B, C],
            list(get_subclasses(A)))
