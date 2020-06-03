from manim import *

from structures import ListElement, AnimatedList


class MyScene(Scene):

    def construct(self):
        el = AnimatedList([1, 3, 4, 9])

        self.play(ShowCreation(el.group))
        self.play(*el.swap_positions(0, 2))
        self.play(*el.swap_positions(1, 2))
        self.wait(2)
