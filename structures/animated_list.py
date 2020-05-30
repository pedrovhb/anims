from itertools import chain

from manim import *

from structures import ListElement


class AnimatedList:
    DISTANCE_BETWEEN_ELS = RIGHT * 0.3
    SWAP_NONADJACENT_Y_CHANGE = 1
    SWAP_NONADJACENT_N_POINTS = 100

    def __init__(self, initial_list):
        self.lst = initial_list
        self.el_lst = [ListElement(val) for val in self.lst]

        all_submobjects = []
        for submobject_lst in (chain(el.vgroup.submobjects) for el in self.el_lst):
            all_submobjects.extend(submobject_lst)
        self.group = VGroup(*all_submobjects)

        for i, el in enumerate(self.el_lst):
            el.vgroup.shift(RIGHT * i + self.DISTANCE_BETWEEN_ELS * i)

        self.group.shift(LEFT * self.group.get_width() / 2)

    def swap_positions(self, i, j):
        self.lst[i], self.lst[j] = self.lst[j], self.lst[i]
        self.el_lst[i], self.el_lst[j] = self.el_lst[j], self.el_lst[i]
        # if abs(i - j) == 1:
        #     return self._swap_list_els_adjacent(self.el_lst[i], self.el_lst[j])
        # else:
        # return [ApplyFunction(lambda x: x.shift(UP) and x.shift(LEFT), self.el_lst[2].vgroup)]
        pmo = PMobject()
        pmo.add_points([(1, 0.01 * i, 0) for i in range(1, 100)])
        return [MoveAlongPath(self.el_lst[1].vgroup, pmo)]

    def make_path(self, frm, to, y_sign):
        pmo = PMobject()
        for i in range(self.SWAP_NONADJACENT_N_POINTS//4):
            # pmo.add_points(*np.)

    @staticmethod
    def _swap_list_els_adjacent(c1: ListElement, c2: ListElement):
        # Transforms happen from one object to another. If we want to animate
        # a clockwise movement, then we have to transform into copies that are
        # in another location
        c1_copy, c2_copy = deepcopy(c1), deepcopy(c2)
        c1_copy.vgroup.move_to(c2.vgroup.get_center())
        c2_copy.vgroup.move_to(c1.vgroup.get_center())
        return [
            CounterclockwiseTransform(c1.vgroup, c1_copy.vgroup),
            CounterclockwiseTransform(c2.vgroup, c2_copy.vgroup),
        ]
