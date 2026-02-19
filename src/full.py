from manim import *
# from manim.utils.color.DVIPSNAMES

from manim.utils.color import interpolate_color, BLUE, GREEN, RED
import numpy as np
from missingcolors import *

class BezierCurvePresentation(MovingCameraScene):
      
    # Helper functions
    def evaluate_basis_individual(self, t_val):
        # Calculate each basis function
        b0 = (1-t_val)**3
        b1 = 3*(1-t_val)**2*t_val
        b2 = 3*(1-t_val)*t_val**2
        b3 = t_val**3
        
        values = [b0, b1, b2, b3]
        
        # Define color gradient function using Manim's color utilities
        
        def value_to_color(val):
            # Ensure val is between 0 and 1
            val = np.clip(val, 0, 1)
            
            # Continuous gradient from RED (0) to GREEN (1)
            return interpolate_color(GREEN, RED, val)
        
        # Create individual lines with colors
        lines = VGroup()
        
        for i, val in enumerate(values):
            # Choose color based on value
            color = value_to_color(val)
            line = MathTex(rf"{val:.3f}", font_size=32, color=color)
            
            lines.add(line)
        
        # Arrange vertically
        lines.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        
        return lines
    
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

class Intro(MovingCameraScene):
    def construct(self):
        # Title Scene
        self.title_scene()

    def title_scene(self):
        # Title
        title = Text("Bezier Curves", font_size=72, color=BLUE)
        title.move_to(ORIGIN)
        
        self.play(Write(title))
        self.wait(3)
        self.play(FadeOut(title))

class Scene1(BezierCurvePresentation):
    def construct(self):
        self.scene1_bezier_with_slider()
    
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

        self.wait(0.5)
        
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
        grid.shift(UP*0.1)
        self.play(FadeIn(grid, shift=DOWN), run_time=1)
        
        # Draw control polygon
        polygon = Polygon(*control_points, color=BLUE, stroke_opacity=0.5, close_new_points=False)
        dots = VGroup(*[Dot(p, color=RED) for p in control_points])
        self.play(Create(dots))
        self.play(Create(polygon))
        
        # Create wiggly Bezier curve with animation
        curve = self.create_bezier_curve(control_points, color=YELLOW)
        
        # Create slider
        slider = self.create_slider()
        slider.to_edge(DOWN, buff=0.4)
        
        # Create t value label
        t_label = MathTex("t = 0.00", font_size=24, color=WHITE)
        t_label.next_to(slider, UP, buff=0.2)
        
        self.play(FadeIn(slider), Write(t_label))

        self.wait(2)
        
        # Animate curve drawing with slider movement
        final_curve = self.animate_curve_with_slider(curve, slider, t_label, control_points)
        
        self.wait(1)
        
        # Fade everything out
        self.play(*[FadeOut(mob) for mob in [c_t, grid, dots, curve, slider, t_label, final_curve, polygon]])

