from typing import List

from manimlib.imports import *
import random

SCALE = 1.8
Y_SHIFT = 1.1


class Element:
    def __init__(self, val):
        self.val = val
        self.circle = Circle(radius=0.4 * SCALE)
        self.text = TextMobject(str(self.val))
        self.text.scale(SCALE)


def rearrange_elements(els: List[Element]):
    # Centers elements horizontally

    anims = []
    for i in range(len(els)):
        new_pos = [(-(len(els) / 2) + i + 0.5) * SCALE, Y_SHIFT * SCALE, 0]
        anims.append(ApplyMethod(els[i].text.move_to, new_pos))
        anims.append(ApplyMethod(els[i].circle.move_to, new_pos))
    return anims


class SelectionSort(Scene):
    def construct(self):

        shuffled_arr = [0, 2, 4, 5, 6, 7, 9]
        random.shuffle(shuffled_arr)
        els = [Element(n) for n in shuffled_arr]
        sorted_els = []

        # Move elements to their starting positions
        for i in range(len(els)):
            new_pos = [(-(len(els) / 2) + i + 0.5) * SCALE, Y_SHIFT * SCALE, 0]
            els[i].circle.move_to(new_pos)
            els[i].text.move_to(new_pos)

        # Show the creation of elements
        self.wait(0.5)
        self.play(
            *[ShowCreation(el.circle) for el in els], *[Write(el.text) for el in els]
        )

        # Start sorting
        while els:

            # The first element starts out being the min
            min_el_index = 0
            self.play(ApplyMethod(els[min_el_index].circle.set_color, BLUE_C))

            # For each element other than the first one...
            for i in range(1, len(els)):

                # If this element is smaller than the min element seen yet...
                if els[i].val < els[min_el_index].val:
                    # Set this circle's color to blue and the previous min's to yellow
                    self.play(
                        ApplyMethod(els[i].circle.set_color, BLUE_C),
                        ApplyMethod(els[min_el_index].circle.set_color, YELLOW_B),
                    )
                    # Update new min index
                    min_el_index = i
                else:
                    # If it's not less than the min element, just mark it as yellow (visited)
                    self.play(ApplyMethod(els[i].circle.set_color, YELLOW_B))

            new_element_x = (-3 + len(sorted_els)) * SCALE
            new_element_y = -Y_SHIFT * SCALE

            moved_element = els.pop(min_el_index)
            sorted_els.append(moved_element)

            # Move element down (to baseline)
            self.play(
                ApplyMethod(moved_element.circle.shift, DOWN * SCALE * Y_SHIFT),
                ApplyMethod(moved_element.text.shift, DOWN * SCALE * Y_SHIFT),
            )

            rearrange_shuffled_els_anims = rearrange_elements(els)

            # Move element to its new X position and shuffled elements to new position
            self.play(
                ApplyMethod(moved_element.circle.move_to, [new_element_x, 0, 0]),
                ApplyMethod(moved_element.text.move_to, [new_element_x, 0, 0]),
                *rearrange_shuffled_els_anims,
            )

            # Move element down to sorted Y position and recolor shuffled elements red
            self.play(
                ApplyMethod(
                    moved_element.circle.move_to, [new_element_x, new_element_y, 0]
                ),
                ApplyMethod(
                    moved_element.text.move_to, [new_element_x, new_element_y, 0]
                ),
                *[ApplyMethod(el.circle.set_color, RED_C) for el in els],
            )

        # Turn sorted elements green and move them to center of the screen
        self.play(
            *[ApplyMethod(el.circle.shift, UP * Y_SHIFT * SCALE) for el in sorted_els],
            *[ApplyMethod(el.text.shift, UP * Y_SHIFT * SCALE) for el in sorted_els],
        )
        self.play(*[ApplyMethod(el.circle.set_color, GREEN_C) for el in sorted_els])

        self.wait(4)
