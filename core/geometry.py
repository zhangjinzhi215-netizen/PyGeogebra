"""Core geometric objects and base classes"""

import numpy as np
from typing import Tuple, List, Optional, Dict, Any
from abc import ABC, abstractmethod
import uuid
from datetime import datetime


class GeometricObject(ABC):
    """Base class for all geometric objects"""
    
    def __init__(self, name: Optional[str] = None, color: str = "black", 
                 line_width: float = 2.0, alpha: float = 1.0):
        self.id = str(uuid.uuid4())
        self.name = name or f"Object_{self.id[:8]}"
        self.color = color
        self.line_width = line_width
        self.alpha = alpha
        self.visible = True
        self.selected = False
        self.locked = False
        self.tags = set()
        self.metadata = {}
        self.created_at = datetime.now()
        self.modified_at = datetime.now()
        self.constraints = []
        self.parent_objects = []  # Objects this depends on
        self.child_objects = []   # Objects that depend on this
        
    @abstractmethod
    def get_bounds(self) -> Tuple[float, float, float, float]:
        """Return (xmin, ymin, xmax, ymax)"""
        pass
    
    @abstractmethod
    def get_vertices(self) -> np.ndarray:
        """Return array of vertices/points"""
        pass
    
    @abstractmethod
    def contains_point(self, point: 'Point', tolerance: float = 1e-6) -> bool:
        """Check if point is on/in this object"""
        pass
    
    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary"""
        pass
    
    def add_constraint(self, constraint):
        """Add constraint to object"""
        if constraint not in self.constraints:
            self.constraints.append(constraint)
            self.modified_at = datetime.now()
    
    def remove_constraint(self, constraint):
        """Remove constraint from object"""
        if constraint in self.constraints:
            self.constraints.remove(constraint)
            self.modified_at = datetime.now()
    
    def add_parent(self, obj: 'GeometricObject'):
        """Add dependency"""
        if obj not in self.parent_objects:
            self.parent_objects.append(obj)
            obj.child_objects.append(self)
    
    def get_distance_to_point(self, point: 'Point') -> float:
        """Calculate minimum distance to point"""
        raise NotImplementedError
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name='{self.name}', id='{self.id[:8]}')"
    
    def __eq__(self, other) -> bool:
        return isinstance(other, GeometricObject) and self.id == other.id
    
    def __hash__(self) -> int:
        return hash(self.id)


class Point(GeometricObject):
    """Represents a point in 2D space"""
    
    def __init__(self, x: float, y: float, name: Optional[str] = None, **kwargs):
        super().__init__(name, **kwargs)
        self.x = float(x)
        self.y = float(y)
        self.size = kwargs.get('size', 5.0)
        self.is_fixed = False
    
    def get_coordinates(self) -> Tuple[float, float]:
        """Get point coordinates"""
        return (self.x, self.y)
    
    def set_coordinates(self, x: float, y: float):
        """Set point coordinates"""
        self.x = float(x)
        self.y = float(y)
        self.modified_at = datetime.now()
    
    def get_bounds(self) -> Tuple[float, float, float, float]:
        offset = self.size / 2
        return (self.x - offset, self.y - offset, self.x + offset, self.y + offset)
    
    def get_vertices(self) -> np.ndarray:
        return np.array([[self.x, self.y]])
    
    def contains_point(self, point: 'Point', tolerance: float = 1e-6) -> bool:
        dist = np.sqrt((self.x - point.x)**2 + (self.y - point.y)**2)
        return dist <= tolerance
    
    def distance_to(self, other: 'Point') -> float:
        """Calculate distance to another point"""
        return np.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)
    
    def midpoint(self, other: 'Point') -> 'Point':
        """Get midpoint between this and another point"""
        return Point((self.x + other.x) / 2, (self.y + other.y) / 2)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'type': 'Point',
            'id': self.id,
            'name': self.name,
            'x': self.x,
            'y': self.y,
            'color': self.color,
            'size': self.size,
            'visible': self.visible
        }
    
    def __repr__(self) -> str:
        return f"Point({self.name}, {self.x:.2f}, {self.y:.2f})"


class Line(GeometricObject):
    """Represents an infinite line defined by two points or equation ax + by + c = 0"""
    
    def __init__(self, point1: Point, point2: Point, name: Optional[str] = None, **kwargs):
        super().__init__(name, **kwargs)
        self.point1 = point1
        self.point2 = point2
        self.add_parent(point1)
        self.add_parent(point2)
        self._update_equation()
    
    def _update_equation(self):
        """Calculate line equation ax + by + c = 0"""
        x1, y1 = self.point1.x, self.point1.y
        x2, y2 = self.point2.x, self.point2.y
        
        if abs(x2 - x1) < 1e-10:  # Vertical line
            self.a, self.b, self.c = 1, 0, -x1
        elif abs(y2 - y1) < 1e-10:  # Horizontal line
            self.a, self.b, self.c = 0, 1, -y1
        else:
            # General case: (y2-y1)x - (x2-x1)y + (x2-x1)y1 - (y2-y1)x1 = 0
            self.a = y2 - y1
            self.b = -(x2 - x1)
            self.c = (x2 - x1) * y1 - (y2 - y1) * x1
        
        # Normalize
        norm = np.sqrt(self.a**2 + self.b**2)
        if norm > 0:
            self.a /= norm
            self.b /= norm
            self.c /= norm
    
    def get_slope(self) -> Optional[float]:
        """Get line slope, None if vertical"""
        if abs(self.point2.x - self.point1.x) < 1e-10:
            return None
        return (self.point2.y - self.point1.y) / (self.point2.x - self.point1.x)
    
    def get_bounds(self) -> Tuple[float, float, float, float]:
        # Return extended bounds for infinite line
        x1, y1 = self.point1.x, self.point1.y
        x2, y2 = self.point2.x, self.point2.y
        return (min(x1, x2) - 1000, min(y1, y2) - 1000,
                max(x1, x2) + 1000, max(y1, y2) + 1000)
    
    def get_vertices(self) -> np.ndarray:
        return np.array([[self.point1.x, self.point1.y], [self.point2.x, self.point2.y]])
    
    def contains_point(self, point: Point, tolerance: float = 1e-6) -> bool:
        """Check if point lies on line"""
        distance = abs(self.a * point.x + self.b * point.y + self.c)
        return distance <= tolerance
    
    def distance_to_point(self, point: Point) -> float:
        """Get perpendicular distance from point to line"""
        return abs(self.a * point.x + self.b * point.y + self.c)
    
    def intersection_with_line(self, other: 'Line') -> Optional[Point]:
        """Find intersection point with another line"""
        det = self.a * other.b - self.b * other.a
        if abs(det) < 1e-10:
            return None  # Parallel lines
        
        x = (self.b * other.c - self.c * other.b) / det
        y = (self.c * other.a - self.a * other.c) / det
        return Point(x, y)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'type': 'Line',
            'id': self.id,
            'name': self.name,
            'point1_id': self.point1.id,
            'point2_id': self.point2.id,
            'color': self.color,
            'visible': self.visible
        }


class LineSegment(GeometricObject):
    """Represents a finite line segment between two points"""
    
    def __init__(self, point1: Point, point2: Point, name: Optional[str] = None, **kwargs):
        super().__init__(name, **kwargs)
        self.point1 = point1
        self.point2 = point2
        self.add_parent(point1)
        self.add_parent(point2)
    
    def get_length(self) -> float:
        """Get segment length"""
        return self.point1.distance_to(self.point2)
    
    def get_midpoint(self) -> Point:
        """Get midpoint of segment"""
        return self.point1.midpoint(self.point2)
    
    def get_bounds(self) -> Tuple[float, float, float, float]:
        x1, y1 = self.point1.x, self.point1.y
        x2, y2 = self.point2.x, self.point2.y
        return (min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2))
    
    def get_vertices(self) -> np.ndarray:
        return np.array([[self.point1.x, self.point1.y], [self.point2.x, self.point2.y]])
    
    def contains_point(self, point: Point, tolerance: float = 1e-6) -> bool:
        """Check if point lies on segment"""
        # Check if point is on infinite line
        dx = self.point2.x - self.point1.x
        dy = self.point2.y - self.point1.y
        
        if abs(dx) < 1e-10 and abs(dy) < 1e-10:
            return self.point1.distance_to(point) <= tolerance
        
        # Check if point is between endpoints
        t = ((point.x - self.point1.x) * dx + (point.y - self.point1.y) * dy) / (dx**2 + dy**2)
        
        if t < -tolerance or t > 1 + tolerance:
            return False
        
        # Check perpendicular distance
        closest_x = self.point1.x + t * dx
        closest_y = self.point1.y + t * dy
        dist = np.sqrt((point.x - closest_x)**2 + (point.y - closest_y)**2)
        
        return dist <= tolerance
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'type': 'LineSegment',
            'id': self.id,
            'name': self.name,
            'point1_id': self.point1.id,
            'point2_id': self.point2.id,
            'length': self.get_length(),
            'color': self.color,
            'visible': self.visible
        }


class Ray(GeometricObject):
    """Represents a ray starting from a point and going through another point"""
    
    def __init__(self, start: Point, through: Point, name: Optional[str] = None, **kwargs):
        super().__init__(name, **kwargs)
        self.start = start
        self.through = through
        self.add_parent(start)
        self.add_parent(through)
        self._update_direction()
    
    def _update_direction(self):
        """Calculate direction vector"""
        dx = self.through.x - self.start.x
        dy = self.through.y - self.start.y
        length = np.sqrt(dx**2 + dy**2)
        if length > 0:
            self.direction = np.array([dx / length, dy / length])
        else:
            self.direction = np.array([1.0, 0.0])
    
    def get_bounds(self) -> Tuple[float, float, float, float]:
        return (self.start.x - 1000, self.start.y - 1000,
                self.start.x + 1000, self.start.y + 1000)
    
    def get_vertices(self) -> np.ndarray:
        return np.array([[self.start.x, self.start.y], [self.through.x, self.through.y]])
    
    def contains_point(self, point: Point, tolerance: float = 1e-6) -> bool:
        """Check if point lies on ray"""
        dx = point.x - self.start.x
        dy = point.y - self.start.y
        
        # Check if point is in correct direction
        dot_product = dx * self.direction[0] + dy * self.direction[1]
        if dot_product < -tolerance:
            return False
        
        # Check perpendicular distance
        cross = abs(dx * self.direction[1] - dy * self.direction[0])
        return cross <= tolerance
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'type': 'Ray',
            'id': self.id,
            'name': self.name,
            'start_id': self.start.id,
            'through_id': self.through.id,
            'color': self.color,
            'visible': self.visible
        }
