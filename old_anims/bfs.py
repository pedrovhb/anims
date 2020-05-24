from collections import deque
from manimlib.imports import *


class Node:
    def __init__(self, val):
        self.val = val
        self.circle = Circle(radius=0.4)
        self.circle.set_fill(BLACK, 1)
        self.text = TextMobject(str(self.val))
        self.left = None
        self.right = None

    def move_to(self, *args, **kwargs):
        self.circle.move_to(*args, **kwargs)
        self.text.move_to(*args, **kwargs)


# Create tree nodes
nodes = {v: Node(v) for v in [0, 2, 3, 4, 5, 6, 7, 9]}

# Link them together
root = nodes[5]
root.left = nodes[2]
root.left.left = nodes[0]
root.left.right = nodes[4]
root.left.right.left = nodes[3]
root.right = nodes[7]
root.right.left = nodes[6]
root.right.right = nodes[9]


class BFS(Scene):
    def construct(self):

        # Set up camera position and zoom out a bit
        self.camera.set_frame_center(DOWN + LEFT * 0.5)
        self.camera.set_frame_height(self.camera.get_frame_height() * 1.1)
        self.camera.set_frame_width(self.camera.get_frame_width() * 1.1)

        # Set up tree node positions
        nodes[5].move_to(UP * 2 + LEFT * 2.5)

        nodes[2].move_to(UP * 1 + LEFT * 4.5)
        nodes[7].move_to(UP * 1 + LEFT * 0.5)

        nodes[0].move_to(LEFT * 5.5)
        nodes[4].move_to(LEFT * 3.5)
        nodes[6].move_to(LEFT * 1.5)
        nodes[9].move_to(RIGHT * 0.5)

        nodes[3].move_to(DOWN * 1 + LEFT * 4.5)

        # Set up lines between nodes
        edges = [(5, 2), (5, 7), (2, 0), (2, 4), (4, 3), (7, 9), (7, 6)]
        lines = {
            (a, b): Line(nodes[a].circle.get_center(), nodes[b].circle.get_center())
            for (a, b) in edges
        }

        # Make a copy of the nodes to use them in queue/visited nodes
        queue_nodes = {k: deepcopy(v) for k, v in nodes.items()}

        # Animate line and element creations
        self.play(*[ShowCreation(a) for a in lines.values()])
        self.play(
            *[ShowCreation(n.circle) for n in nodes.values()],
            *[ShowCreation(n.text) for n in nodes.values()]
        )

        # Create "Visited nodes" rectangles and text
        visited_rectangles = [
            Rectangle(width=1, height=1, color=GRAY) for _ in range(len(nodes))
        ]
        for i, vr in enumerate(visited_rectangles):
            vr.move_to(LEFT * 6 + 3.5 * DOWN + RIGHT * i)
        visited_text = TextMobject("Visited nodes")
        visited_text.next_to(visited_rectangles[0], UP)
        visited_text.align_to(visited_rectangles[0], LEFT)
        self.play(*[ShowCreation(vr) for vr in visited_rectangles])
        self.play(Write(visited_text))

        # Create "Queue" and "Current node" rectangles and text
        queue_end = DOWN * 2.5 + RIGHT * 4
        queue_rectangles = [Rectangle(width=1, height=1, color=GRAY) for _ in range(6)]
        queue_rectangles[0].set_color(WHITE)
        for i, qr in enumerate(queue_rectangles):
            qr.move_to(queue_end + UP * (i - 1))
        queue_rectangles.pop(1)
        queue_text = TextMobject("Queue")
        crt_node_text = TextMobject("Current node")
        queue_text.next_to(queue_rectangles[-1], UP)
        queue_text.align_to(visited_rectangles[-1], ORIGIN)

        crt_node_text.next_to(queue_rectangles[0], DOWN)
        crt_node_text.align_to(visited_rectangles[0], ORIGIN)

        self.play(*[ShowCreation(qr) for qr in queue_rectangles[1:]])
        self.play(Write(queue_text))

        self.play(ShowCreation(queue_rectangles[0]))
        self.play(Write(crt_node_text))

        queue = deque()
        visited_nodes = []

        # Adds a node to the queue and animates it
        def add_node_to_queue(node):
            queue_nodes[node.val].move_to(queue_end + UP * (len(queue) + 1))
            queue.append(node)
            self.play(
                FadeInFrom(queue_nodes[node.val].circle, UP),
                FadeInFrom(queue_nodes[node.val].text, UP),
            )

        # Traverse, adding left and right children to queue
        def bfs_helper(node):
            nonlocal queue

            if node.left:
                self.play(
                    ApplyMethod(lines[(node.val, node.left.val)].set_stroke, YELLOW_C),
                    WiggleOutThenIn(node.left.circle),
                )
                add_node_to_queue(node.left)
                self.play(
                    ApplyMethod(lines[(node.val, node.left.val)].set_stroke, WHITE)
                )

            if node.right:
                self.play(
                    ApplyMethod(lines[(node.val, node.right.val)].set_stroke, YELLOW_C),
                    WiggleOutThenIn(node.right.circle),
                )
                add_node_to_queue(node.right)
                self.play(
                    ApplyMethod(lines[(node.val, node.right.val)].set_stroke, WHITE)
                )

        # Initially, only the root is added
        add_node_to_queue(nodes[5])

        # While the queue is not empty, apply BFS helper and perform the necessary animations
        while queue:
            crt_node = queue.popleft()

            # Animate queue/current node movement
            self.play(
                ApplyMethod(queue_nodes[crt_node.val].circle.shift, 2 * DOWN),
                ApplyMethod(queue_nodes[crt_node.val].text.shift, 2 * DOWN),
                *[
                    ApplyMethod(queue_nodes[v].circle.shift, DOWN)
                    for v in [n.val for n in queue]
                ],
                *[
                    ApplyMethod(queue_nodes[v].text.shift, DOWN)
                    for v in [n.val for n in queue]
                ]
            )

            # Set current node color to yellow both in queue and tree
            self.play(
                ApplyMethod(nodes[crt_node.val].circle.set_stroke, YELLOW_C),
                ApplyMethod(queue_nodes[crt_node.val].circle.set_stroke, YELLOW_C),
            )

            # Indicate current node both in queue and tree
            self.play(
                Indicate(queue_nodes[crt_node.val].text),
                Indicate(nodes[crt_node.val].text),
                WiggleOutThenIn(nodes[crt_node.val].circle),
                WiggleOutThenIn(queue_nodes[crt_node.val].circle),
            )

            bfs_helper(crt_node)

            # Add node to visited nodes list
            visited_nodes.append(queue_nodes[crt_node.val])

            def move_and_greenify(c: Circle):
                c.shift(LEFT * (11 - len(visited_nodes)))
                c.set_stroke(GREEN_C)
                return c

            # Animate shift from current node to visited nodes
            self.play(
                ApplyFunction(move_and_greenify, queue_nodes[crt_node.val].circle),
                ApplyMethod(
                    queue_nodes[crt_node.val].text.shift,
                    LEFT * (11 - len(visited_nodes)),
                ),
                ApplyMethod(nodes[crt_node.val].circle.set_stroke, GREEN_C),
            )

        self.wait(4)
