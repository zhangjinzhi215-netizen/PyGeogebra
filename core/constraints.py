"""Geometric constraints system"""

from abc import ABC, abstractmethod
from typing import List, Optional
from .geometry import GeometricObject, Point, Line, LineSegment
from .shapes import Circle
import math


class Constraint(ABC):
    """Base class for geometric constraints"""
    
    def __init__(self, objects: List[GeometricObject], name: str = ""):
        self.objects = objects
        self.name = name
        self.active = True
    
    @abstractmethod
    def is_satisfied(self, tolerance: float = 1e-6) -> bool:
        """Check if constraint is satisfied"""
        pass
    
    @abstractmethod
    def get_error(self) -> float:
        """Get constraint violation amount"""
        pass
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.name})"


class FixedPointConstraint(Constraint):
    """Constraint that fixes a point at specific coordinates"""
    
    def __init__(self, point: Point, x: float, y: float, name: str = ""):
        super().__init__([point], name or "Fixed")
        self.point = point
        self.x = x
        self.y = y
    
    def is_satisfied(self, tolerance: float = 1e-6) -> bool:
        return (abs(self.point.x - self.x) < tolerance and 
                abs(self.point.y - self.y) < tolerance)
    
    def get_error(self) -> float:
        dx = self.point.x - self.x
        dy = self.point.y - self.y
        return math.sqrt(dx**2 + dy**2)


class ParallelConstraint(Constraint):
    """Constraint that makes two lines parallel"""
    
    def __init__(self, line1: Line, line2: Line, name: str = ""):
        super().__init__([line1, line2], name or "Parallel")
        self.line1 = line1
        self.line2 = line2
    
    def is_satisfied(self, tolerance: float = 1e-6) -> bool:
        # Lines are parallel if their direction vectors are parallel
        dx1 = self.line1.point2.x - self.line1.point1.x
        dy1 = self.line1.point2.y - self.line1.point1.y
        dx2 = self.line2.point2.x - self.line2.point1.x
        dy2 = self.line2.point2.y - self.line2.point1.y
        
        # Cross product should be zero
        cross = abs(dx1 * dy2 - dy1 * dx2)
        return cross < tolerance
    
    def get_error(self) -> float:
        dx1 = self.line1.point2.x - self.line1.point1.x
        dy1 = self.line1.point2.y - self.line1.point1.y
        dx2 = self.line2.point2.x - self.line2.point1.x
        dy2 = self.line2.point2.y - self.line2.point1.y
        return abs(dx1 * dy2 - dy1 * dx2)


class PerpendicularConstraint(Constraint):
    """Constraint that makes two lines perpendicular"""
    
    def __init__(self, line1: Line, line2: Line, name: str = ""):
        super().__init__([line1, line2], name or "Perpendicular")
        self.line1 = line1
        self.line2 = line2
    
    def is_satisfied(self, tolerance: float = 1e-6) -> bool:
        # Lines are perpendicular if their direction vectors are orthogonal
        dx1 = self.line1.point2.x - self.line1.point1.x
        dy1 = self.line1.point2.y - self.line1.point1.y
        dx2 = self.line2.point2.x - self.line2.point1.x
        dy2 = self.line2.point2.y - self.line2.point1.y
        
        # Dot product should be zero
        dot = abs(dx1 * dx2 + dy1 * dy2)
        return dot < tolerance
    
    def get_error(self) -> float:
        dx1 = self.line1.point2.x - self.line1.point1.x
        dy1 = self.line1.point2.y - self.line1.point1.y
        dx2 = self.line2.point2.x - self.line2.point1.x
        dy2 = self.line2.point2.y - self.line2.point1.y
        return abs(dx1 * dx2 + dy1 * dy2)


class EqualDistanceConstraint(Constraint):
    """Constraint that makes two segments equal length"""
    
    def __init__(self, seg1: LineSegment, seg2: LineSegment, name: str = ""):
        super().__init__([seg1, seg2], name or "Equal")
        self.seg1 = seg1
        self.seg2 = seg2
    
    def is_satisfied(self, tolerance: float = 1e-6) -> bool:
        len1 = self.seg1.get_length()
        len2 = self.seg2.get_length()
        return abs(len1 - len2) < tolerance
    
    def get_error(self) -> float:
        len1 = self.seg1.get_length()
        len2 = self.seg2.get_length()
        return abs(len1 - len2)


class TangentConstraint(Constraint):
    """Constraint that makes line tangent to circle"""
    
    def __init__(self, line: Line, circle: Circle, name: str = ""):
        super().__init__([line, circle], name or "Tangent")
        self.line = line
        self.circle = circle
    
    def is_satisfied(self, tolerance: float = 1e-6) -> bool:
        dist = self.line.distance_to_point(self.circle.center)
        return abs(dist - self.circle.radius) < tolerance
    
    def get_error(self) -> float:
        dist = self.line.distance_to_point(self.circle.center)
        return abs(dist - self.circle.radius)


class ConcurrentConstraint(Constraint):
    """Constraint that makes lines intersect at a point"""
    
    def __init__(self, lines: List[Line], point: Point, name: str = ""):
        super().__init__(lines + [point], name or "Concurrent")
        self.lines = lines
        self.point = point
    
    def is_satisfied(self, tolerance: float = 1e-6) -> bool:
        return all(line.contains_point(self.point, tolerance) for line in self.lines)
    
    def get_error(self) -> float:
        return max(line.distance_to_point(self.point) for line in self.lines)


class DistanceConstraint(Constraint):
    """Constraint that sets distance between two points"""
    
    def __init__(self, p1: Point, p2: Point, distance: float, name: str = ""):
        super().__init__([p1, p2], name or "Distance")
        self.p1 = p1
        self.p2 = p2
        self.distance = distance
    
    def is_satisfied(self, tolerance: float = 1e-6) -> bool:
        actual = self.p1.distance_to(self.p2)
        return abs(actual - self.distance) < tolerance
    
    def get_error(self) -> float:
        actual = self.p1.distance_to(self.p2)
        return abs(actual - self.distance)
