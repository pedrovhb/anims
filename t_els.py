from manim import *

from structures import AnimatedList


class MyScene(Scene):

    def construct(self):
        el = AnimatedList([1, 3, 4, 9])
        el.set_highlight_rect_no_anim(0, 1)

        self.play(ShowCreation(el.group))

        self.play(*el.swap_positions(0, 2))
        self.play(*el.swap_positions(0, 1))
        self.play(*el.set_highlight_rect(1, 2))
        self.play(*el.show_passing_flash(1, 2))
        self.play(*el.show_passing_flash(1))
        self.play(*el.set_highlight_rect(1, 1))
        self.play(*el.set_highlight_rect(3, 3))
        self.wait(2)
