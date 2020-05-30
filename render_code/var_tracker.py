from typing import Optional

from manim import *

from render_code import RenderedCodeWithHighlight


class VariablesTracker(RenderedCodeWithHighlight):
    def __init__(self, variables: Optional[dict] = None, font_size=48, image_pad=12, scale=0.15):
        self.variables = variables or {}
        code = ""
        for var in self.variables:
            code += self._text_for_var(var) + "\n"
        code += "\n" * 3  # hacky way to make slots for undeclared vars

        super().__init__(
            code,
            font_size=font_size,
            image_pad=image_pad,
            scale=scale,
            use_line_numbers=False,
        )

        self.highlight_rect.set_opacity(0)

    def _text_for_var(self, var_name):
        var_value = self.variables[var_name]
        return f"{var_name} = {var_value}"

    def update_variable(self, scene, variable, new_val):
        self.variables[variable] = new_val
        variable_index = list(self.variables).index(variable)

        old_mobject = self.line_mobjects[variable_index]

        line_text = self._text_for_var(variable)
        rendered_file = self._render_line(line_text)

        new_mobject = ImageMobject(rendered_file)
        new_mobject.scale(self.scale)
        new_mobject.align_to(old_mobject, DOWN)
        new_mobject.align_to(self.group, LEFT)
        self.line_mobjects[variable_index] = new_mobject

        self.highlight_rect.set_opacity(1)
        self.highlight_rect.set_width(
            max(old_mobject.get_width(), new_mobject.get_width()), stretch=True
        )
        self.highlight_rect.align_to(new_mobject, LEFT)
        self.highlight_rect.align_to(new_mobject, DOWN)
        scene.bring_to_back(self.highlight_rect)

        anims = [
            VFadeInThenOut(self.highlight_rect),
            FadeOut(old_mobject),
            FadeIn(new_mobject),
        ]

        return anims
