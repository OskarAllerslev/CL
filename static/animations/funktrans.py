from manim import *

class ParallelAxesFunction(Scene):
    def construct(self):
        # Konfigurer baggrund
        self.camera.background_color = BLACK

        # Opret parallelle akser
        x_axis = NumberLine(
            x_range=[-2, 3, 1],
            length=6,
            color=WHITE,
            include_numbers=True
        ).shift(LEFT*3)

        y_axis = NumberLine(
            x_range=[-5, 10, 2],
            length=6,
            color=WHITE,
            include_numbers=True,
            label_direction=LEFT
        ).shift(RIGHT*3).rotate(PI/2)

        # Tilføj etiketter
        x_label = Text("X-akse").next_to(x_axis, DOWN)
        y_label = Text("Y-akse").next_to(y_axis, RIGHT)

        # Fælles elementer
        title = Text("Funktionstransformation", font_size=32).to_edge(UP)
        self.play(Write(title))
        
        # Vis akser
        self.play(
            Create(x_axis),
            Create(y_axis),
            Write(x_label),
            Write(y_label),
            run_time=2
        )
        self.wait(1)

        # Funktioner og punkter
        functions = [
            (lambda x: x, "f(x) = x", [-2, 1, 3], BLUE),
            (lambda x: x**2, "f(x) = x²", [-2, 1, 3], GREEN),
            (lambda x: 2*x-1, "f(x) = 2x-1", [-2, 1, 3], RED)
        ]

        for func, label, x_vals, color in functions:
            func_title = Text(label, font_size=24, color=color).to_edge(UP + RIGHT)
            self.play(Write(func_title))
            
            for x in x_vals:
                # X-punkt
                x_point = x_axis.n2p(x)
                x_dot = Dot(x_point, color=color)
                x_text = MathTex(f"x = {x}", color=color).next_to(x_dot, DOWN)

                # Y-punkt
                y = func(x)
                y_point = y_axis.n2p(y) + RIGHT*3
                y_dot = Dot(y_point, color=color)
                y_text = MathTex(f"f({x}) = {y}", color=color).next_to(y_dot, RIGHT)

                # Pil animation
                arrow = CurvedArrow(
                    x_point,
                    y_point,
                    color=color,
                    angle=-TAU/4,
                    tip_length=0.2
                )

                # Animationsekvens
                self.play(
                    FadeIn(x_dot),
                    Write(x_text),
                    run_time=0.5
                )
                self.play(
                    Create(arrow),
                    FadeIn(y_dot),
                    Write(y_text),
                    run_time=1.5
                )
                self.wait(1)
                
                # Fjern elementer
                self.play(
                    FadeOut(x_dot),
                    FadeOut(x_text),
                    FadeOut(arrow),
                    FadeOut(y_dot),
                    FadeOut(y_text)
                )
            
            self.play(FadeOut(func_title))

        self.wait(2)