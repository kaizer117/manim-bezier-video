from manim import *
import numpy as np

class ParameterizedCurvesGrid(Scene):
    def construct(self):
        # Title
        title = Text("Parameterized Curves", font_size=42, color=BLUE)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)
        
        # Create the 2x2 grid
        grid = self.create_grid()
        self.play(Create(grid), run_time=1.5)
        
        # Get the four quadrants as numpy arrays
        quadrants = self.get_quadrants()
        
        # Show each curve in its quadrant
        self.show_parabola(quadrants[0])  # Top-left
        self.show_ellipse(quadrants[1])   # Top-right
        self.show_circle(quadrants[2])    # Bottom-left
        self.show_hyperbola(quadrants[3]) # Bottom-right
        
        self.wait(2)
    
    def create_grid(self):
        """Create a 2x2 grid dividing the frame"""
        # Get frame boundaries
        frame = self.camera.frame
        frame_width = frame.width
        frame_height = frame.height
        
        # Create vertical and horizontal lines
        v_line = Line(
            start=[0, -frame_height/2, 0],
            end=[0, frame_height/2, 0],
            color=WHITE,
            stroke_width=2
        )
        
        h_line = Line(
            start=[-frame_width/2, 0, 0],
            end=[frame_width/2, 0, 0],
            color=WHITE,
            stroke_width=2
        )
        
        return VGroup(v_line, h_line)
    
    def get_quadrants(self):
        """Get the centers of the four quadrants as numpy arrays"""
        frame = self.camera.frame
        w = frame.width / 4  # Quarter width for quadrant center
        h = frame.height / 4  # Quarter height for quadrant center
        
        # Return as numpy arrays for proper math operations
        return [
            np.array([-w, h, 0]),   # Top-left
            np.array([w, h, 0]),    # Top-right
            np.array([-w, -h, 0]),  # Bottom-left
            np.array([w, -h, 0])    # Bottom-right
        ]
    
    def create_axes(self, center, size=3):
        """Create axes for a quadrant"""
        axes = Axes(
            x_range=[-2, 2, 1],
            y_range=[-2, 2, 1],
            x_length=size,
            y_length=size,
            axis_config={"color": GRAY, "stroke_width": 1}
        )
        axes.move_to(center)
        
        # Add labels
        x_label = axes.get_x_axis_label("x")
        y_label = axes.get_y_axis_label("y")
        
        return VGroup(axes, x_label, y_label)
    
    def show_parabola(self, center):
        """Show parabola: (t, t²)"""
        axes = self.create_axes(center)
        self.play(Create(axes), run_time=0.5)
        
        # Formula - properly position using numpy array
        formula = MathTex(
            r"\begin{cases} x = t \\ y = t^2 \end{cases}",
            font_size=36,
            color=YELLOW
        )
        formula.move_to(center + np.array([0, 1.5, 0]))
        self.play(Write(formula))
        self.wait(0.5)
        
        # Create parabola curve
        curve = axes.plot_parametric_curve(
            lambda t: np.array([t, t**2, 0]),
            t_range=[-1.5, 1.5],
            color=YELLOW,
            stroke_width=3
        )
        
        # Fade out formula, draw curve
        self.play(
            FadeOut(formula),
            Create(curve, run_time=1.5)
        )
        
        # Add label
        label = Text("Parabola", font_size=20, color=YELLOW)
        label.next_to(axes, UP, buff=0.2)
        self.play(Write(label))
    
    def show_ellipse(self, center):
        """Show ellipse: (2cos(t), sin(t))"""
        axes = self.create_axes(center)
        self.play(Create(axes), run_time=0.5)
        
        # Formula
        formula = MathTex(
            r"\begin{cases} x = 2\cos t \\ y = \sin t \end{cases}",
            font_size=36,
            color=GREEN
        )
        formula.move_to(center + np.array([0, 1.5, 0]))
        self.play(Write(formula))
        self.wait(0.5)
        
        # Create ellipse curve
        curve = axes.plot_parametric_curve(
            lambda t: np.array([2 * np.cos(t), np.sin(t), 0]),
            t_range=[0, 2*PI],
            color=GREEN,
            stroke_width=3
        )
        
        # Fade out formula, draw curve
        self.play(
            FadeOut(formula),
            Create(curve, run_time=1.5)
        )
        
        # Add label
        label = Text("Ellipse", font_size=20, color=GREEN)
        label.next_to(axes, UP, buff=0.2)
        self.play(Write(label))
    
    def show_circle(self, center):
        """Show circle: (cos(t), sin(t))"""
        axes = self.create_axes(center)
        self.play(Create(axes), run_time=0.5)
        
        # Formula
        formula = MathTex(
            r"\begin{cases} x = \cos t \\ y = \sin t \end{cases}",
            font_size=36,
            color=BLUE
        )
        formula.move_to(center + np.array([0, 1.5, 0]))
        self.play(Write(formula))
        self.wait(0.5)
        
        # Create circle curve
        curve = axes.plot_parametric_curve(
            lambda t: np.array([np.cos(t), np.sin(t), 0]),
            t_range=[0, 2*PI],
            color=BLUE,
            stroke_width=3
        )
        
        # Fade out formula, draw curve
        self.play(
            FadeOut(formula),
            Create(curve, run_time=1.5)
        )
        
        # Add label
        label = Text("Circle", font_size=20, color=BLUE)
        label.next_to(axes, UP, buff=0.2)
        self.play(Write(label))
    
    def show_hyperbola(self, center):
        """Show hyperbola: (cosh(t), sinh(t))"""
        axes = self.create_axes(center)
        self.play(Create(axes), run_time=0.5)
        
        # Formula
        formula = MathTex(
            r"\begin{cases} x = \cosh t \\ y = \sinh t \end{cases}",
            font_size=36,
            color=RED
        )
        formula.move_to(center + np.array([0, 1.5, 0]))
        self.play(Write(formula))
        self.wait(0.5)
        
        # Create hyperbola (right branch)
        curve_right = axes.plot_parametric_curve(
            lambda t: np.array([np.cosh(t), np.sinh(t), 0]),
            t_range=[-2, 2],
            color=RED,
            stroke_width=3
        )
        
        # Left branch (x negative)
        curve_left = axes.plot_parametric_curve(
            lambda t: np.array([-np.cosh(t), np.sinh(t), 0]),
            t_range=[-2, 2],
            color=RED,
            stroke_width=3
        )
        
        curve = VGroup(curve_right, curve_left)
        
        # Fade out formula, draw curve
        self.play(
            FadeOut(formula),
            Create(curve, run_time=1.5)
        )
        
        # Add label
        label = Text("Hyperbola", font_size=20, color=RED)
        label.next_to(axes, UP, buff=0.2)
        self.play(Write(label))

