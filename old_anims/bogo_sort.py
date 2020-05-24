from manimlib.imports import *


class Element:
    def __init__(self, val):
        self.val = val
        self.circle = Circle(radius=0.4)
        self.text = TextMobject(str(self.val))


class BogoSort(Scene):
    def construct(self):
        shuffled_arr = [4, 2, 0, 6, 9, 5, 7]
        els = [Element(n) for n in shuffled_arr]

        self.wait(1)

        # Move elements to their starting positions
        start_x = -len(els) / 2
        for i in range(len(els)):
            new_pos = [start_x + i, 0, 0]
            els[i].circle.move_to(new_pos)
            els[i].text.move_to(new_pos)
        self.play(
            *[ShowCreation(el.circle) for el in els], *[Write(el.text) for el in els]
        )

        self.wait(0.5)

        possible_heights = [start_x + i for i in range(len(shuffled_arr))]
        random.shuffle(possible_heights)
        self.play(
            *[
                ApplyMethod(el.circle.set_y, possible_heights[i])
                for i, el in enumerate(els)
            ],
            *[
                ApplyMethod(el.text.set_y, possible_heights[i])
                for i, el in enumerate(els)
            ]
        )

        sorted_arr = list(sorted(shuffled_arr))
        els_dict = {el.val: el for el in els}
        self.play(
            *[
                ApplyMethod(els_dict[val].circle.set_x, start_x + i)
                for i, val in enumerate(sorted_arr)
            ],
            *[
                ApplyMethod(els_dict[val].text.set_x, start_x + i)
                for i, val in enumerate(sorted_arr)
            ]
        )

        self.play(
            *[ApplyMethod(el.circle.set_y, 0) for el in els],
            *[ApplyMethod(el.text.set_y, 0) for el in els]
        )

        self.play(*[ApplyMethod(el.circle.set_color, GREEN_C) for el in els])
        self.wait(4)
