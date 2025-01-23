from manim import *
import numpy as np

class ParallelAxesSameHeightDifferentScale(Scene):
    def construct(self):
        # ----------------------------------------------------------------------
        # 1) Kamera-indstillinger: så vi har plads til akserne og ticks.
        #    (Hvis 'self.camera.frame.set(...)' ikke virker i din version,
        #     kan du bruge self.camera.frame_width og self.camera.frame_height)
        # ----------------------------------------------------------------------
        self.camera.frame_width = 16
        self.camera.frame_height = 12
        self.camera.frame_center = ORIGIN

        # ----------------------------------------------------------------------
        # 2) Definér data-intervaller for venstre og højre akse.
        #    Venstre akse:  data fra -3 til  5
        #    Højre akse:    data fra -3 til 10
        #
        #    Visuelt vil begge akser dog kun fylde "scene-intervallet" -3 til +5
        #    i den lodrette retning. Så er de lige høje.
        # ----------------------------------------------------------------------
        left_data_min, left_data_max   = -3, 5
        right_data_min, right_data_max = -3, 10

        # Scene-interval (lodret) for BEGGE akser skal være ens,
        # så de bliver samme højde.
        scene_min, scene_max = -3, 5  # 8 "scene-enheder" i højden

        # Hjælpefunktion: lineær omskalering fra [A,B] -> [C,D]
        def map_range(value, data_min, data_max, scene_min, scene_max):
            """Lineært "map" value fra data-intervallet [data_min, data_max]
            til scene-intervallet [scene_min, scene_max]."""
            proportion = (value - data_min) / (data_max - data_min)
            return scene_min + proportion * (scene_max - scene_min)

        # ----------------------------------------------------------------------
        # 3) Tegn venstre akse (for x) og højre akse (for y) med samme fysiske højde
        # ----------------------------------------------------------------------
        # Venstre akse: i x = -6, fra scene_min til scene_max
        left_axis = Arrow(
            start=[-6, scene_min, 0],
            end=[-6, scene_max, 0],
            buff=0,
            color=WHITE
        )
        left_label = MathTex("x").next_to(left_axis.get_end(), UP, buff=0.2)

        # Højre akse: i x = +6, også fra scene_min til scene_max
        right_axis = Arrow(
            start=[6, scene_min, 0],
            end=[6, scene_max, 0],
            buff=0,
            color=WHITE
        )
        right_label = MathTex("y").next_to(right_axis.get_end(), UP, buff=0.2)

        self.play(
            Create(left_axis),
            Create(right_axis),
            Write(left_label),
            Write(right_label),
            run_time=2
        )

        # ----------------------------------------------------------------------
        # 4) Lav tick-marks til hver akse
        # ----------------------------------------------------------------------
        def create_vertical_ticks(
            x_coord,           # hvor aksen er placeret (typisk -6 eller +6)
            data_min, data_max,
            scene_min, scene_max,
            step=1,
            label_side=LEFT
        ):
            """Laver et sæt af lineære tick-marks i data-intervallet [data_min, data_max].
               De placeres dog i scene-intervallet [scene_min, scene_max].
               step er afstanden i data-enheder mellem ticks."""
            ticks = VGroup()
            for val in range(data_min, data_max+1, step):
                # 4a) Find scene-koordinat for val
                scene_y = map_range(val, data_min, data_max, scene_min, scene_max)

                # 4b) Selve tick-stregen
                tick = Line(
                    start=[x_coord - 0.2, scene_y, 0],
                    end=[x_coord + 0.2, scene_y, 0],
                    color=WHITE,
                    stroke_width=1
                )
                # 4c) Label
                label = MathTex(str(val)).scale(0.5)
                label.next_to(tick, label_side, buff=0.1)

                ticks.add(tick, label)
            return ticks

        # Venstre akse: ticks for x = -3..5, i trin på 1
        left_ticks = create_vertical_ticks(
            x_coord=-6,
            data_min=left_data_min,
            data_max=left_data_max,
            scene_min=scene_min,
            scene_max=scene_max,
            step=1,
            label_side=LEFT
        )

        # Højre akse: ticks for y = -3..10, i trin på 1
        right_ticks = create_vertical_ticks(
            x_coord=6,
            data_min=right_data_min,
            data_max=right_data_max,
            scene_min=scene_min,
            scene_max=scene_max,
            step=1,
            label_side=RIGHT
        )

        self.play(
            Create(left_ticks, lag_ratio=0.1),
            Create(right_ticks, lag_ratio=0.1),
            run_time=2
        )

        # ----------------------------------------------------------------------
        # 5) Funktionstekst i midten
        # ----------------------------------------------------------------------
        func_text = MathTex("").scale(1.2).move_to([0,0,0])  # centralt
        self.add(func_text)  # Et tomt MathTex, som vi kan udskifte undervejs

        # ----------------------------------------------------------------------
        # 6) Vi vil vise x -> f(x) for x=1,3,-1 og for tre funktioner
        # ----------------------------------------------------------------------
        x_vals = [1, 3, -1]
        functions = [
            (lambda x: x,      "f(x) = x",    BLUE),
            (lambda x: np.log(x+2)+1,   "g(x) = log(x+2)+1",  YELLOW),
            (lambda x: 2*x-1,  "h(x) = 2x - 1", GREEN),
        ]

        # Hjælpefunktioner til at placere punkter på hver akse
        # Bemærk, at vi nu oversætter x_value og y_value fra "data" til "scene".
        def left_line_point(x_value):
            # Placeres ved x=-6, men scene_y findes via map_range
            scene_y = map_range(
                x_value, left_data_min, left_data_max,
                scene_min, scene_max
            )
            return np.array([-6, scene_y, 0])

        def right_line_point(y_value):
            # Placeres ved x=+6, men scene_y findes via map_range
            scene_y = map_range(
                y_value, right_data_min, right_data_max,
                scene_min, scene_max
            )
            return np.array([6, scene_y, 0])

        # ----------------------------------------------------------------------
        # 7) Gå igennem funktioner og x‐værdier, og animer
        # ----------------------------------------------------------------------
        for func, label_str, color in functions:
            # Skift funktionstekst
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

                # Buet pil fra x_dot til y_dot
                arrow = CurvedArrow(
                    start_point=x_dot.get_center(),
                    end_point=y_dot.get_center(),
                    color=color,
                    angle=-TAU/4  # let bue nedad
                )

                # Animer
                self.play(FadeIn(x_dot), Write(x_label_num))
                self.play(Create(arrow), FadeIn(y_dot), Write(y_label_num))
                self.wait(0.5)

                # Ryd op igen
                self.play(
                    FadeOut(arrow),
                    FadeOut(x_dot), FadeOut(x_label_num),
                    FadeOut(y_dot), FadeOut(y_label_num)
                )

        self.wait(2)