class ParameterizedCurvesDynamic(MovingCameraScene):
    def construct(self):
        # Title
        title = Text("Parameterized Curves: Motion along t", font_size=36, color=BLUE)
        title.to_edge(UP)
        self.add(title)
        
        # Get title's bottom boundary
        title_bottom = title.get_bottom()
        title_height = title.height
        title_y_min = title_bottom[1]  # y-coordinate of title's bottom
        
        # Get frame boundaries
        frame = self.camera.frame
        frame_top = frame.get_top()[1]
        frame_bottom = frame.get_bottom()[1]
        frame_left = frame.get_left()[0]
        frame_right = frame.get_right()[0]
        
        # Calculate available space below title
        available_height = frame_top - frame_bottom - title_height - 1.0  # -1.0 for extra buffer
        available_width = frame_right - frame_left
        
        # Adjust quadrant sizes based on available space
        w = available_width / 4
        h = available_height / 4
        
        # Calculate vertical offset to center quadrants in available space
        # The center of the available space is halfway between title bottom and frame bottom
        vertical_center = (frame_bottom + title_y_min) / 2
        
        quad_centers = [
            np.array([-w, vertical_center + h, 0]),   # Top-left (below title)
            np.array([w, vertical_center + h, 0]),    # Top-right (below title)
            np.array([-w, vertical_center - h, 0]),   # Bottom-left
            np.array([w, vertical_center - h, 0])     # Bottom-right
        ]
        
        # Create grid lines that account for title
        grid_lines = VGroup(
            Line(
                start=[0, frame_bottom, 0],
                end=[0, title_y_min, 0],
                color=WHITE, 
                stroke_width=2
            ),
            Line(
                start=[frame_left, vertical_center, 0],
                end=[frame_right, vertical_center, 0],
                color=WHITE, 
                stroke_width=2
            )
        )
        self.add(grid_lines)
        
        # Create axes in each quadrant
        axes_list = []
        colors = [YELLOW, GREEN, BLUE, RED]
        names = ["Parabola", "Ellipse", "Circle", "Hyperbola"]
        
        for i, center in enumerate(quad_centers):
            axes = Axes(
                x_range=[-2, 2, 1],
                y_range=[-2, 2, 1],
                x_length=3,
                y_length=3,
                axis_config={"color": GRAY}
            )
            axes.move_to(center)
            axes_list.append(axes)
            self.add(axes)
            
            # Add quadrant labels
            label = Text(names[i], font_size=16, color=colors[i])
            label.next_to(axes, UP, buff=0.2)
            self.add(label)
        
        # Show each curve
        self.animate_parabola(quad_centers[0], axes_list[0])
        self.animate_ellipse(quad_centers[1], axes_list[1])
        self.animate_circle(quad_centers[2], axes_list[2])
        self.animate_hyperbola(quad_centers[3], axes_list[3])
    
    def animate_parabola(self, center, axes):
        formula = MathTex(r"(t, t^2)", color=YELLOW, font_size=30)
        formula.move_to(center + np.array([0, 1.2, 0]))
        self.play(Write(formula))
        
        curve = axes.plot_parametric_curve(
            lambda t: np.array([t, t**2, 0]),
            t_range=[-1.5, 1.5],
            color=YELLOW
        )
        
        self.play(FadeOut(formula), Create(curve))
        self.wait(0.5)
    
    def animate_ellipse(self, center, axes):
        formula = MathTex(r"(2\cos t, \sin t)", color=GREEN, font_size=30)
        formula.move_to(center + np.array([0, 1.2, 0]))
        self.play(Write(formula))
        
        curve = axes.plot_parametric_curve(
            lambda t: np.array([2*np.cos(t), np.sin(t), 0]),
            t_range=[0, 2*PI],
            color=GREEN
        )
        
        self.play(FadeOut(formula), Create(curve))
        self.wait(0.5)
    
    def animate_circle(self, center, axes):
        formula = MathTex(r"(\cos t, \sin t)", color=BLUE, font_size=30)
        formula.move_to(center + np.array([0, 1.2, 0]))
        self.play(Write(formula))
        
        curve = axes.plot_parametric_curve(
            lambda t: np.array([np.cos(t), np.sin(t), 0]),
            t_range=[0, 2*PI],
            color=BLUE
        )
        
        self.play(FadeOut(formula), Create(curve))
        self.wait(0.5)
    
    def animate_hyperbola(self, center, axes):
        formula = MathTex(r"(\cosh t, \sinh t)", color=RED, font_size=30)
        formula.move_to(center + np.array([0, 1.2, 0]))
        self.play(Write(formula))
        
        curve_right = axes.plot_parametric_curve(
            lambda t: np.array([np.cosh(t), np.sinh(t), 0]),
            t_range=[-1.5, 1.5],
            color=RED
        )
        
        curve_left = axes.plot_parametric_curve(
            lambda t: np.array([-np.cosh(t), np.sinh(t), 0]),
            t_range=[-1.5, 1.5],
            color=RED
        )
        
        self.play(FadeOut(formula), Create(curve_right), Create(curve_left))
        self.wait(0.5)

