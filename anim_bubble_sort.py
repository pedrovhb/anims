from manimlib.imports import *


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


def get_element(n):
    VGroup()


class BubbleSort(Scene):
    def construct(self):
        code = Code(
            os.path.join(os.getcwd(), "bubble_sort.py"), style="Keyword=#FF88AA"
        )
        code.shift(UP * 2)
        code_width = max(line.get_width() for line in code.code)

        code_highlight = Rectangle(width=code_width, height=code.code[0].get_height())
        code_highlight.set_y(code.code[0].get_y())
        code_highlight.set_x(0)
        self.play(ShowCreation(code))
        self.play(ShowCreation(code_highlight))
