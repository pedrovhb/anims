from manim.imports import *

from render_code import RenderedCodeWithHighlight, VariablesTracker


# class VarTracker:
#     def __init__(self, var_name, var_val):
#         self.var_name = var_name
#         self.var_val = var_val
#         self.mobject = TextMobject(self.as_text)
#
#     def update_val(self, new_val):
#         self.var_val = new_val
#         # self.mobject
#
#     @property
#     def as_text(self):
#         return f"{self.var_name} = {self.var_val}"


class BubbleSort(Scene):
    CONFIG = {"camera_config": {"background_color": "#243040"}}

    def construct(self):

        file_path = os.path.join(os.getcwd(), "bubble_sort.py")
        code = RenderedCodeWithHighlight.from_file(file_path, scale=0.15)
        code.group.shift(UP * 12.3)
        code.group.shift(LEFT * 1)

        variables = VariablesTracker({"a": "b", "c": "d"})
        self.play(ShowCreation(variables.group))

        self.play(ShowIncreasingSubsets(code.group))
        self.bring_to_back(code.highlight_rect)

        self.play(code.animate_highlight_line(4))
        self.play(code.animate_highlight_line(6))
