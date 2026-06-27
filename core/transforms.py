"""Geometric transformations module"""

import numpy as np
from typing import List, Tuple, Optional
from .geometry import Point, Line, LineSegment, Ray, GeometricObject
from .shapes import Circle, Polygon, Arc
import math


class TransformationMatrix:
    """2D Transformation matrix (3x3 homogeneous coordinates)"""
    
    def __init__(self, matrix: Optional[np.ndarray] = None):
        if matrix is None:
            self.matrix = np.eye(3)
        else:
            self.matrix = np.array(matrix, dtype=float)
    
    @staticmethod
    def identity() -> 'TransformationMatrix':
        """Create identity transformation"""
        return TransformationMatrix()
    
    @staticmethod
    def translation(tx: float, ty: float) -> 'TransformationMatrix':
        """Create translation matrix"""
        m = np.eye(3)
        m[0, 2] = tx
        m[1, 2] = ty
        return TransformationMatrix(m)
    
    @staticmethod
    def rotation(angle: float, cx: float = 0, cy: float = 0) -> 'TransformationMatrix':
        """Create rotation matrix (angle in degrees)"""
        rad = math.radians(angle)
        cos_a = math.cos(rad)
        sin_a = math.sin(rad)
        
        m = np.eye(3)
        m[0, 0] = cos_a
        m[0, 1] = -sin_a
        m[1, 0] = sin_a
        m[1, 1] = cos_a
        m[0, 2] = cx - cx * cos_a + cy * sin_a
        m[1, 2] = cy - cx * sin_a - cy * cos_a
        
        return TransformationMatrix(m)
    
    @staticmethod
    def scaling(sx: float, sy: float, cx: float = 0, cy: float = 0) -> 'TransformationMatrix':
        """Create scaling matrix"""
        m = np.eye(3)
        m[0, 0] = sx
        m[1, 1] = sy
        m[0, 2] = cx * (1 - sx)
        m[1, 2] = cy * (1 - sy)
        
        return TransformationMatrix(m)
    
    @staticmethod
    def reflection_x(y: float = 0) -> 'TransformationMatrix':
        """Create reflection across horizontal line y=const"""
        m = np.eye(3)
        m[1, 1] = -1
        m[1, 2] = 2 * y
        return TransformationMatrix(m)
    
    @staticmethod
    def reflection_y(x: float = 0) -> 'TransformationMatrix':
        """Create reflection across vertical line x=const"""
        m = np.eye(3)
        m[0, 0] = -1
        m[0, 2] = 2 * x
        return TransformationMatrix(m)
    
    @staticmethod
    def reflection_line(line: Line) -> 'TransformationMatrix':
        """Create reflection across arbitrary line"""
        a, b, c = line.a, line.b, line.c
        m = np.eye(3)
        m[0, 0] = a*a - b*b
        m[0, 1] = 2*a*b
        m[1, 0] = 2*a*b
        m[1, 1] = b*b - a*a
        m[0, 2] = -2*a*c
        m[1, 2] = -2*b*c
        m = m / (a*a + b*b)
        
        return TransformationMatrix(m)
    
    @staticmethod
    def shear(shx: float = 0, shy: float = 0, cx: float = 0, cy: float = 0) -> 'TransformationMatrix':
        """Create shear transformation"""
        m = np.eye(3)
        m[0, 1] = shx
        m[1, 0] = shy
        m[0, 2] = -shx * cy
        m[1, 2] = -shy * cx
        
        return TransformationMatrix(m)
    
    def compose(self, other: 'TransformationMatrix') -> 'TransformationMatrix':
        """Compose two transformations: self followed by other"""
        return TransformationMatrix(other.matrix @ self.matrix)
    
    def apply_to_point(self, point: Point) -> Point:
        """Apply transformation to a point"""
        v = np.array([point.x, point.y, 1])
        v_transformed = self.matrix @ v
        return Point(v_transformed[0], v_transformed[1])
    
    def __repr__(self) -> str:
        return f"TransformationMatrix\n{self.matrix}"


def translate(obj: GeometricObject, tx: float, ty: float) -> GeometricObject:
    """Apply translation to object"""
    transform = TransformationMatrix.translation(tx, ty)
    return _apply_transformation(obj, transform)


