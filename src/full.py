from manim import *
from manim.utils.color import DVIPSNAMES
import numpy as np
from missingcolors import *

class BezierCurvePresentation(MovingCameraScene):
    def construct(self):
        # Title Scene
        self.title_scene()
        
        # Scene 1: Bezier Curve with Slider
        self.scene1_bezier_with_slider()
        
        # Scene 2: 4x4 Parameterized Curves Grid
        self.scene2_parameterized_grid()
        
        # Scene 3: Bezier Transformations
        self.scene3_bezier_transformations()
    
    def title_scene(self):
        # Title
        title = Text("Bezier Curves", font_size=72, color=BLUE)
        title.move_to(ORIGIN)
        
        self.play(Write(title))
        self.wait(3)
        self.play(FadeOut(title))
    
    def scene1_bezier_with_slider(self):
        # Control points for a wiggly Bezier curve
        control_points = [
            np.array([-4, -2, 0]),
            np.array([-2, 3, 0]),
            np.array([2, -1, 0]),
            np.array([4, 2, 0])
        ]
        
        # Show C(t)
        c_t = MathTex("C(t)", font_size=48, color=YELLOW)
        c_t.move_to(ORIGIN)
        self.play(Write(c_t))
        self.wait(0.5)
        
        # Move C(t) to left side
        self.play(c_t.animate.to_edge(LEFT).shift(UP))
        
        # Create grid
        grid = NumberPlane(
            x_range=[-5, 5, 1],
            y_range=[-3, 3, 1],
            background_line_style={
                "stroke_color": GRAY,
                "stroke_width": 1,
                "stroke_opacity": 0.3
            }
        )
        self.play(FadeIn(grid, shift=DOWN), run_time=1)
        
        # Draw control polygon
        # polygon = Polygon(*control_points, color=BLUE, stroke_opacity=0.5)
        dots = VGroup(*[Dot(p, color=RED) for p in control_points])
        self.play(Create(dots))
        
        # Create wiggly Bezier curve with animation
        curve = self.create_bezier_curve(control_points, color=YELLOW)
        
        # Create slider
        slider = self.create_slider()
        slider.to_edge(DOWN, buff=0.5)
        
        # Create t value label
        t_label = MathTex("t = 0.00", font_size=24, color=WHITE)
        t_label.next_to(slider, UP, buff=0.2)
        
        self.play(FadeIn(slider), Write(t_label))

        self.wait(2)
        
        # Animate curve drawing with slider movement
        final_curve = self.animate_curve_with_slider(curve, slider, t_label, control_points)
        
        self.wait(1)
        
        # Fade everything out
        self.play(*[FadeOut(mob) for mob in [c_t, grid, dots, curve, slider, t_label, final_curve]])
    
    def scene2_parameterized_grid(self):
        # Create 4x4 grid
        grid = self.create_4x4_grid()
        
        # Create names for parameterized curves
        curve_names = VGroup()
        equations = [
            r"y = x^2",                    # Parabola
            r"\frac{x^2}{a^2} + \frac{y^2}{b^2} = 1",  # Ellipse
            r"x^2 + y^2 = r^2",            # Circle
            r"\frac{x^2}{a^2} - \frac{y^2}{b^2} = 1",  # Hyperbola
            r"x = \cosh t, y = \sinh t",   # Hyperbolic
            r"x = t^2, y = t",              # Parabola (parametric)
            r"r = a + b\cos\theta",         # Limacon
            r"x = a\cos^3 t, y = a\sin^3 t", # Astroid
            r"x = \cos t, y = \sin 2t",      # Lissajous
            r"r = a\theta",                  # Archimedean spiral
            r"x = \sec t, y = \tan t",       # Hyperbola (parametric)
            r"x = \cos^3 t, y = \sin^3 t",   # Astroid (parametric)
            r"x = t\sin t, y = t\cos t",     # Spiral
            r"x = e^t\cos t, y = e^t\sin t", # Logarithmic spiral
            r"x = \cosh t, y = \sinh t",     # Hyperbola
            r"x = \cos 2t, y = \sin 3t"      # Lissajous
        ]
        
        colors = [YELLOW, GREEN, BLUE, RED, PURPLE, ORANGE, PINK, TEAL, 
                  MAROON, GOLD, LIME, CYAN, MAGENTA, BROWN, DARK_BLUE, LIGHT_BROWN]
        
        # Position names in grid cells
        positions = self.get_grid_positions(4, 4)
        
        for i, (pos, eq, color) in enumerate(zip(positions, equations, colors)):
            name = MathTex(eq, font_size=16, color=color)
            name.move_to(pos)
            curve_names.add(name)
        
        # Fade in names
        self.play(LaggedStart(*[FadeIn(name, scale=0.5) for name in curve_names], lag_ratio=0.1))
        self.wait(3)
        
        # Fade out names
        self.play(FadeOut(curve_names))
        
        # Create curves in grid
        curves = VGroup()
        for i, (pos, eq, color) in enumerate(zip(positions, equations, colors)):
            # Create axes for this cell
            axes = Axes(
                x_range=[-1.5, 1.5, 1],
                y_range=[-1.5, 1.5, 1],
                x_length=1.2,
                y_length=1.2,
                axis_config={"color": GRAY, "stroke_width": 0.5, "include_tip": False}
            )
            axes.move_to(pos)
            
            # Create a simple curve for each type (simplified for visualization)
            if i % 4 == 0:  # Parabola-like
                curve = axes.plot(lambda x: x**2, x_range=[-1, 1], color=color)
            elif i % 4 == 1:  # Ellipse-like
                curve = axes.plot_parametric_curve(
                    lambda t: [1.2*np.cos(t), 0.8*np.sin(t), 0],
                    t_range=[0, 2*PI],
                    color=color
                )
            elif i % 4 == 2:  # Circle-like
                curve = axes.plot_parametric_curve(
                    lambda t: [np.cos(t), np.sin(t), 0],
                    t_range=[0, 2*PI],
                    color=color
                )
            else:  # Hyperbola-like
                curve_right = axes.plot_parametric_curve(
                    lambda t: [1.2*np.cosh(t/1.5), np.sinh(t/1.5), 0],
                    t_range=[-1.5, 1.5],
                    color=color
                )
                curve_left = axes.plot_parametric_curve(
                    lambda t: [-1.2*np.cosh(t/1.5), np.sinh(t/1.5), 0],
                    t_range=[-1.5, 1.5],
                    color=color
                )
                curve = VGroup(curve_right, curve_left)
            
            curves.add(axes, curve)
        
        # Fade in grid and curves
        self.play(
            FadeIn(grid),
            *[Create(curve) for curve in curves if isinstance(curve, VMobject)],
            run_time=2
        )
        self.wait(2)
        
        # Fade out everything
        self.play(FadeOut(VGroup(grid, curves)))
    
    def scene3_bezier_transformations(self):
        # Show C(t)
        c_t = MathTex("C(t)", font_size=48, color=YELLOW)
        c_t.move_to(ORIGIN)
        self.play(Write(c_t))
        self.wait(0.5)
        
        # Shift leftward
        self.play(c_t.animate.shift(LEFT * 3))
        
        # Generalized Bezier equation
        bezier_eq = MathTex(
            r"C(t) = \sum_{i=0}^{n} P_i B_{i,n}(t)",
            font_size=36,
            color=BLUE
        )
        bezier_eq.next_to(c_t, RIGHT, buff=1)
        bezier_eq.shift(UP * 0.5)
        
        bernstein = MathTex(
            r"B_{i,n}(t) = \binom{n}{i} t^i (1-t)^{n-i}",
            font_size=30,
            color=GREEN
        )
        bernstein.next_to(bezier_eq, DOWN, buff=0.5)
        bernstein.shift(RIGHT * 0.5)
        
        self.play(
            Write(bezier_eq),
            Write(bernstein)
        )
        self.wait(4)
        
        # Transform to matrix representation
        matrix_intro = MathTex(
            r"C(t) = \mathbf{T} \cdot \mathbf{M} \cdot \mathbf{P}",
            font_size=42,
            color=ORANGE
        )
        matrix_intro.move_to(bezier_eq)
        
        self.play(
            Transform(bezier_eq, matrix_intro),
            FadeOut(bernstein)
        )
        self.wait(4)
        
        # Show full matrix form for cubic (n=3)
        matrix_full = MathTex(
            r"C(t) = \begin{bmatrix} 1 & t & t^2 & t^3 \end{bmatrix}",
            r"\begin{bmatrix} 1 & 0 & 0 & 0 \\ -3 & 3 & 0 & 0 \\ 3 & -6 & 3 & 0 \\ -1 & 3 & -3 & 1 \end{bmatrix}",
            r"\begin{bmatrix} P_0 \\ P_1 \\ P_2 \\ P_3 \end{bmatrix}",
            font_size=30
        )
        matrix_full.arrange(RIGHT, buff=0.3)
        matrix_full.next_to(c_t, RIGHT, buff=1)
        matrix_full.shift(UP * 0.5)
        
        self.play(
            Transform(bezier_eq, matrix_full),
            FadeOut(matrix_intro)
        )
        self.wait(4)
        
        # Generalize to n dimensions
        general_matrix = MathTex(
            r"C(t) = \begin{bmatrix} 1 & t & t^2 & \cdots & t^n \end{bmatrix}",
            r"\mathbf{M}_n",
            r"\begin{bmatrix} P_0 \\ P_1 \\ \vdots \\ P_n \end{bmatrix}",
            font_size=30
        )
        general_matrix.arrange(RIGHT, buff=0.3)
        general_matrix.next_to(c_t, RIGHT, buff=1)
        
        m_explanation = Text(
            "M_n is the (n+1)×(n+1) Bezier basis matrix",
            font_size=20,
            color=GRAY
        )
        m_explanation.next_to(general_matrix, DOWN, buff=0.5)
        
        self.play(
            Transform(bezier_eq, general_matrix),
            FadeIn(m_explanation)
        )
        self.wait(4)
        
        # Fade out everything
        self.play(*[FadeOut(mob) for mob in [c_t, bezier_eq, m_explanation]])
    
    # Helper functions
    def create_bezier_curve(self, control_points, color=YELLOW):
        """Create a cubic Bezier curve"""
        def bezier_point(t):
            b0 = (1-t)**3
            b1 = 3*(1-t)**2*t
            b2 = 3*(1-t)*t**2
            b3 = t**3
            return (b0 * control_points[0] + 
                   b1 * control_points[1] + 
                   b2 * control_points[2] + 
                   b3 * control_points[3])
        
        return ParametricFunction(
            bezier_point,
            t_range=[0, 1],
            color=color,
            stroke_width=4
        )
    
    def create_slider(self):
        """Create a slider for t parameter"""
        line = Line(LEFT * 3, RIGHT * 3, color=WHITE, stroke_width=3)
        handle = Dot(color=RED)
        handle.add_updater(lambda d: d.move_to(line.get_start() + (line.get_end() - line.get_start()) * self.t_value))
        
        slider = VGroup(line, handle)
        self.t_value = 0  # Will be updated during animation
        
        return slider
    
    def animate_curve_with_slider(self, curve, slider, t_label, control_points):
        """Animate curve drawing with slider movement"""
        curve_copy = curve.copy()
        curve_copy.set_stroke(opacity=0.3)
        # self.add(curve_copy)
        
        # Animate the curve being drawn progressively
        for t in np.linspace(0, 1, 100):
            # Update slider position
            self.t_value = t
            slider[1].move_to(slider[0].get_start() + (slider[0].get_end() - slider[0].get_start()) * t)
            
            # Update t label
            new_label = MathTex(f"t = {t:.2f}", font_size=24, color=WHITE)
            new_label.next_to(slider, UP, buff=0.2)
            t_label.become(new_label)
            
            # Draw partial curve
            partial_curve = ParametricFunction(
                lambda s: self.bezier_point(control_points, s),
                t_range=[0, t],
                color=YELLOW,
                stroke_width=4
            )
            
            self.add(partial_curve)
            self.wait(0.1)
            self.remove(partial_curve)
            
            if t < 1:
                self.remove(partial_curve)
        
        # Final curve
        final_curve = ParametricFunction(
            lambda s: self.bezier_point(control_points, s),
            t_range=[0, 1],
            color=YELLOW,
            stroke_width=4
        )
        self.add(final_curve)
        # self.remove(curve_copy)
        return final_curve
    
    def bezier_point(self, control_points, t):
        """Helper for Bezier point calculation"""
        b0 = (1-t)**3
        b1 = 3*(1-t)**2*t
        b2 = 3*(1-t)*t**2
        b3 = t**3
        return (b0 * control_points[0] + 
               b1 * control_points[1] + 
               b2 * control_points[2] + 
               b3 * control_points[3])
    
    def create_4x4_grid(self):
        """Create a 4x4 grid lines"""
        grid = VGroup()
        
        # Vertical lines
        for i in range(5):
            x = (i - 2) * 2  # Scale to fit screen
            line = Line(
                start=[x, -3, 0],
                end=[x, 3, 0],
                color=WHITE,
                stroke_width=1,
                stroke_opacity=0.5
            )
            grid.add(line)
        
        # Horizontal lines
        for i in range(5):
            y = (i - 2) * 1.5  # Scale to fit screen
            line = Line(
                start=[-4, y, 0],
                end=[4, y, 0],
                color=WHITE,
                stroke_width=1,
                stroke_opacity=0.5
            )
            grid.add(line)
        
        return grid
    
    def get_grid_positions(self, rows, cols):
        """Get center positions for grid cells"""
        positions = []
        for i in range(rows):
            for j in range(cols):
                x = (j - (cols-1)/2) * 2
                y = ((rows-1)/2 - i) * 1.5
                positions.append(np.array([x, y, 0]))
        return positions

# To render: manim -pql file_name.py BezierCurvePresentation