class Scene2(BezierCurvePresentation):
    def construct(self):
        #Scene 2
        self.scene2_parameterized_grid()

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
        self.wait(5)
        
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
            
            # Create curve based on index
            if i == 0:  # Parabola y = x²
                curve = axes.plot(lambda x: x**2, x_range=[-1.5, 1.5], color=color)
                
            elif i == 1:  # Ellipse x²/a² + y²/b² = 1
                curve = axes.plot_parametric_curve(
                    lambda t: [1.5 * np.cos(t), np.sin(t), 0],
                    t_range=[0, 2*PI],
                    color=color
                )
                
            elif i == 2:  # Circle x² + y² = r²
                curve = axes.plot_parametric_curve(
                    lambda t: [np.cos(t), np.sin(t), 0],
                    t_range=[0, 2*PI],
                    color=color
                )
                
            elif i == 3:  # Hyperbola x²/a² - y²/b² = 1
                right_branch = axes.plot_parametric_curve(
                    lambda t: [1.5 * np.cosh(t/1.5), np.sinh(t/1.5), 0],
                    t_range=[-1.5, 1.5],
                    color=color
                )
                left_branch = axes.plot_parametric_curve(
                    lambda t: [-1.5 * np.cosh(t/1.5), np.sinh(t/1.5), 0],
                    t_range=[-1.5, 1.5],
                    color=color
                )
                curve = VGroup(right_branch, left_branch)
                
            elif i == 4:  # x = cosh t, y = sinh t
                right_branch = axes.plot_parametric_curve(
                    lambda t: [1.5 * np.cosh(t/1.5), np.sinh(t/1.5), 0],
                    t_range=[-1.5, 1.5],
                    color=color
                )
                left_branch = axes.plot_parametric_curve(
                    lambda t: [-1.5 * np.cosh(t/1.5), np.sinh(t/1.5), 0],
                    t_range=[-1.5, 1.5],
                    color=color
                )
                curve = VGroup(right_branch, left_branch)
                
            elif i == 5:  # x = t², y = t
                curve = axes.plot_parametric_curve(
                    lambda t: [t**2, t, 0],
                    t_range=[-1.5, 1.5],
                    color=color
                )
                
            elif i == 6:  # r = a + b cos θ (limacon)
                curve = axes.plot_parametric_curve(
                    lambda t: [(1 + 0.5*np.cos(t)) * np.cos(t), 
                            (1 + 0.5*np.cos(t)) * np.sin(t), 0],
                    t_range=[0, 2*PI],
                    color=color
                )
                
            elif i == 7:  # x = a cos³ t, y = a sin³ t (astroid)
                curve = axes.plot_parametric_curve(
                    lambda t: [np.cos(t)**3, np.sin(t)**3, 0],
                    t_range=[0, 2*PI],
                    color=color
                )
                
            elif i == 8:  # x = cos t, y = sin 2t (Lissajous)
                curve = axes.plot_parametric_curve(
                    lambda t: [np.cos(t), np.sin(2*t), 0],
                    t_range=[0, 2*PI],
                    color=color
                )
                
            elif i == 9:  # r = aθ (Archimedean spiral)
                curve = axes.plot_parametric_curve(
                    lambda t: [0.3 * t * np.cos(t), 0.3 * t * np.sin(t), 0],
                    t_range=[0, 4*PI],
                    color=color
                )
                
            elif i == 10:  # x = sec t, y = tan t
                right_branch = axes.plot_parametric_curve(
                    lambda t: [1.5 / np.cos(t), np.tan(t), 0],
                    t_range=[-1.2, 1.2],
                    color=color,
                    discontinuities=[-PI/2, PI/2]
                )
                left_branch = axes.plot_parametric_curve(
                    lambda t: [-1.5 / np.cos(t), np.tan(t), 0],
                    t_range=[-1.2, 1.2],
                    color=color,
                    discontinuities=[-PI/2, PI/2]
                )
                curve = VGroup(right_branch, left_branch)
                
            elif i == 11:  # x = cos³ t, y = sin³ t (astroid)
                curve = axes.plot_parametric_curve(
                    lambda t: [np.cos(t)**3, np.sin(t)**3, 0],
                    t_range=[0, 2*PI],
                    color=color
                )
                
            elif i == 12:  # x = t sin t, y = t cos t
                curve = axes.plot_parametric_curve(
                    lambda t: [t * np.sin(t), t * np.cos(t), 0],
                    t_range=[0, 2*PI],
                    color=color
                )
                
            elif i == 13:  # x = e^t cos t, y = e^t sin t (logarithmic spiral)
                curve = axes.plot_parametric_curve(
                    lambda t: [0.3 * np.exp(0.2*t) * np.cos(t), 
                            0.3 * np.exp(0.2*t) * np.sin(t), 0],
                    t_range=[0, 3*PI],
                    color=color
                )
                
            elif i == 14:  # x = cosh t, y = sinh t
                right_branch = axes.plot_parametric_curve(
                    lambda t: [1.5 * np.cosh(t/1.5), np.sinh(t/1.5), 0],
                    t_range=[-1.5, 1.5],
                    color=color
                )
                left_branch = axes.plot_parametric_curve(
                    lambda t: [-1.5 * np.cosh(t/1.5), np.sinh(t/1.5), 0],
                    t_range=[-1.5, 1.5],
                    color=color
                )
                curve = VGroup(right_branch, left_branch)
                
            elif i == 15:  # x = cos 2t, y = sin 3t (Lissajous)
                curve = axes.plot_parametric_curve(
                    lambda t: [np.cos(2*t), np.sin(3*t), 0],
                    t_range=[0, 2*PI],
                    color=color
                )
                
            else:  # Default fallback
                curve = axes.plot(lambda x: x**2, x_range=[-1, 1], color=color)
            
            curves.add(axes, curve)
        
        # Fade in grid and curves
        self.play(
            FadeIn(grid),
            LaggedStart(
                *[Create(curve) for curve in curves if isinstance(curve, VMobject)],
                lag_ratio=0.2  # 0.2 seconds between each curve creation
            ),
            run_time=4  # Total run time
        )
        self.wait(2)
        
        # Fade out everything
        self.play(FadeOut(VGroup(grid, curves)))