# Alternative: More flexible version with automatic spacing
class ParameterizedCurvesDynamicWithSpacing(Scene):
    def construct(self):
        # Title
        title = Text("Parameterized Curves: Motion along t", font_size=36, color=BLUE)
        title.to_edge(UP)
        self.add(title)
        
        # Get title's bottom
        title_bottom = title.get_bottom()
        
        # Create a VGroup for all content below title
        content_area = VGroup()
        
        # Create 2x2 grid in the remaining space
        frame = self.camera.frame
        
        # Create grid lines that start below title
        v_line = Line(
            start=frame.get_top() * np.array([0, 1, 1]) + np.array([0, title_bottom[1], 0]),
            end=frame.get_bottom(),
            color=WHITE,
            stroke_width=2
        )
        
        h_line = Line(
            start=frame.get_left(),
            end=frame.get_right(),
            color=WHITE,
            stroke_width=2
        )
        # Adjust horizontal line to be in the middle of available space
        h_line.move_to(np.array([0, (frame.get_bottom()[1] + title_bottom[1])/2, 0]))
        
        grid_lines = VGroup(v_line, h_line)
        self.add(grid_lines)
        
        # Calculate quadrant centers
        left_x = frame.get_left()[0] + frame.width/4
        right_x = frame.get_right()[0] - frame.width/4
        top_y = (title_bottom[1] + h_line.get_center()[1])/2
        bottom_y = (h_line.get_center()[1] + frame.get_bottom()[1])/2
        
        quad_centers = [
            np.array([left_x, top_y, 0]),
            np.array([right_x, top_y, 0]),
            np.array([left_x, bottom_y, 0]),
            np.array([right_x, bottom_y, 0])
        ]
        
        # Create axes
        axes_list = []
        colors = [YELLOW, GREEN, BLUE, RED]
        names = ["Parabola: (t, t²)", "Ellipse: (2cos t, sin t)", 
                 "Circle: (cos t, sin t)", "Hyperbola: (cosh t, sinh t)"]
        
        for i, center in enumerate(quad_centers):
            axes = Axes(
                x_range=[-2, 2, 1],
                y_range=[-2, 2, 1],
                x_length=2.5,
                y_length=2.5,
                axis_config={"color": GRAY}
            )
            axes.move_to(center)
            axes_list.append(axes)
            self.add(axes)
            
            # Add labels below each quadrant
            label = Text(names[i], font_size=14, color=colors[i])
            label.next_to(axes, DOWN, buff=0.3)
            self.add(label)
        
        # Animate curves
        self.animate_parabola(quad_centers[0], axes_list[0])
        self.animate_ellipse(quad_centers[1], axes_list[1])
        self.animate_circle(quad_centers[2], axes_list[2])
        self.animate_hyperbola(quad_centers[3], axes_list[3])
    
    def animate_parabola(self, center, axes):
        curve = axes.plot_parametric_curve(
            lambda t: np.array([t, t**2, 0]),
            t_range=[-1.5, 1.5],
            color=YELLOW
        )
        self.play(Create(curve))
    
    def animate_ellipse(self, center, axes):
        curve = axes.plot_parametric_curve(
            lambda t: np.array([2*np.cos(t), np.sin(t), 0]),
            t_range=[0, 2*PI],
            color=GREEN
        )
        self.play(Create(curve))
    
    def animate_circle(self, center, axes):
        curve = axes.plot_parametric_curve(
            lambda t: np.array([np.cos(t), np.sin(t), 0]),
            t_range=[0, 2*PI],
            color=BLUE
        )
        self.play(Create(curve))
    
    def animate_hyperbola(self, center, axes):
        curve_right = axes.plot_parametric_curve(
            lambda t: np.array([np.cosh(t), np.sinh(t), 0]),
            t_range=[-1.5, 1.5],
            color=RED
        )
        curve_left = axes.plot_parametric_curve(
            lambda t: np.array([-np.cosh(t), np.sinh(t), 0]),
            t_range=[-1.5, 1.5],
            color=RED
        )
        self.play(Create(curve_right), Create(curve_left))