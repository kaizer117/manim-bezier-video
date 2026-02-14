from manim import *
import numpy as np

class BezierBasisTransformations(MovingCameraScene):
    def construct(self):
        # Title
        title = Text("Bezier Curve Representations", font_size=36)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)
        
        # Create control points for a cubic Bezier curve
        control_points = [
            np.array([-3, -2, 0]),
            np.array([-1, 2, 0]),
            np.array([2, 2, 0]),
            np.array([4, -1, 0])
        ]
        
        # Part 1: Bernstein Basis Representation
        self.show_bernstein_basis(control_points)
        self.wait(2)
        
        # Part 2: Transform to Matrix Basis
        self.show_matrix_basis(control_points)
        self.wait(2)
        
        # Part 3: Algebraic Expanded Notation
        self.show_algebraic_form(control_points)
        self.wait(3)
    
    def show_bernstein_basis(self, control_points):
        # Clear previous content but keep title
        self.clear_rects_and_transform()
        
        # Create section title
        bernstein_title = Text("1. Bernstein Basis", font_size=30, color=BLUE)
        bernstein_title.next_to(self.camera.frame.get_top(), DOWN, buff=0.5)
        self.play(Write(bernstein_title))
        
        # Display control points
        dots = VGroup(*[Dot(point, color=RED, radius=0.08) for point in control_points])
        labels = VGroup(*[
            Text(f"P{i}", font_size=20, color=RED).next_to(point, DOWN, buff=0.1)
            for i, point in enumerate(control_points)
        ])
        
        self.play(
            LaggedStart(*[FadeIn(dot) for dot in dots], lag_ratio=0.2),
            LaggedStart(*[Write(label) for label in labels], lag_ratio=0.2)
        )
        
        # Create Bernstein polynomial representation
        bernstein_eq = MathTex(
            r"B(t) = \sum_{i=0}^{3} P_i \binom{3}{i} t^i (1-t)^{3-i}",
            font_size=36
        )
        bernstein_eq.next_to(bernstein_title, DOWN, buff=0.5)
        
        self.play(Write(bernstein_eq))
        self.wait(1)
        
        # Draw the Bezier curve using Bernstein basis
        curve = self.create_bezier_curve(control_points, color=YELLOW)
        self.play(Create(curve), run_time=2)
        
        # Show basis functions
        self.show_bernstein_basis_functions()
        
        self.wait(1)
    
    def show_matrix_basis(self, control_points):
        # Transform from Bernstein to Matrix basis
        transform_text = Text("Transforming to Matrix Basis...", font_size=28, color=GREEN)
        transform_text.to_edge(DOWN)
        self.play(Write(transform_text))
        self.wait(1)
        
        # Clear previous basis functions and equations
        self.clear_rects_and_transform()
        
        # Create matrix basis title
        matrix_title = Text("2. Matrix Basis (Power Basis)", font_size=30, color=GREEN)
        matrix_title.next_to(self.camera.frame.get_top(), DOWN, buff=0.5)
        self.play(Write(matrix_title))
        
        # Show the conversion matrix
        conversion_matrix = MathTex(
            r"\begin{pmatrix} 1 & 0 & 0 & 0 \\ -3 & 3 & 0 & 0 \\ 3 & -6 & 3 & 0 \\ -1 & 3 & -3 & 1 \end{pmatrix}",
            font_size=36
        )
        conversion_matrix.shift(UP * 1.5)
        self.play(Write(conversion_matrix))
        
        # Show matrix representation
        matrix_eq = MathTex(
            r"B(t) = \begin{bmatrix} 1 & t & t^2 & t^3 \end{bmatrix}",
            r"\begin{bmatrix} 1 & 0 & 0 & 0 \\ -3 & 3 & 0 & 0 \\ 3 & -6 & 3 & 0 \\ -1 & 3 & -3 & 1 \end{bmatrix}",
            r"\begin{bmatrix} P_0 \\ P_1 \\ P_2 \\ P_3 \end{bmatrix}",
            font_size=32
        )
        matrix_eq.next_to(conversion_matrix, DOWN, buff=0.5)
        
        self.play(Write(matrix_eq[0]), Write(matrix_eq[1]), Write(matrix_eq[2]))
        self.wait(2)
        
        # Keep the curve visible
        curve = self.create_bezier_curve(control_points, color=YELLOW)
        self.add(curve)
    
    def show_algebraic_form(self, control_points):
        # Transform to algebraic expanded notation
        transform_text = Text("Expanding to Algebraic Form...", font_size=28, color=ORANGE)
        transform_text.to_edge(DOWN)
        self.play(Write(transform_text))
        self.wait(1)
        
        # Clear previous equations
        self.clear_rects_and_transform()
        
        # Create algebraic form title
        algebraic_title = Text("3. Algebraic Expanded Form", font_size=30, color=ORANGE)
        algebraic_title.next_to(self.camera.frame.get_top(), DOWN, buff=0.5)
        self.play(Write(algebraic_title))
        
        # Show algebraic expansion
        # For cubic Bezier: B(t) = (1-t)³P₀ + 3(1-t)²tP₁ + 3(1-t)t²P₂ + t³P₃
        expanded_eq1 = MathTex(
            r"B(t) = (1-t)^3 P_0 + 3(1-t)^2 t P_1 + 3(1-t) t^2 P_2 + t^3 P_3",
            font_size=36
        )
        expanded_eq1.next_to(algebraic_title, DOWN, buff=0.5)
        self.play(Write(expanded_eq1))
        self.wait(1)
        
        # Further expansion
        expanded_eq2 = MathTex(
            r"B(t) = P_0 + (-3P_0+3P_1)t + (3P_0-6P_1+3P_2)t^2 + (-P_0+3P_1-3P_2+P_3)t^3",
            font_size=32
        )
        expanded_eq2.next_to(expanded_eq1, DOWN, buff=0.5)
        self.play(Write(expanded_eq2))
        self.wait(1)
        
        # Show final polynomial form
        expanded_eq3 = MathTex(
            r"B(t) = a_0 + a_1 t + a_2 t^2 + a_3 t^3",
            font_size=36
        )
        expanded_eq3.next_to(expanded_eq2, DOWN, buff=0.5)
        self.play(Write(expanded_eq3))
        
        # Keep the curve visible
        curve = self.create_bezier_curve(control_points, color=YELLOW)
        self.add(curve)
        
        # Show coefficients explanation
        coeff_text = Text(
            "where a_i are linear combinations of control points",
            font_size=24,
            color=GRAY
        )
        coeff_text.next_to(expanded_eq3, DOWN, buff=0.5)
        self.play(Write(coeff_text))
    
    def create_bezier_curve(self, control_points, color=YELLOW, n_samples=100):
        """Create a cubic Bezier curve from control points"""
        def bezier_point(t):
            # Bernstein polynomials for cubic Bezier
            b0 = (1-t)**3
            b1 = 3*(1-t)**2*t
            b2 = 3*(1-t)*t**2
            b3 = t**3
            
            return (b0 * control_points[0] + 
                   b1 * control_points[1] + 
                   b2 * control_points[2] + 
                   b3 * control_points[3])
        
        curve = ParametricFunction(
            lambda t: bezier_point(t),
            t_range=[0, 1],
            color=color,
            stroke_width=3
        )
        
        return curve
    
    def show_bernstein_basis_functions(self):
        """Show the Bernstein basis functions"""
        basis_title = Text("Bernstein Basis Functions:", font_size=24, color=BLUE)
        basis_title.to_edge(LEFT, buff=1).shift(UP * 2)
        self.play(Write(basis_title))
        
        basis_funcs = VGroup(
            MathTex(r"B_{0,3}(t) = (1-t)^3", font_size=24, color=BLUE),
            MathTex(r"B_{1,3}(t) = 3(1-t)^2 t", font_size=24, color=GREEN),
            MathTex(r"B_{2,3}(t) = 3(1-t) t^2", font_size=24, color=YELLOW),
            MathTex(r"B_{3,3}(t) = t^3", font_size=24, color=RED)
        )
        
        basis_funcs.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        basis_funcs.next_to(basis_title, DOWN, buff=0.3)
        
        for func in basis_funcs:
            self.play(Write(func), run_time=0.5)
    
    def clear_rects_and_transform(self):
        """Helper to clear screen for transitions"""
        self.play(
            *[FadeOut(mob) for mob in self.mobjects if mob != self.camera.frame]
        )

