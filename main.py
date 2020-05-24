import random

from manim.imports import *

SCALE = 1.8


class Element:
    def __init__(self, val):
        self.val = val
        self.circle = Circle(radius=0.4 * SCALE)
        self.text = TextMobject(str(self.val))
        self.text.scale(SCALE)


def swap_mobjects(c1: Mobject, c2: Mobject):
    # Transforms happen from one object to another. If we want to animate
    # a clockwise movement, then we have to transform into copies that are
    # in another location
    c1_copy, c2_copy = deepcopy(c1), deepcopy(c2)
    c1_copy.move_to(c2.get_center())
    c2_copy.move_to(c1.get_center())
    return [
        CounterclockwiseTransform(c1, c1_copy),
        CounterclockwiseTransform(c2, c2_copy),
    ]


def swap_elements(e1: Element, e2: Element):
    # This returns the animations produced by swapping both text and the circles for the
    # given elements.
    return [*swap_mobjects(e1.text, e2.text), *swap_mobjects(e1.circle, e2.circle)]


class BubbleSort(Scene):
    def construct(self):
        code = Code("bubble_sort.py")
        code.shift(UP * 2)
        self.play(ShowCreation(code))
        # shuffled_arr = [0, 2, 4, 5, 6, 7, 9]
        shuffled_arr = [4, 5, 0, 2, 6, 7, 9]
        random.shuffle(shuffled_arr)
        els = [Element(n) for n in shuffled_arr]

        # Create sliding rectangle
        crt_view_rectangle = Rectangle(width=2 * SCALE, height=1 * SCALE)

        # Move elements to their starting positions
        for i in range(len(shuffled_arr)):
            new_pos = [(-3 + i) * SCALE, 0, 0]
            els[i].circle.move_to(new_pos)
            els[i].text.move_to(new_pos)

        self.play(ShowPassingFlashAround(code.code[0]))
        # Show the creation of elements
        self.play(
            *[ShowCreation(el.circle) for el in els], *[Write(el.text) for el in els]
        )

        # Move the rectangle to its starting position
        initial_rect_pos = midpoint(
            els[0].circle.get_center(), els[1].circle.get_center()
        )
        crt_view_rectangle.move_to(initial_rect_pos)

        # Show the creation of the rectangle
        self.play(ShowCreation(crt_view_rectangle))

        # Start sorting
        while True:
            self.play(ShowPassingFlashAround(code.code[1]))

            # For each cycle, swapped flag is initially false
            swapped = False
            self.play(ShowPassingFlashAround(code.code[2]))

            # For each element until the second-to-last one...
            for i in range(len(shuffled_arr) - 1):
                self.play(ShowPassingFlashAround(code.code[3]))

                # If this element's value is larger than the next one...
                self.play(ShowPassingFlashAround(code.code[4]))
                if els[i].val > els[i + 1].val:
                    # Swap them
                    self.play(ShowPassingFlashAround(code.code[5]))
                    els[i], els[i + 1] = els[i + 1], els[i]

                    # Set the swapped flag to True
                    swapped = True

                    # Play the swapping animation
                    self.play(*swap_elements(els[i], els[i + 1]))

                # Move the rectangle to its next position
                if i != len(shuffled_arr) - 2:
                    self.play(ApplyMethod(crt_view_rectangle.shift, RIGHT * SCALE))

            # At the end of the cycle, move the rectangle back to its starting position
            self.play(ApplyMethod(crt_view_rectangle.move_to, initial_rect_pos))

            # If the swapped flag hasn't been set to true, we went through the
            # array without swapping anything, and that means that it's been sorted
            self.play(ShowPassingFlashAround(code.code[6]))
            if not swapped:
                self.play(ShowPassingFlashAround(code.code[7]))
                break

        # When we're done, animate a change color to green for all the elements
        self.play(*[ApplyMethod(el.circle.set_color, GREEN_C) for el in els])

        self.wait(3)
