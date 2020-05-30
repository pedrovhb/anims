from manim import *


class ListElement:

    def __init__(self, value):
        self.value = value
        self.circle = Circle(radius=0.5)
        self.text = TextMobject(str(self.value))
        self.vgroup = VGroup(self.circle, self.text)