class Scene3(BezierCurvePresentation):
    def construct(self):
        # Scene 3
        self.scene3_bezier_transformations()

    def scene3_bezier_transformations(self):
        # Show C(t)
        c_t = MathTex("C(t)", font_size=48, color=YELLOW)
        c_t.move_to(ORIGIN)
        self.play(Write(c_t))
        self.wait(0.5)
        
        # Shift leftward
        self.play(c_t.animate.shift(LEFT * 3))
        
        # Full Bezier equation
        bezier_eq = MathTex(
            r"B(t) = \sum_{i=0}^{n} \binom{n}{i} (1-t)^{n-i} t^i P_i, \quad t \in [0,1]",
            font_size=36,
            color=BLUE
        )
        bezier_eq.next_to(c_t, RIGHT, buff=1)
        
        self.play(Write(bezier_eq))
        self.wait(4)
        
        # Fade out everything
        self.play(*[FadeOut(mob) for mob in [c_t, bezier_eq]])

class Scene4(BezierCurvePresentation):
    def construct(self):
        self.scene4_degree_expansions()
    
    def scene4_degree_expansions(self):
        # Clear the scene
        # self.clear_rects_and_transform()
        
        # Divide frame horizontally
        frame = self.camera.frame
        h_line = Line(
            start=frame.get_left(),
            end=frame.get_right(),
            color=WHITE,
            stroke_width=2
        )
        
        self.play(Create(h_line))
        
        # Add degree labels
        degree2_label = Text("Degree 2 (Quadratic)", font_size=30, color=GREEN)
        degree2_label.move_to(np.array([-3, 2, 0]))
        
        degree3_label = Text("Degree 3 (Cubic)", font_size=30, color=BLUE)
        degree3_label.move_to(np.array([-3, -1, 0]))
        
        self.play(Write(degree2_label), Write(degree3_label))
        self.wait(1)
        
        # Quadratic Bezier (Degree 2)
        quadratic_bezier = MathTex(
            r"B(t) = (1-t)^2 P_0 + 2(1-t)t P_1 + t^2 P_2",
            font_size=28,
            color=GREEN
        )
        quadratic_bezier.move_to(np.array([3, 2, 0]))
        
        # Cubic Bezier (Degree 3)
        cubic_bezier = MathTex(
            r"B(t) = (1-t)^3 P_0 + 3(1-t)^2 t P_1 + 3(1-t) t^2 P_2 + t^3 P_3",
            font_size=28,
            color=BLUE
        )
        cubic_bezier.move_to(np.array([3, -1, 0]))
        
        self.play(Write(quadratic_bezier), Write(cubic_bezier))
        self.wait(2)
        
        # Transform to factorized form (grouped by t powers)

        self.play(FadeOut(mob) for mob in [degree2_label,degree3_label])
        self.wait(2)
        self.play(obj.animate.move_to([-1, obj.get_y(), 0]) for obj in [quadratic_bezier,cubic_bezier])
        
        quadratic_factorized = MathTex(
            r"B(t) = P_0 + (-2P_0 + 2P_1)t + (P_0 - 2P_1 + P_2)t^2",
            font_size=28,
            color=GREEN
        )
        quadratic_factorized.move_to(quadratic_bezier.get_center())
        
        cubic_factorized = MathTex(
            r"B(t) = P_0 + (-3P_0 + 3P_1)t + (3P_0 - 6P_1 + 3P_2)t^2 + (-P_0 + 3P_1 - 3P_2 + P_3)t^3",
            font_size=26,
            color=BLUE
        )
        cubic_factorized.move_to(cubic_bezier.get_center())
        
        self.play(
            Transform(quadratic_bezier, quadratic_factorized),
            Transform(cubic_bezier, cubic_factorized)
        )
        self.wait(3)
        
        # Transform to matrix form
        quadratic_matrix = MathTex(
            r"B(t) = \begin{bmatrix} 1 & t & t^2 \end{bmatrix}",
            r"\begin{bmatrix} 1 & 0 & 0 \\ -2 & 2 & 0 \\ 1 & -2 & 1 \end{bmatrix}",
            r"\begin{bmatrix} P_0 \\ P_1 \\ P_2 \end{bmatrix}",
            font_size=24
        )
        quadratic_matrix.arrange(RIGHT, buff=0.2)
        quadratic_matrix.move_to(quadratic_bezier.get_center())
        
        cubic_matrix = MathTex(
            r"B(t) = \begin{bmatrix} 1 & t & t^2 & t^3 \end{bmatrix}",
            r"\begin{bmatrix} 1 & 0 & 0 & 0 \\ -3 & 3 & 0 & 0 \\ 3 & -6 & 3 & 0 \\ -1 & 3 & -3 & 1 \end{bmatrix}",
            r"\begin{bmatrix} P_0 \\ P_1 \\ P_2 \\ P_3 \end{bmatrix}",
            font_size=22
        )
        cubic_matrix.arrange(RIGHT, buff=0.2)
        cubic_matrix.move_to(cubic_bezier.get_center())
        
        self.play(
            Transform(quadratic_bezier, quadratic_matrix),
            Transform(cubic_bezier, cubic_matrix)
        )
        self.wait(4)
        
        # Show basis matrices explanation
        basis_explanation = Text(
            "Basis matrices convert between Bernstein and power basis",
            font_size=24,
            color=YELLOW
        )
        basis_explanation.to_edge(DOWN, buff=0.5)
        
        self.play(Write(basis_explanation))
        self.wait(3)
        
        # Fade out
        self.play(*[FadeOut(mob) for mob in [
            h_line, degree2_label, degree3_label, 
            quadratic_bezier, cubic_bezier, basis_explanation
        ]])

