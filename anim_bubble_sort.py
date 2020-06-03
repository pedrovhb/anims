from manim import *

from render_code import RenderedCodeWithHighlight, VariablesTracker
from structures import AnimatedList

VAR_i = "i"
VAR_swapped = "swapped"
VAR_shuffled_array = "shuffled_array"


class BubbleSort(Scene):
    CONFIG = {"camera_config": {"background_color": "#243040"}, "run_time": 0.1}

    def construct(self):
        file_path = os.path.join(os.getcwd(), "bubble_sort.py")
        code = RenderedCodeWithHighlight.from_file(file_path, scale=0.15)
        code.group.shift(UP * 12.3)
        code.group.shift(LEFT * 1)

        variables = VariablesTracker()

        self.bring_to_back(variables.highlight_rect)
        self.play(ShowCreation(variables.group))

        self.bring_to_back(code.highlight_rect)
        self.play(ShowIncreasingSubsets(code.group))

        self.play(code.animate_highlight_line(1))

        shuffled_arr = [4, 5, 0, 2, 6, 7, 9]
        self.play(code.animate_highlight_line(1))
        self.play(*variables.update_variable(self, VAR_shuffled_array, [4, 5, 0, 2, 6, 7, 9]))

        el_list = AnimatedList([1, 3, 4, 9])
        self.play(ShowCreation(el_list.group))

        while True:
            self.play(code.animate_highlight_line(3))

            swapped = False
            self.play(code.animate_highlight_line(4))
            self.play(*variables.update_variable(self, VAR_swapped, swapped))

            for i in range(len(shuffled_arr) - 1):
                self.play(code.animate_highlight_line(6))
                self.play(*variables.update_variable(self, VAR_i, i))

                self.play(code.animate_highlight_line(7))
                if shuffled_arr[i] < shuffled_arr[i + 1]:
                    swapped = True
                    self.play(code.animate_highlight_line(8))
                    self.play(*variables.update_variable(self, VAR_swapped, swapped))

                    shuffled_arr[i], shuffled_arr[i + 1] = shuffled_arr[i + 1], shuffled_arr[i]
                    self.play(code.animate_highlight_line(9))
                    self.play(*variables.update_variable(self, VAR_shuffled_array, shuffled_arr))

                return

            self.play(code.animate_highlight_line(11))
            if not swapped:
                self.play(code.animate_highlight_line(12))
                break
            return

        self.wait(2)
