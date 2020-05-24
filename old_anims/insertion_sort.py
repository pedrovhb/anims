from typing import List

from manimlib.imports import *
import random

SCALE = 1.8
Y_SHIFT = 0.9


class Element:
    def __init__(self, val):
        self.val = val
        self.circle = Circle(radius=0.4 * SCALE)
        self.text = TextMobject(str(self.val))
        self.text.scale(SCALE)


def swap_elements(
    els: List[Element], index_1: int, index_2: int, min_element_arrow: Arrow, s: Scene
):
    # Left element moves up, right element down
    # Swap X positions
    # Y positions go back to 0

    index_1, index_2 = min(index_1, index_2), max(index_1, index_2)
    pos_1 = [(-(len(els) / 2) + index_1 + 0.5) * SCALE, Y_SHIFT * SCALE, 0]
    pos_2 = [(-(len(els) / 2) + index_2 + 0.5) * SCALE, -Y_SHIFT * SCALE, 0]

    # Shift Y
    s.play(
        ApplyMethod(els[index_1].circle.move_to, pos_1),
        ApplyMethod(els[index_1].text.move_to, pos_1),
        ApplyMethod(els[index_2].circle.move_to, pos_2),
        ApplyMethod(els[index_2].text.move_to, pos_2),
        ApplyMethod(min_element_arrow.move_to, pos_2 + DOWN * SCALE * 0.8),
    )

    # Move X
    pos_1[0], pos_2[0] = pos_2[0], pos_1[0]
    s.play(
        ApplyMethod(els[index_1].circle.move_to, pos_1),
        ApplyMethod(els[index_1].text.move_to, pos_1),
        ApplyMethod(els[index_2].circle.move_to, pos_2),
        ApplyMethod(els[index_2].text.move_to, pos_2),
        ApplyMethod(min_element_arrow.move_to, pos_2 + DOWN * SCALE * 0.8),
    )

    # Unshift Y
    pos_1[1], pos_2[1] = 0, 0
    s.play(
        ApplyMethod(els[index_1].circle.move_to, pos_1),
        ApplyMethod(els[index_1].text.move_to, pos_1),
        ApplyMethod(els[index_2].circle.move_to, pos_2),
        ApplyMethod(els[index_2].text.move_to, pos_2),
        ApplyMethod(min_element_arrow.move_to, pos_2 + DOWN * SCALE * 0.8),
    )


class SelectionSort(Scene):
    def construct(self):
        shuffled_arr = [0, 2, 4, 5, 6, 7, 9]
        random.shuffle(shuffled_arr)
        els = [Element(n) for n in shuffled_arr]

        # Move elements to their starting positions
        for i in range(len(els)):
            new_pos = [(-(len(els) / 2) + i + 0.5) * SCALE, 0, 0]
            els[i].circle.move_to(new_pos)
            els[i].text.move_to(new_pos)

        # Show the creation of elements
        self.wait(0.5)
        self.play(
            *[ShowCreation(el.circle) for el in els], *[Write(el.text) for el in els]
        )

        # Current length of sorted sub-array
        sorted_len = 1
        while sorted_len < len(els) - 1:

            # Should start at the beginning of the unsorted sub-array
            for i in range(sorted_len, len(els)):
                cont_flag = False
                if els[i].val < els[i - 1].val:
                    self.play(
                        ApplyMethod(els[i].circle.shift, DOWN * SCALE * 1.5),
                        ApplyMethod(els[i].text.shift, DOWN * SCALE * 1.5),
                    )
                    for j in range(sorted_len, -1, -1):
                        self.play(
                            ApplyMethod(els[i].circle.shift, LEFT * SCALE),
                            ApplyMethod(els[i].text.shift, LEFT * SCALE),
                        )
                        print(i, j - 1)
                        print(els[i].val, els[j - 1].val)
                        if j - 1 < 0 or els[j - 1].val < els[i].val:
                            self.play(
                                *[
                                    ApplyMethod(el.circle.shift, RIGHT * SCALE)
                                    for el in els[j - 1 : i]
                                ],
                                *[
                                    ApplyMethod(el.text.shift, RIGHT * SCALE)
                                    for el in els[j - 1 : i]
                                ]
                            )
                            self.play(
                                ApplyMethod(els[i].circle.shift, UP * SCALE * 1.5),
                                ApplyMethod(els[i].text.shift, UP * SCALE * 1.5),
                            )

                            left_sorted, right_sorted, unsorted = (
                                els[: j - 1],
                                els[j - 1 : i],
                                els[i + 1 :],
                            )
                            els = left_sorted + [els[i]] + right_sorted + unsorted
                            print([el.val for el in els])
                            sorted_len += 1
                            cont_flag = True
                            break
                if cont_flag:
                    continue

            break
        self.wait(4)