# Alternative: More detailed version with step-by-step transformation
class DetailedBezierTransformations(Scene):
    def construct(self):
        # Control points
        P0 = np.array([-3, -2, 0])
        P1 = np.array([-1, 2, 0])
        P2 = np.array([2, 2, 0])
        P3 = np.array([4, -1, 0])
        
        # Title
        title = Text("Bezier Curve: Three Representations", font_size=36)
        title.to_edge(UP)
        self.add(title)
        
        # Draw control polygon
        control_points = [P0, P1, P2, P3]
        polygon = Polygon(*control_points, color=BLUE, stroke_opacity=0.5)
        dots = VGroup(*[Dot(p, color=RED) for p in control_points])
        
        self.play(Create(polygon), Create(dots))
        
        # Draw the curve
        curve = self.create_bezier_curve(control_points)
        self.play(Create(curve))
        
        # Show Bernstein representation
        self.show_bernstein_representation()
        
        # Transform to matrix representation
        self.transform_to_matrix()
        
        # Transform to algebraic representation
        self.transform_to_algebraic()
        
        self.wait(2)
    
    def create_bezier_curve(self, control_points):
        def bezier(t):
            b0 = (1-t)**3
            b1 = 3*(1-t)**2*t
            b2 = 3*(1-t)*t**2
            b3 = t**3
            return b0*control_points[0] + b1*control_points[1] + b2*control_points[2] + b3*control_points[3]
        
        return ParametricFunction(bezier, t_range=[0, 1], color=YELLOW, stroke_width=4)
    
    def show_bernstein_representation(self):
        eq = MathTex(
            r"B(t) = ",
            r"(1-t)^3P_0 + ",
            r"3(1-t)^2tP_1 + ",
            r"3(1-t)t^2P_2 + ",
            r"t^3P_3"
        )
        eq.scale(0.8)
        eq.to_edge(DOWN)
        
        self.play(Write(eq))
        self.wait(2)
        self.remove(eq)
    
    def transform_to_matrix(self):
        matrix_repr = MathTex(
            r"B(t) = \begin{bmatrix}1 & t & t^2 & t^3\end{bmatrix}",
            r"\begin{bmatrix}1 & 0 & 0 & 0 \\ -3 & 3 & 0 & 0 \\ 3 & -6 & 3 & 0 \\ -1 & 3 & -3 & 1\end{bmatrix}",
            r"\begin{bmatrix}P_0 \\ P_1 \\ P_2 \\ P_3\end{bmatrix}"
        )
        matrix_repr.scale(0.7)
        matrix_repr.to_edge(DOWN)
        
        self.play(Write(matrix_repr))
        self.wait(2)
        self.remove(matrix_repr)
    
    def transform_to_algebraic(self):
        algebraic = MathTex(
            r"B(t) = ",
            r"P_0 + ",
            r"(-3P_0+3P_1)t + ",
            r"(3P_0-6P_1+3P_2)t^2 + ",
            r"(-P_0+3P_1-3P_2+P_3)t^3"
        )
        algebraic.scale(0.7)
        algebraic.to_edge(DOWN)
        
        self.play(Write(algebraic))
        self.wait(2)
        self.remove(algebraic)

# To render: manim -pql file_name.py BezierBasisTransformations