class Scene5(BezierCurvePresentation):
    def construct(self):
        # Initial cubic Bezier equation
        cubic_bezier = MathTex(
            r"B(t) = (1-t)^3 P_0 + 3(1-t)^2 t P_1 + 3(1-t) t^2 P_2 + t^3 P_3",
            font_size=28,
            color=BLUE
        )
        cubic_bezier.move_to(ORIGIN)
        
        # Fade in initial equation
        self.play(FadeIn(cubic_bezier, scale=0.8))
        self.wait(1)
        
        # First transformation to aligned version
        bezier_aligned = MathTex(
            r"B(t) = (1-t)^3 P_0 \\",
            r"+ 3(1-t)^2 t P_1 \\",
            r"+ 3(1-t) t^2 P_2 \\",
            r"+ t^3 P_3",
            font_size=28,
            color=BLUE
        )
        bezier_aligned.move_to(ORIGIN)
        
        self.play(Transform(cubic_bezier, bezier_aligned))
        self.wait(1)
        
        # Create the two separate parts
        # Basis functions part
        basis_part = MathTex(
            r"(1-t)^3 \\",
            r"3(1-t)^2 t \\",
            r"3(1-t) t^2 \\",
            r"t^3",
            font_size=32,
            color=YELLOW
        )
        
        # Control points part
        points_part = MathTex(
            r"P_0 \\",
            r"P_1 \\",
            r"P_2 \\",
            r"P_3",
            font_size=32,
            color=RED
        )

        # Position them side by side
        basis_part.move_to(ORIGIN + LEFT * 3)
        points_part.move_to(ORIGIN + RIGHT * 3)
        
        # Transform the single equation into the two parts
        self.play(
            ReplacementTransform(cubic_bezier, basis_part),
            FadeIn(points_part, shift=RIGHT),
            run_time = 2
        )
        self.wait(1)
        
        # Add "t = " label above basis part
        t_label = Text("t = ", font_size=24, color=WHITE)
        t_label.next_to(basis_part, UP, buff=0.5)
        t_value = DecimalNumber(0, num_decimal_places=3, font_size=24, color=YELLOW)
        t_value.next_to(t_label, RIGHT)
        
        self.play(Write(t_label), Write(t_value))
        self.wait(1)
        new_basis_loc = basis_part.get_center()
        
        # Animate t from 0 to 1
        for t in np.linspace(0, 1, 40):  # 11 steps from 0 to 1
            new_basis = self.evaluate_basis_individual(t)
            new_basis.move_to(new_basis_loc)
            new_t_value = DecimalNumber(t, num_decimal_places=3, font_size=24, color=YELLOW)
            new_t_value.next_to(t_label, RIGHT)
            
            self.play(
                ReplacementTransform(basis_part, new_basis),
                Transform(t_value, new_t_value),
                run_time=0.5
            )
            basis_part = new_basis
            self.wait(0.1)
        
        self.wait(2)


