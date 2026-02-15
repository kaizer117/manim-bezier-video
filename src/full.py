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

        # Scene 4: Degree Expansions
        self.scene4_degree_expansions()
    
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

# To render: manim -pql full.py BezierCurvePresentation