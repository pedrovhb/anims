from manimlib.imports import *


class Element:
    def __init__(self, val):
        self.val = val
        self.circle = Circle(radius=0.4)
        self.text = TextMobject(str(self.val))


to_sort_list = [6, 9, 2, 0, 7, 5, 4]
els = [Element(v) for v in to_sort_list]
els_dict = {el.val: el for el in els}
x_start = -len(els) / 2


def swap_elements(index_1: int, index_2: int, s: Scene):
    # Left element moves up, right element down
    # Swap X positions
    # Y positions go back to 0

    index_1, index_2 = min(index_1, index_2), max(index_1, index_2)
    if index_2 - index_1 == 1:
        Y_SHIFT = 0.5
    else:
        Y_SHIFT = 1

    pos_1 = [(-(len(els) / 2) + index_1), Y_SHIFT, 0]
    pos_2 = [(-(len(els) / 2) + index_2), -Y_SHIFT, 0]

    # Shift Y
    s.play(
        ApplyMethod(els[index_1].circle.move_to, pos_1),
        ApplyMethod(els[index_1].text.move_to, pos_1),
        ApplyMethod(els[index_2].circle.move_to, pos_2),
        ApplyMethod(els[index_2].text.move_to, pos_2),
    )

    # Move X
    pos_1[0], pos_2[0] = pos_2[0], pos_1[0]
    s.play(
        ApplyMethod(els[index_1].circle.move_to, pos_1),
        ApplyMethod(els[index_1].text.move_to, pos_1),
        ApplyMethod(els[index_2].circle.move_to, pos_2),
        ApplyMethod(els[index_2].text.move_to, pos_2),
    )

    # Unshift Y
    pos_1[1], pos_2[1] = 0, 0
    s.play(
        ApplyMethod(els[index_1].circle.move_to, pos_1),
        ApplyMethod(els[index_1].text.move_to, pos_1),
        ApplyMethod(els[index_2].circle.move_to, pos_2),
        ApplyMethod(els[index_2].text.move_to, pos_2),
    )


