"""PyGeogebra core module - Geometric objects and operations"""

from .geometry import GeometricObject, Point, Line, LineSegment, Ray
from .shapes import Circle, Ellipse, Polygon, Rectangle, RegularPolygon, Arc
from .transforms import (
    translate, rotate, scale, reflect, shear,
    TransformationMatrix, ApplyTransformation
)
from .measurements import (
    distance, angle, area, perimeter, calculate_coordinates
)
from .constraints import (
    Constraint, ParallelConstraint, PerpendicularConstraint,
    TangentConstraint, EqualDistanceConstraint
)

__all__ = [
    'GeometricObject', 'Point', 'Line', 'LineSegment', 'Ray',
    'Circle', 'Ellipse', 'Polygon', 'Rectangle', 'RegularPolygon', 'Arc',
    'translate', 'rotate', 'scale', 'reflect', 'shear', 'TransformationMatrix',
    'distance', 'angle', 'area', 'perimeter', 'calculate_coordinates',
    'Constraint', 'ParallelConstraint', 'PerpendicularConstraint',
    'TangentConstraint', 'EqualDistanceConstraint'
]