class Scene6(BezierCurvePresentation):
    def construct(self):
        # Control points for the Bezier curve
        self.control_points = [
            np.array([-4, -2, 0]),
            np.array([-2, 3, 0]),
            np.array([2, -1, 0]),
            np.array([4, 2, 0])
        ]
        
        # Part 1: Show basis and points part (from Scene 5)
        self.show_basis_and_points()
        
        # Part 2: Shift everything down and fade in grid above
        self.shift_and_add_grid()
        
        # Part 3: Transform points to coordinates with lag
        self.transform_points_to_coordinates()
        
        # Part 4: Animate t from 0 to 1 with basis evaluation and curve drawing
        self.animate_t_variation_with_lines()
        
        # Fade out everything
        self.fade_out_all()
    
    def show_basis_and_points(self):
        # Basis part (Bernstein polynomials)
        self.basis_part = MathTex(
            r"(1-t)^3 + \\",
            r"3(1-t)^2 t + \\",
            r"3(1-t) t^2 + \\",
            r"t^3",
            font_size=32,
            color=YELLOW
        )
        
        # Points part (control points)
        self.points_part = MathTex(
            r"P_0 \\",
            r"P_1 \\",
            r"P_2 \\",
            r"P_3",
            font_size=32,
            color=RED
        )
        
        # Position them side by side at top
        self.basis_part.move_to(ORIGIN + LEFT * 3 + UP * 2)
        self.points_part.move_to(ORIGIN + RIGHT * 3 + UP * 2)
        
        
        
        # Fade everything in
        self.play(
            FadeIn(self.basis_part),
            FadeIn(self.points_part),
        )
        self.wait(1)
        
        
    
    def shift_and_add_grid(self):
        shift_amount = DOWN * 4.5
        self.play(
            self.basis_part.animate.shift(shift_amount),
            self.points_part.animate.shift(shift_amount)
        )
        # Get the current positions of basis and points parts
        basis_bottom = self.basis_part.get_bottom()
        points_bottom = self.points_part.get_bottom()
        
        # Find the lowest point between them (they should be at similar height)
        lowest_y = min(basis_bottom[1], points_bottom[1])
        
        # Get camera frame boundaries
        frame_top = self.camera.frame.get_top()[1]
        
        # Calculate available vertical space between top of frame and basis/points
        available_height = frame_top - lowest_y - 0.5  # 0.5 buffer
        
        # Calculate grid height (leaving some margin)
        grid_height = min(6, available_height * 0.8)  # Use 80% of available space
        
        # Calculate aspect ratio for grid (standard 16:9-ish for full frame)
        grid_width = grid_height * (16/9) * 0.8  # Slightly narrower than full frame
        
        # Shift basis and points downward
        
        
        # Create grid with calculated dimensions
        self.grid = NumberPlane(
            x_range=[-5, 5, 1],
            y_range=[-3, 3, 1],
            x_length=grid_width,
            y_length=grid_height,
            background_line_style={
                "stroke_color": GRAY,
                "stroke_width": 1,
                "stroke_opacity": 0.3
            }
        )
        
        # Position grid in the upper half, centered horizontally
        grid_center_y = (frame_top + lowest_y) / 2  # Midpoint between top and basis
        self.grid.move_to([0, grid_center_y, 0])
        
        # Fade in grid
        self.play(FadeIn(self.grid, scale=0.8), run_time=1)
        self.wait(0.5)
    
    def transform_points_to_coordinates(self):
        # Create coordinate representation of control points
        coord_strings = []
        for i, p in enumerate(self.control_points):
            coord_strings.append(rf"({p[0]:.0f}, {p[1]:.0f})")
        
        # Create coordinate labels with lag
        self.coord_labels = VGroup()
        colors = [BLUE, GREEN, YELLOW, RED]
        
        for i, (coord, color) in enumerate(zip(coord_strings, colors)):
            label = MathTex(coord, font_size=28, color=color)
            label.move_to(self.points_part[i].get_center())
            self.coord_labels.add(label)
        
        # Replacement transform with lag
        self.play(
            LaggedStart(
                *[ReplacementTransform(self.points_part[i], self.coord_labels[i]) 
                  for i in range(4)],
                lag_ratio=0.3
            )
        )
        self.wait(0.5)
        
        # Plot the points on the grid
        self.points_dots = VGroup()
        for i, p in enumerate(self.control_points):
            dot = Dot(
                point=self.grid.c2p(p[0], p[1]),  # Convert to grid coordinates
                color=colors[i],
                radius=0.08
            )
            self.points_dots.add(dot)
        
        # Add dots with lag
        self.play(
            LaggedStart(
                *[Create(dot) for dot in self.points_dots],
                lag_ratio=0.2
            )
        )
        
        # Draw control polygon (open - don't connect last to first)
        self.control_lines = VGroup()
        for i in range(len(self.control_points) - 1):
            line = Line(
                start=self.grid.c2p(self.control_points[i][0], self.control_points[i][1]),
                end=self.grid.c2p(self.control_points[i+1][0], self.control_points[i+1][1]),
                color=BLUE,
                stroke_opacity=0.5
            )
            self.control_lines.add(line)
        
        self.play(Create(self.control_lines))
        self.wait(0.5)
    
    def animate_t_variation_with_lines(self):
        # Create slider
        self.slider = self.create_slider()
        self.slider.to_edge(DOWN, buff=0.2)
        
        # Create t value label
        self.t_label = MathTex("t = 0.00", font_size=24, color=WHITE)
        self.t_label.next_to(self.slider, UP, buff=0.2)
        
        self.play(FadeIn(self.slider), Write(self.t_label))
        
        # Create moving point on curve
        self.curve_point = Dot(color=WHITE)
        self.curve_point.move_to(self.get_bezier_point(0))
        self.add(self.curve_point)
        
        # Create the full curve (will be drawn progressively)
        self.full_curve = self.create_bezier_curve_mobject()
        self.full_curve.set_stroke(opacity=0.3)
        # self.add(self.full_curve)
        
        # Initialize colored lines
        self.colored_lines = VGroup()
        basis_colors = [BLUE, GREEN, YELLOW, RED]  # Initial colors (will be updated)
        
        # Create initial lines (transparent)
        for i, p in enumerate(self.control_points):
            line = Line(
                start=self.grid.c2p(p[0], p[1]),
                end=self.curve_point.get_center(),
                color=WHITE,
                stroke_width=2,
                stroke_opacity=0.3
            )
            self.colored_lines.add(line)
        
        # self.add(self.colored_lines)
        
        # Animate t from 0 to 1
        for t in np.linspace(0, 1, 101):
            # Calculate basis values
            b0 = (1-t)**3
            b1 = 3*(1-t)**2*t
            b2 = 3*(1-t)*t**2
            b3 = t**3
            values = [b0, b1, b2, b3]
            
            # Get colors for each basis value
            line_colors = [self.value_to_color(val) for val in values]
            
            # Update basis part with colors
            new_basis = self.evaluate_basis_with_colormap(t)
            new_basis.move_to(self.basis_part.get_center())
            
            # Update t label
            new_t_label = MathTex(f"t = {t:.2f}", font_size=24, color=WHITE)
            new_t_label.next_to(self.slider, UP, buff=0.2)
            
            # Update slider position
            self.slider[1].move_to(
                self.slider[0].get_start() + 
                (self.slider[0].get_end() - self.slider[0].get_start()) * t
            )
            
            # Get current curve point
            current_point = self.get_bezier_point(t)
            
            # Update curve point
            self.curve_point.move_to(current_point)
            
            # Draw partial curve up to current t
            partial_curve = self.create_partial_bezier_curve(t)
            
            if t > 0:
                self.remove(self.current_partial_curve)
            
            self.current_partial_curve = partial_curve
            self.add(partial_curve)
            
            # Update colored lines with new colors and positions
            new_lines = VGroup()
            for i, (p, color) in enumerate(zip(self.control_points, line_colors)):
                line = Line(
                    start=self.grid.c2p(p[0], p[1]),
                    end=current_point,
                    color=color,
                    stroke_width=2 + values[i] * 3,  # Line width based on basis value
                    stroke_opacity=0.5 + values[i] * 0.5  # Opacity based on basis value
                )
                new_lines.add(line)
                
            if (t==0):
                self.play(FadeIn(self.colored_lines),ReplacementTransform(self.basis_part,new_basis),FadeIn(self.full_curve),run_time=1)
                self.basis_part=new_basis
            else:
                self.remove(self.colored_lines)
                self.colored_lines = new_lines
                self.add(self.colored_lines)
                
                # Update basis display
                self.remove(self.basis_part)
                self.basis_part = new_basis
                self.add(self.basis_part)
                
                # Update t label
                self.remove(self.t_label)
                self.t_label = new_t_label
                self.add(self.t_label)
            
            # Wait a tiny bit for each frame
            self.wait(0.1)
        
        # Final curve
        final_curve = self.create_bezier_curve_mobject(color=YELLOW)
        self.remove(self.current_partial_curve, self.full_curve)
        self.add(final_curve)
        self.curve = final_curve
        
        # Final update with t=1
        b0, b1, b2, b3 = 0, 0, 0, 1
        values = [b0, b1, b2, b3]
        final_colors = [self.value_to_color(val) for val in values]
        
        final_lines = VGroup()
        for i, (p, color) in enumerate(zip(self.control_points, final_colors)):
            line = Line(
                start=self.grid.c2p(p[0], p[1]),
                end=self.get_bezier_point(1),
                color=color,
                stroke_width=2 + values[i] * 3,
                stroke_opacity=0.5 + values[i] * 0.5
            )
            final_lines.add(line)
        
        self.remove(self.colored_lines)
        self.colored_lines = final_lines
        self.add(self.colored_lines)
        
        self.wait(1)

    def value_to_color(self, val):
        """Convert basis value to color (0=BLUE, 0.5=GREEN, 1=RED)"""
        from manim.utils.color import interpolate_color, BLUE, GREEN, RED
        
        val = np.clip(val, 0, 1)
        
        if val <= 0.5:
            # Blue (0) to Green (0.5)
            return interpolate_color(BLUE, GREEN, val * 2)
        else:
            # Green (0.5) to Red (1)
            return interpolate_color(GREEN, RED, (val - 0.5) * 2)

    def evaluate_basis_with_colormap(self, t_val):
        """Create basis display with colors matching the lines"""
        # Calculate each basis function
        b0 = (1-t_val)**3
        b1 = 3*(1-t_val)**2*t_val
        b2 = 3*(1-t_val)*t_val**2
        b3 = t_val**3
        
        values = [b0, b1, b2, b3]
        
        # Create individual lines with colors
        lines = VGroup()
        
        for i, val in enumerate(values):
            color = self.value_to_color(val)
            
            if i < 3:  # First three lines with plus
                line = MathTex(rf"{val:.2f} +", font_size=32, color=color)
            else:  # Last line without plus
                line = MathTex(rf"{val:.2f}", font_size=32, color=color)
            
            lines.add(line)
        
        # Arrange vertically
        lines.arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        
        return lines

    # Replace the original animate_t_variation and bonus_colored_lines with:
    def animate_t_variation(self):
        self.animate_t_variation_with_lines()

    def bonus_colored_lines(self):
        # This is now integrated into animate_t_variation_with_lines
        pass
    
    def fade_out_all(self):
        # Fade out everything
        all_objects = VGroup(
            self.basis_part, self.coord_labels,
            self.grid, self.control_lines, self.points_dots,
            self.slider, self.t_label, self.curve, self.curve_point,
            self.colored_lines
        )
        
        self.play(FadeOut(all_objects))
        self.wait(1)
    
    # Helper functions
    def create_slider(self):
        line = Line(LEFT * 3, RIGHT * 3, color=WHITE, stroke_width=3)
        handle = Dot(color=RED)
        handle.move_to(line.get_left())
        return VGroup(line, handle)
    
    def get_bezier_point(self, t):
        p0, p1, p2, p3 = self.control_points
        b0 = (1-t)**3
        b1 = 3*(1-t)**2*t
        b2 = 3*(1-t)*t**2
        b3 = t**3
        
        point = b0 * p0 + b1 * p1 + b2 * p2 + b3 * p3
        return self.grid.c2p(point[0], point[1])
    
    def create_bezier_curve_mobject(self, color=YELLOW):
        return ParametricFunction(
            lambda t: self.grid.c2p(
                self.bezier_point(t)[0],
                self.bezier_point(t)[1]
            ),
            t_range=[0, 1],
            color=color,
            stroke_width=3
        )
    
    def create_partial_bezier_curve(self, t_max):
        return ParametricFunction(
            lambda t: self.grid.c2p(
                self.bezier_point(t)[0],
                self.bezier_point(t)[1]
            ),
            t_range=[0, t_max],
            color=YELLOW,
            stroke_width=3
        )
    
    def bezier_point(self, t):
        p0, p1, p2, p3 = self.control_points
        b0 = (1-t)**3
        b1 = 3*(1-t)**2*t
        b2 = 3*(1-t)*t**2
        b3 = t**3
        return b0 * p0 + b1 * p1 + b2 * p2 + b3 * p3
    
    def evaluate_basis_with_colormap(self, t_val):
        # Calculate each basis function
        b0 = (1-t_val)**3
        b1 = 3*(1-t_val)**2*t_val
        b2 = 3*(1-t_val)*t_val**2
        b3 = t_val**3
        
        values = [b0, b1, b2, b3]
        
        # Define color gradient from RED (0) to GREEN (1)
        from manim.utils.color import interpolate_color, RED, GREEN
        
        def value_to_color(val):
            return interpolate_color(RED, GREEN, val)
        
        # Create individual lines with colors
        lines = VGroup()
        
        for i, val in enumerate(values):
            color = value_to_color(val)
            
            if i < 3:  # First three lines with plus
                line = MathTex(rf"{val:.2f} +", font_size=32, color=color)
            else:  # Last line without plus
                line = MathTex(rf"{val:.2f}", font_size=32, color=color)
            
            lines.add(line)
        
        # Arrange vertically
        lines.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        
        return lines


# To render: manim -pql full.py SceneN