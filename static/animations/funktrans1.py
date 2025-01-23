from manim import *

class ParallelAxesMappingImproved(Scene):
    def construct(self):
        # Juster kameraets ramme
        self.camera.frame_width = 16  # Bredere ramme
        self.camera.frame_height = 20 # Højere ramme
        self.camera.frame_center = ORIGIN

        # Lodret "x-linje" til venstre: fra y=-3 til y=5
        left_axis = Arrow(
            start= [-6, -3, 0],
            end=   [-6, 5, 0],
            buff=0,
            color=WHITE,
            stroke_width=2
        )
        left_label = MathTex("x").next_to(left_axis.get_end(), UP, buff=0.2)

        # Lodret "y-linje" til højre: fra y=-3 til y=15
        right_axis = Arrow(
            start= [6, -3, 0],
            end=   [6, 15, 0],
            buff=0,
            color=WHITE,
            stroke_width=2
        )
        right_label = MathTex("y").next_to(right_axis.get_end(), UP, buff=0.2)

        self.play(
            Create(left_axis), 
            Create(right_axis),
            Write(left_label),
            Write(right_label),
            run_time=2
        )

        # Forbedrede ticks på y-aksen
        def create_ticks(axis_x, y_start, y_end, step, direction):
            ticks = VGroup()
            for y in np.arange(y_start, y_end + step, step):
                tick = Line(
                    start=[axis_x - 0.2, y, 0],
                    end=[axis_x + 0.2, y, 0],
                    color=WHITE,
                    stroke_width=1
                )
                label = MathTex(str(int(y))).scale(0.5).next_to(tick, direction, buff=0.1)
                ticks.add(tick, label)
            return ticks

        left_ticks = create_ticks(-6, -2, 4, 1, LEFT)
        right_ticks = create_ticks(6, -2, 14, 2, RIGHT)  # Ticks hver 2. enhed

        self.play(
            Create(left_ticks, lag_ratio=0.1),
            Create(right_ticks, lag_ratio=0.1),
            run_time=2
        )

        # Funktionstekst i midten
        func_text = MathTex("").scale(1.2).move_to([0,3,0])
        self.add(func_text)

        # Ticks på venstre "x-linje"
        left_ticks = VGroup()
        for val in range(-2, 5):
            tick_length = 0.15
            tick_start = np.array([-5 - tick_length, val, 0])
            tick_end   = np.array([-5 + tick_length, val, 0])
            tick = Line(tick_start, tick_end, color=WHITE)
            label = MathTex(str(val)).scale(0.5).next_to(tick, LEFT, buff=0.1)
            if val != 4:
                left_ticks.add(tick, label)

        # Ticks på højre "y-linje"
        right_ticks = VGroup()
        for val in range(-2, 11):
            tick_length = 0.15
            tick_start = np.array([5 - tick_length, val, 0])
            tick_end   = np.array([5 + tick_length, val, 0])
            tick = Line(tick_start, tick_end, color=WHITE)
            label = MathTex(str(val)).scale(0.5).next_to(tick, RIGHT, buff=0.1)
            if val != 10:
                right_ticks.add(tick, label)

        self.play(Create(left_ticks), Create(right_ticks))

        x_vals = [1, 3, -1]
        functions = [
            (lambda x: x,        "f(x) = x",      BLUE),
            (lambda x: x**2,     "g(x) = x^2",    YELLOW),
            (lambda x: 2*x - 1,  "h(x) = 2x - 1", GREEN),
        ]

        def left_line_point(x_value):
            return [-5, x_value, 0]

        def right_line_point(y_value):
            return [5, y_value, 0]

        for func, label_str, color in functions:
            new_text = MathTex(label_str).scale(1.2).set_color(color)
            new_text.move_to(func_text.get_center())
            self.play(Transform(func_text, new_text))
            self.wait(0.5)

            for x_val in x_vals:
                y_val = func(x_val)
                x_dot = Dot(left_line_point(x_val), color=color)
                x_label_num = MathTex(str(x_val)).scale(0.7)
                x_label_num.next_to(x_dot, LEFT, buff=0.15)

                y_dot = Dot(right_line_point(y_val), color=color)
                y_label_num = MathTex(str(y_val)).scale(0.7)
                y_label_num.next_to(y_dot, RIGHT, buff=0.15)

                arrow = CurvedArrow(
                    start_point=x_dot.get_center(),
                    end_point=y_dot.get_center(),
                    color=color,
                    angle=-TAU/4
                )

                self.play(FadeIn(x_dot), Write(x_label_num))
                self.play(Create(arrow), FadeIn(y_dot), Write(y_label_num))
                self.wait(0.5)

                self.play(
                    FadeOut(arrow),
                    FadeOut(x_dot), FadeOut(x_label_num),
                    FadeOut(y_dot), FadeOut(y_label_num)
                )

        self.wait(2)
