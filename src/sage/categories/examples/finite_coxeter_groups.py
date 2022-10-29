r"""
Examples of finite Coxeter groups
"""
# ****************************************************************************
#  Copyright (C) 2008 Nicolas M. Thiery <nthiery at users.sf.net>
#  Copyright (C) 2009 Nicolas Borie <nicolas dot borie at math.u-psud.fr>
#
#  Distributed under the terms of the GNU General Public License (GPL)
#                  https://www.gnu.org/licenses/
# *****************************************************************************
from sage.misc.cachefunc import cached_method
from sage.structure.parent import Parent
from sage.structure.element_wrapper import ElementWrapper
from sage.categories.all import FiniteCoxeterGroups
from sage.structure.unique_representation import UniqueRepresentation
from sage.misc.functional import is_odd, is_even
from sage.combinat.root_system.coxeter_matrix import CoxeterMatrix


class DihedralGroup(UniqueRepresentation, Parent):
    r"""
    An example of finite Coxeter group: the `n`-th dihedral group of order `2n`.

    The purpose of this class is to provide a minimal template for
    implementing finite Coxeter groups. See
    :class:`~sage.groups.perm_gps.permgroup_named.DihedralGroup` for a
    full featured and optimized implementation.

    EXAMPLES::

        sage: G = FiniteCoxeterGroups().example()

    This group is generated by two simple reflections `s_1` and `s_2`
    subject to the relation `(s_1s_2)^n = 1`::

        sage: G.simple_reflections()
        Finite family {1: (1,), 2: (2,)}

        sage: s1, s2 = G.simple_reflections()
        sage: (s1*s2)^5 == G.one()
        True

    An element is represented by its reduced word (a tuple of elements
    of `self.index_set()`)::

        sage: G.an_element()
        (1, 2)

        sage: list(G)
        [(),
         (1,),
         (2,),
         (1, 2),
         (2, 1),
         (1, 2, 1),
         (2, 1, 2),
         (1, 2, 1, 2),
         (2, 1, 2, 1),
         (1, 2, 1, 2, 1)]

    This reduced word is unique, except for the longest element where
    the chosen reduced word is `(1,2,1,2\dots)`::

        sage: G.long_element()
        (1, 2, 1, 2, 1)

    TESTS::

        sage: TestSuite(G).run()

        sage: c = FiniteCoxeterGroups().example(3).cayley_graph()
        sage: c.edges(sort=True)
        [((), (1,), 1),
         ((), (2,), 2),
         ((1,), (), 1),
         ((1,), (1, 2), 2),
         ((1, 2), (1,), 2),
         ((1, 2), (1, 2, 1), 1),
         ((1, 2, 1), (1, 2), 1),
         ((1, 2, 1), (2, 1), 2),
         ((2,), (), 2),
         ((2,), (2, 1), 1),
         ((2, 1), (1, 2, 1), 2),
         ((2, 1), (2,), 1)]
    """

    def __init__(self, n=5):
        r"""
        Construct the `n`-th DihedralGroup of order `2 n`.

        INPUT:

        - `n` -- an integer with `n>=2`

        EXAMPLES::

            sage: from sage.categories.examples.finite_coxeter_groups import DihedralGroup
            sage: DihedralGroup(3)
            The 3-th dihedral group of order 6
        """
        assert n >= 2
        Parent.__init__(self, category=FiniteCoxeterGroups())
        self.n = n

    def _repr_(self):
        r"""
        EXAMPLES::

            sage: FiniteCoxeterGroups().example()
            The 5-th dihedral group of order 10
            sage: FiniteCoxeterGroups().example(6)
            The 6-th dihedral group of order 12
        """
        return "The %s-th dihedral group of order %s" % (self.n, 2 * self.n)

    def __contains__(self, x):
        r"""
        Check in the element x is in the mathematical parent self.

        EXAMPLES::

            sage: D5 = FiniteCoxeterGroups().example()
            sage: D5.an_element() in D5
            True
            sage: 1 in D5
            False

        (also tested by :meth:`test_an_element` :meth:`test_some_elements`)
        """
        from sage.structure.all import parent
        return parent(x) is self

    @cached_method
    def one(self):
        r"""
        Implements :meth:`Monoids.ParentMethods.one`.

        EXAMPLES::

            sage: D6 = FiniteCoxeterGroups().example(6)
            sage: D6.one()
            ()
        """
        return self(())

    def index_set(self):
        r"""
        Implements :meth:`CoxeterGroups.ParentMethods.index_set`.

        EXAMPLES::

            sage: D4 = FiniteCoxeterGroups().example(4)
            sage: D4.index_set()
            (1, 2)
        """
        return (1, 2)

    def degrees(self):
        """
        Return the degrees of ``self``.

        EXAMPLES::

            sage: FiniteCoxeterGroups().example(6).degrees()
            (2, 6)
        """
        from sage.rings.integer_ring import ZZ
        return (ZZ(2), ZZ(self.n))

    def coxeter_matrix(self):
        """
        Return the Coxeter matrix of ``self``.

        EXAMPLES::

            sage: FiniteCoxeterGroups().example(6).coxeter_matrix()
            [1 6]
            [6 1]
        """
        return CoxeterMatrix([[1, self.n], [self.n, 1]])

    class Element(ElementWrapper):
        wrapped_class = tuple
        __lt__ = ElementWrapper._lt_by_value

        def has_right_descent(self, i, positive=False, side="right"):
            r"""
            Implements :meth:`SemiGroups.ElementMethods.has_right_descent`.

            EXAMPLES::

                sage: D6 = FiniteCoxeterGroups().example(6)
                sage: s = D6.simple_reflections()
                sage: s[1].has_descent(1)
                True
                sage: s[1].has_descent(1)
                True
                sage: s[1].has_descent(2)
                False
                sage: D6.one().has_descent(1)
                False
                sage: D6.one().has_descent(2)
                False
                sage: D6.long_element().has_descent(1)
                True
                sage: D6.long_element().has_descent(2)
                True

            TESTS::

                sage: D6._test_has_descent()
            """
            reduced_word = self.value
            if len(reduced_word) == self.parent().n:
                return not positive
            elif len(reduced_word) == 0:
                return positive
            else:
                return (i == reduced_word[0 if side == "left" else -1]) == (not positive)

        def apply_simple_reflection_right(self, i):
            r"""
            Implements :meth:`CoxeterGroups.ElementMethods.apply_simple_reflection`.

            EXAMPLES::

                sage: D5 = FiniteCoxeterGroups().example(5)
                sage: [i^2 for i in D5]  # indirect doctest
                [(), (), (), (1, 2, 1, 2), (2, 1, 2, 1), (), (), (2, 1), (1, 2), ()]
                sage: [i^5 for i in D5]  # indirect doctest
                [(), (1,), (2,), (), (), (1, 2, 1), (2, 1, 2), (), (), (1, 2, 1, 2, 1)]
            """
            from copy import copy
            reduced_word = copy(self.value)
            n = self.parent().n
            if len(reduced_word) == n:
                if (i == 1 and is_odd(n)) or (i == 2 and is_even(n)):
                    return self.parent()(reduced_word[:-1])
                else:
                    return self.parent()(reduced_word[1:])
            elif (len(reduced_word) == n-1 and (not self.has_descent(i))) and (reduced_word[0] == 2):
                return self.parent()((1,)+reduced_word)
            else:
                if self.has_descent(i):
                    return self.parent()(reduced_word[:-1])
                else:
                    return self.parent()(reduced_word+(i,))

Example = DihedralGroup