class Quicksort(Scene):
    def construct(self):

        self.camera.set_frame_height(self.camera.get_frame_height() * 0.95)
        self.camera.set_frame_width(self.camera.get_frame_width() * 0.95)

        def partition(arr, left, right):
            print("Partitioning", arr[left : right + 1], ", pivot:", arr[right])
            pivot = arr[right]

            # Highlight pivot by raising it and displaying text above it
            pivot_text = TextMobject("Pivot")
            pivot_el = els[right]

            def yellow_and_up(c: Mobject):
                c.shift(UP)
                c.set_color(YELLOW_C)
                return c

            self.play(
                ApplyFunction(yellow_and_up, pivot_el.circle),
                ApplyMethod(pivot_el.text.shift, UP),
            )
            pivot_text.next_to(pivot_el.circle, UP)
            self.play(Write(pivot_text))

            # Show "Partitioning around pivot" rect and text
            pap_rectangle = Rectangle(width=right - left, height=1, color=WHITE)
            pap_rectangle.move_to(
                midpoint(
                    els[left].circle.get_center(), els[right - 1].circle.get_center()
                )
            )
            pap_text = TextMobject("Partition around pivot")
            pap_text.next_to(pap_rectangle, DOWN)
            self.play(ShowCreation(pap_rectangle), ShowCreation(pap_text))

            # Fade out "Partitioning around pivot" text
            self.wait(1)
            self.play(FadeOut(pap_text))

            smaller_element_index = left

            # Show "looking at element" rectangle if there's more than one el to iterate upon
            if right - left > 1:
                looking_at_rect = Rectangle(width=1, height=1, color=WHITE)
                looking_at_rect.move_to(els[left].circle)
                self.play(ShowCreation(looking_at_rect))

            for i in range(left, right):
                print(arr)

                if arr[i] < pivot:
                    comparison_text = TexMobject(f"{arr[i]} < {pivot}")
                    comparison_text.set_y(-2)
                    self.play(Write(comparison_text), run_time=1)

                    # swap_elements plays swapping animations
                    swap_elements(i, smaller_element_index, self)

                    arr[smaller_element_index], arr[i] = (
                        arr[i],
                        arr[smaller_element_index],
                    )
                    els[smaller_element_index], els[i] = (
                        els[i],
                        els[smaller_element_index],
                    )
                    smaller_element_index += 1

                    self.play(FadeOut(comparison_text), run_time=1)

                # Shift "looking at rect" if it exists and it's not at the last position
                if right - left > 1 and i != right - 1:
                    self.play(ApplyMethod(looking_at_rect.shift, RIGHT), run_time=0.6)

            # Remove white "Partitioning around pivot" rect and "looking at" rect
            clear_pap_anims = [FadeOut(pap_rectangle)]
            if right - left > 1:
                clear_pap_anims.append(FadeOut(looking_at_rect))
            self.play(*clear_pap_anims)

            # Create and show "Smaller than pivot" rect
            show_sm_rect = smaller_element_index - left > 0
            sm_rectangle = Rectangle(
                width=smaller_element_index - left - 0.05, height=1, color=GREEN_C
            )
            sm_rectangle.move_to(
                midpoint(
                    els[left].circle.get_center(),
                    els[smaller_element_index - 1].circle.get_center(),
                )
            )
            sm_text = TextMobject("Smaller than pivot", color=GREEN_C)
            sm_text.next_to(sm_rectangle, UP)
            if show_sm_rect:
                self.play(ShowCreation(sm_rectangle), ShowCreation(sm_text))

            # Create and show "Larger than pivot" rect
            show_lg_rect = right - smaller_element_index > 0
            lg_rectangle = Rectangle(
                width=right - smaller_element_index - 0.05, height=1, color=BLUE_C
            )
            lg_rectangle.move_to(
                midpoint(
                    els[smaller_element_index].circle.get_center(),
                    els[right - 1].circle.get_center(),
                )
            )
            lg_text = TextMobject("Larger than pivot", color=BLUE_C)
            lg_text.next_to(lg_rectangle, DOWN)
            self.play(ShowCreation(lg_rectangle), ShowCreation(lg_text))

            self.wait(1)

            # Fade out smaller/larger/pivot text before swapping pivot
            clear_text_anims = [
                FadeOut(sm_text) if show_sm_rect else None,
                FadeOut(lg_text) if show_lg_rect else None,
                FadeOut(pivot_text),
            ]
            clear_text_anims = [an for an in clear_text_anims if an is not None]
            self.play(*clear_text_anims)

            # Swap pivot
            swap_elements(smaller_element_index, right, self)

            # Return to clear array state
            clear_anims = [
                FadeOut(sm_rectangle) if show_sm_rect else None,
                FadeOut(lg_rectangle) if show_lg_rect else None,
            ]

            # Remove None (anims that shouldn't be played)
            clear_anims = [an for an in clear_anims if an is not None]
            self.play(*clear_anims)

            arr[smaller_element_index], arr[right] = (
                arr[right],
                arr[smaller_element_index],
            )
            els[smaller_element_index], els[right] = (
                els[right],
                els[smaller_element_index],
            )

            return smaller_element_index

        def quicksort(arr, left=0, right=None):
            if right is None:
                right = len(arr) - 1
            if left < right:

                # Show "Quicksort" rectangle and fade
                q_rect = Rectangle(width=right - left + 1, height=1, color=YELLOW_C)
                q_rect.move_to(
                    midpoint(
                        els[left].circle.get_center(), els[right].circle.get_center()
                    )
                )
                q_text = TextMobject("Quicksort")
                q_text.next_to(q_rect, UP)
                self.play(ShowCreation(q_rect), Write(q_text))
                self.wait(1)
                self.play(FadeOut(q_rect), FadeOut(q_text))

                new_pivot_position = partition(arr, left, right)

                # Play animations of elements known to be in their sorted positions turning to green
                anims = []
                # If there's only one element to the left of the pivot, it's sorted
                if new_pivot_position - left == 1:
                    anims.append(ApplyMethod(els[left].circle.set_color, GREEN_C))
                # If there's only one element to the right of the pivot, it's sorted
                if right - new_pivot_position == 1:
                    anims.append(ApplyMethod(els[right].circle.set_color, GREEN_C))
                # New pivot position is known to be correct sorted order
                anims.append(
                    ApplyMethod(els[new_pivot_position].circle.set_color, GREEN_C)
                )
                self.play(*anims)

                quicksort(arr, left, new_pivot_position - 1)
                quicksort(arr, new_pivot_position + 1, right)

        # Move elements to their starting positions
        for i in range(len(els)):
            new_pos = [(-(len(els) / 2) + i), 0, 0]
            els[i].circle.move_to(new_pos)
            els[i].text.move_to(new_pos)

        # Show the creation of elements
        self.wait(0.5)
        self.play(
            *[ShowCreation(el.circle) for el in els], *[Write(el.text) for el in els]
        )

        quicksort(to_sort_list)

        self.wait(3)
