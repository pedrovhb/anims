from itertools import chain

from manim import *

from structures import ListElement


class AnimatedList:
    DISTANCE_BETWEEN_ELS = RIGHT * 0.3

    # Manim units amount of going up/down in non-adjacent element swaps
    SWAP_NONADJACENT_Y_CHANGE = 1.5

    # Resolution for path traced while swapping nonadjacent list els
    SWAP_NONADJACENT_N_POINTS = 1000

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
        if abs(i - j) == 1:
            return self._swap_list_els_adjacent(self.el_lst[i], self.el_lst[j])

        pmo_1 = self._make_path_non_adjacent_swap(self.el_lst[i], self.el_lst[j], 1)
        pmo_2 = self._make_path_non_adjacent_swap(self.el_lst[j], self.el_lst[i], -1)
        return [
            MoveAlongPath(self.el_lst[i].vgroup, pmo_1),
            MoveAlongPath(self.el_lst[j].vgroup, pmo_2)
        ]

    def _make_path_non_adjacent_swap(self, frm_el: ListElement, to_el: ListElement, y_sign: int):
        pmo = PMobject()
        frm_x = frm_el.vgroup.get_x()
        to_x = to_el.vgroup.get_x()
        baseline_y = frm_el.vgroup.get_y()

        total_distance = abs(frm_x - to_x) + self.SWAP_NONADJACENT_Y_CHANGE * 2
        y_climb_proportion = total_distance / self.SWAP_NONADJACENT_Y_CHANGE
        n_points_climb = self.SWAP_NONADJACENT_N_POINTS // y_climb_proportion
        n_points_x = self.SWAP_NONADJACENT_N_POINTS - n_points_climb

        # better - https://numpy.org/doc/stable/reference/generated/numpy.linspace.html#numpy.linspace

        pmo.add_points([(
            frm_x,
            (baseline_y
             + (i / int(n_points_climb / 2))
             * self.SWAP_NONADJACENT_Y_CHANGE
             * y_sign),
            0)
            for i in range(int(n_points_climb / 2))
        ])

        pmo.add_points([(
            frm_x + (i / n_points_x) * (to_x - frm_x),
            (baseline_y
             + self.SWAP_NONADJACENT_Y_CHANGE
             * y_sign),
            0)
            for i in range(int(n_points_x))
        ])

        pmo.add_points([(
            to_x,
            (baseline_y
             + self.SWAP_NONADJACENT_Y_CHANGE * y_sign
             + (i / int(n_points_climb / 2))
             * self.SWAP_NONADJACENT_Y_CHANGE
             * y_sign * -1),
            0)
            for i in range(int(n_points_climb / 2))
        ])
        return pmo

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