def rotate(obj: GeometricObject, angle: float, cx: float = 0, cy: float = 0) -> GeometricObject:
    """Apply rotation to object (angle in degrees)"""
    transform = TransformationMatrix.rotation(angle, cx, cy)
    return _apply_transformation(obj, transform)


def scale(obj: GeometricObject, sx: float, sy: float, cx: float = 0, cy: float = 0) -> GeometricObject:
    """Apply scaling to object"""
    transform = TransformationMatrix.scaling(sx, sy, cx, cy)
    return _apply_transformation(obj, transform)


def reflect(obj: GeometricObject, line: Line) -> GeometricObject:
    """Apply reflection across line to object"""
    transform = TransformationMatrix.reflection_line(line)
    return _apply_transformation(obj, transform)


def shear(obj: GeometricObject, shx: float = 0, shy: float = 0, 
          cx: float = 0, cy: float = 0) -> GeometricObject:
    """Apply shear transformation to object"""
    transform = TransformationMatrix.shear(shx, shy, cx, cy)
    return _apply_transformation(obj, transform)


def _apply_transformation(obj: GeometricObject, transform: TransformationMatrix) -> GeometricObject:
    """Apply transformation to different object types"""
    
    if isinstance(obj, Point):
        return transform.apply_to_point(obj)
    
    elif isinstance(obj, LineSegment):
        p1 = transform.apply_to_point(obj.point1)
        p2 = transform.apply_to_point(obj.point2)
        return LineSegment(p1, p2, obj.name, color=obj.color, line_width=obj.line_width)
    
    elif isinstance(obj, Line):
        p1 = transform.apply_to_point(obj.point1)
        p2 = transform.apply_to_point(obj.point2)
        return Line(p1, p2, obj.name, color=obj.color, line_width=obj.line_width)
    
    elif isinstance(obj, Ray):
        start = transform.apply_to_point(obj.start)
        through = transform.apply_to_point(obj.through)
        return Ray(start, through, obj.name, color=obj.color, line_width=obj.line_width)
    
    elif isinstance(obj, Circle):
        center = transform.apply_to_point(obj.center)
        # For non-uniform scaling, use average scale factor for radius
        scale_x = np.linalg.norm(transform.matrix[:2, 0])
        scale_y = np.linalg.norm(transform.matrix[:2, 1])
        avg_scale = (scale_x + scale_y) / 2
        new_radius = obj.radius * avg_scale
        return Circle(center, new_radius, obj.name, color=obj.color, line_width=obj.line_width)
    
    elif isinstance(obj, Polygon):
        new_vertices = [transform.apply_to_point(v) for v in obj.vertices]
        return Polygon(new_vertices, obj.name, obj.closed, color=obj.color, line_width=obj.line_width)
    
    elif isinstance(obj, Arc):
        center = transform.apply_to_point(obj.center)
        scale_x = np.linalg.norm(transform.matrix[:2, 0])
        scale_y = np.linalg.norm(transform.matrix[:2, 1])
        avg_scale = (scale_x + scale_y) / 2
        new_radius = obj.radius * avg_scale
        return Arc(center, new_radius, obj.start_angle, obj.end_angle, 
                  obj.name, color=obj.color, line_width=obj.line_width)
    
    else:
        # For unknown types, return original
        return obj


class ApplyTransformation:
    """Helper class for chaining transformations"""
    
    def __init__(self, obj: GeometricObject):
        self.obj = obj
        self.transform = TransformationMatrix.identity()
    
    def translate(self, tx: float, ty: float) -> 'ApplyTransformation':
        """Add translation"""
        t = TransformationMatrix.translation(tx, ty)
        self.transform = self.transform.compose(t)
        return self
    
    def rotate(self, angle: float, cx: float = 0, cy: float = 0) -> 'ApplyTransformation':
        """Add rotation"""
        t = TransformationMatrix.rotation(angle, cx, cy)
        self.transform = self.transform.compose(t)
        return self
    
    def scale(self, sx: float, sy: float, cx: float = 0, cy: float = 0) -> 'ApplyTransformation':
        """Add scaling"""
        t = TransformationMatrix.scaling(sx, sy, cx, cy)
        self.transform = self.transform.compose(t)
        return self
    
    def apply(self) -> GeometricObject:
        """Apply all transformations"""
        return _apply_transformation(self.obj, self.transform)
