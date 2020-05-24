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

        # Create and show arrows
        current_arrow = Arrow(UP, DOWN * 0.2)
        current_arrow.next_to(els[0].circle, UP)

        min_element_arrow = Arrow(DOWN, UP * 0.2)
        min_element_arrow.next_to(els[0].circle, DOWN)
        min_element_arrow.set_color(GREEN_C)

        self.play(ShowCreation(current_arrow), ShowCreation(min_element_arrow))

        # Current length of sorted sub-array
        sorted_len = 0
        while True:

            # Should start at the beginning of the unsorted sub-array
            current_min_val_index = sorted_len
            for i in range(sorted_len, len(els)):

                arrow_anims = []

                # Always animate the "currently visiting" arrow to the current element
                arrow_anims.append(
                    ApplyMethod(current_arrow.next_to, els[i].circle, UP)
                )

                # If the element's value is smaller than the previous min element,
                # set the minimum element to this one and animate the min element arrow
                # to its position
                if els[i].val < els[current_min_val_index].val or i == sorted_len:
                    current_min_val_index = i
                    arrow_anims.append(
                        ApplyMethod(min_element_arrow.next_to, els[i].circle, DOWN)
                    )

                self.play(*arrow_anims)

            # Swap only if the min element isn't at the unsorted sub-array start
            if current_min_val_index != sorted_len:
                swap_elements(
                    els, sorted_len, current_min_val_index, min_element_arrow, self
                )
                els[sorted_len], els[current_min_val_index] = (
                    els[current_min_val_index],
                    els[sorted_len],
                )

            # Element is sorted, color it green
            self.play(ApplyMethod(els[sorted_len].circle.set_color, GREEN_C))

            # Increment sorted sub-array length
            sorted_len += 1

            # If we're sorted up to N - 1, we're all sorted
            if sorted_len == len(els) - 1:
                break

        # Vanish arrows
        self.play(
            FadeOutAndShift(min_element_arrow, DOWN), FadeOutAndShift(current_arrow, UP)
        )

        # Last element is sorted
        self.play(ApplyMethod(els[-1].circle.set_color, GREEN_C))

        self.wait(4)
