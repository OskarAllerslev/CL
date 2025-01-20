from manim import *

class IntegrateOverSphere(ThreeDScene):
    def construct(self):

        self.camera.background_color =BLACK
        # Opret en tredimensionel akse
        axes = ThreeDAxes()
        self.set_camera_orientation(phi=75 * DEGREES, theta=-45 * DEGREES)

        # Opret en kugle (enhedssfære)
        sphere = Surface(
            lambda u, v: np.array([
                np.cos(u) * np.sin(v),
                np.sin(u) * np.sin(v),
                np.cos(v)
            ]),
            u_range=[0, TAU],
            v_range=[0, PI],
            resolution=(20, 20)
        )
        sphere.set_fill(BLUE, opacity=0.5)

        # Først: Integration over x-aksen
        self.play(Create(axes))
        self.play(Create(sphere))
        self.wait(1)

        # Vis integration over x-aksen
        x_slice = Surface(
            lambda u, v: np.array([
                u,
                np.sin(v),
                np.cos(v)
            ]),
            u_range=[-1, 1],
            v_range=[0, PI],
            resolution=(20, 20)
        )
        x_slice.set_fill(RED, opacity=0.5)
        self.play(Create(x_slice))
        self.wait(1)

        # Derefter: Integration over y-aksen
        y_slice = Surface(
            lambda u, v: np.array([
                np.sin(u),
                v,
                np.cos(u)
            ]),
            u_range=[0, PI],
            v_range=[-1, 1],
            resolution=(20, 20)
        )
        y_slice.set_fill(GREEN, opacity=0.5)
        self.play(Create(y_slice))
        self.wait(1)

        # Til sidst: Integration over både x- og y-aksen
        self.play(FadeOut(x_slice), FadeOut(y_slice))
        self.wait(1)