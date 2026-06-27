"""Advanced geometric shapes"""

import numpy as np
from typing import Tuple, List, Optional, Dict, Any
from .geometry import GeometricObject, Point
import math


class Circle(GeometricObject):
    """Represents a circle defined by center point and radius"""
    
    def __init__(self, center: Point, radius: float, name: Optional[str] = None, **kwargs):
        super().__init__(name, **kwargs)
        self.center = center
        self.radius = float(radius)
        self.add_parent(center)
    
    def get_area(self) -> float:
        """Calculate circle area"""
        return math.pi * self.radius ** 2
    
    def get_circumference(self) -> float:
        """Calculate circle circumference"""
        return 2 * math.pi * self.radius
    
    def get_bounds(self) -> Tuple[float, float, float, float]:
        return (self.center.x - self.radius, self.center.y - self.radius,
                self.center.x + self.radius, self.center.y + self.radius)
    
    def get_vertices(self) -> np.ndarray:
        """Get circle vertices (approximated as polygon)"""
        theta = np.linspace(0, 2 * np.pi, 64)
        x = self.center.x + self.radius * np.cos(theta)
        y = self.center.y + self.radius * np.sin(theta)
        return np.column_stack([x, y])
    
    def contains_point(self, point: Point, tolerance: float = 1e-6) -> bool:
        """Check if point is on circle circumference"""
        dist = self.center.distance_to(point)
        return abs(dist - self.radius) <= tolerance
    
    def point_inside(self, point: Point) -> bool:
        """Check if point is inside circle"""
        return self.center.distance_to(point) <= self.radius
    
    def intersection_with_circle(self, other: 'Circle') -> List[Point]:
        """Find intersection points with another circle"""
        d = self.center.distance_to(other.center)
        
        if d > self.radius + other.radius or d < abs(self.radius - other.radius) or d == 0:
            return []
        
        a = (self.radius**2 - other.radius**2 + d**2) / (2 * d)
        h = math.sqrt(self.radius**2 - a**2)
        
        px = self.center.x + a * (other.center.x - self.center.x) / d
        py = self.center.y + a * (other.center.y - self.center.y) / d
        
        x1 = px + h * (other.center.y - self.center.y) / d
        y1 = py - h * (other.center.x - self.center.x) / d
        
        x2 = px - h * (other.center.y - self.center.y) / d
        y2 = py + h * (other.center.x - self.center.x) / d
        
        return [Point(x1, y1), Point(x2, y2)]
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'type': 'Circle',
            'id': self.id,
            'name': self.name,
            'center_id': self.center.id,
            'radius': self.radius,
            'area': self.get_area(),
            'circumference': self.get_circumference(),
            'color': self.color,
            'visible': self.visible
        }


class Ellipse(GeometricObject):
    """Represents an ellipse"""
    
    def __init__(self, center: Point, a: float, b: float, rotation: float = 0, 
                 name: Optional[str] = None, **kwargs):
        super().__init__(name, **kwargs)
        self.center = center
        self.a = float(a)  # Semi-major axis
        self.b = float(b)  # Semi-minor axis
        self.rotation = float(rotation)  # Rotation angle in degrees
        self.add_parent(center)
    
    def get_area(self) -> float:
        """Calculate ellipse area"""
        return math.pi * self.a * self.b
    
    def get_bounds(self) -> Tuple[float, float, float, float]:
        max_r = max(self.a, self.b)
        return (self.center.x - max_r, self.center.y - max_r,
                self.center.x + max_r, self.center.y + max_r)
    
    def get_vertices(self) -> np.ndarray:
        """Get ellipse vertices"""
        theta = np.linspace(0, 2 * np.pi, 128)
        rot = math.radians(self.rotation)
        
        x = self.a * np.cos(theta)
        y = self.b * np.sin(theta)
        
        x_rot = x * math.cos(rot) - y * math.sin(rot) + self.center.x
        y_rot = x * math.sin(rot) + y * math.cos(rot) + self.center.y
        
        return np.column_stack([x_rot, y_rot])
    
    def contains_point(self, point: Point, tolerance: float = 1e-6) -> bool:
        """Check if point is on ellipse"""
        # Transform point to ellipse coordinate system
        rot = -math.radians(self.rotation)
        dx = point.x - self.center.x
        dy = point.y - self.center.y
        
        x = dx * math.cos(rot) - dy * math.sin(rot)
        y = dx * math.sin(rot) + dy * math.cos(rot)
        
        # Check ellipse equation
        val = (x / self.a)**2 + (y / self.b)**2
        return abs(val - 1) <= tolerance
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'type': 'Ellipse',
            'id': self.id,
            'name': self.name,
            'center_id': self.center.id,
            'a': self.a,
            'b': self.b,
            'rotation': self.rotation,
            'area': self.get_area(),
            'color': self.color,
            'visible': self.visible
        }


class Polygon(GeometricObject):
    """Represents a polygon defined by vertices"""
    
    def __init__(self, vertices: List[Point], name: Optional[str] = None, 
                 closed: bool = True, **kwargs):
        super().__init__(name, **kwargs)
        self.vertices = vertices
        self.closed = closed
        for v in vertices:
            self.add_parent(v)
    
    def get_area(self) -> float:
        """Calculate polygon area using shoelace formula"""
        if len(self.vertices) < 3:
            return 0.0
        
        area = 0.0
        for i in range(len(self.vertices)):
            v1 = self.vertices[i]
            v2 = self.vertices[(i + 1) % len(self.vertices)]
            area += v1.x * v2.y - v2.x * v1.y
        
        return abs(area) / 2.0
    
    def get_perimeter(self) -> float:
        """Calculate polygon perimeter"""
        if len(self.vertices) < 2:
            return 0.0
        
        perimeter = 0.0
        for i in range(len(self.vertices)):
            v1 = self.vertices[i]
            v2 = self.vertices[(i + 1) % len(self.vertices)]
            perimeter += v1.distance_to(v2)
        
        if not self.closed and len(self.vertices) > 1:
            perimeter -= self.vertices[-1].distance_to(self.vertices[0])
        
        return perimeter
    
    def get_centroid(self) -> Point:
        """Get polygon centroid"""
        cx = sum(v.x for v in self.vertices) / len(self.vertices)
        cy = sum(v.y for v in self.vertices) / len(self.vertices)
        return Point(cx, cy)
    
    def get_bounds(self) -> Tuple[float, float, float, float]:
        xs = [v.x for v in self.vertices]
        ys = [v.y for v in self.vertices]
        return (min(xs), min(ys), max(xs), max(ys))
    
    def get_vertices(self) -> np.ndarray:
        return np.array([[v.x, v.y] for v in self.vertices])
    
    def contains_point(self, point: Point, tolerance: float = 1e-6) -> bool:
        """Check if point is on polygon edge (not fill)"""
        for i in range(len(self.vertices)):
            v1 = self.vertices[i]
            v2 = self.vertices[(i + 1) % len(self.vertices)]
            
            dx = v2.x - v1.x
            dy = v2.y - v1.y
            
            if dx == 0 and dy == 0:
                continue
            
            t = ((point.x - v1.x) * dx + (point.y - v1.y) * dy) / (dx**2 + dy**2)
            
            if -tolerance <= t <= 1 + tolerance:
                closest_x = v1.x + t * dx
                closest_y = v1.y + t * dy
                dist = math.sqrt((point.x - closest_x)**2 + (point.y - closest_y)**2)
                if dist <= tolerance:
                    return True
        
        return False
    
    def point_inside(self, point: Point) -> bool:
        """Check if point is inside polygon (ray casting)"""
        x, y = point.x, point.y
        inside = False
        
        j = len(self.vertices) - 1
        for i in range(len(self.vertices)):
            xi, yi = self.vertices[i].x, self.vertices[i].y
            xj, yj = self.vertices[j].x, self.vertices[j].y
            
            if ((yi > y) != (yj > y)) and (x < (xj - xi) * (y - yi) / (yj - yi) + xi):
                inside = not inside
            
            j = i
        
        return inside
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'type': 'Polygon',
            'id': self.id,
            'name': self.name,
            'vertices_ids': [v.id for v in self.vertices],
            'area': self.get_area(),
            'perimeter': self.get_perimeter(),
            'color': self.color,
            'visible': self.visible
        }


class Rectangle(Polygon):
    """Represents a rectangle"""
    
    def __init__(self, p1: Point, p2: Point, name: Optional[str] = None, **kwargs):
        # Create rectangle vertices
        vertices = [
            p1,
            Point(p2.x, p1.y),
            p2,
            Point(p1.x, p2.y)
        ]
        super().__init__(vertices, name, closed=True, **kwargs)
        self.p1 = p1
        self.p2 = p2
    
    def get_width(self) -> float:
        return abs(self.p2.x - self.p1.x)
    
    def get_height(self) -> float:
        return abs(self.p2.y - self.p1.y)
    
    def to_dict(self) -> Dict[str, Any]:
        d = super().to_dict()
        d['type'] = 'Rectangle'
        d['width'] = self.get_width()
        d['height'] = self.get_height()
        return d


class RegularPolygon(Polygon):
    """Represents a regular polygon"""
    
    def __init__(self, center: Point, radius: float, sides: int, 
                 rotation: float = 0, name: Optional[str] = None, **kwargs):
        self.center = center
        self.radius = float(radius)
        self.sides = int(sides)
        self.rotation = float(rotation)
        
        # Generate vertices
        vertices = []
        for i in range(sides):
            angle = 2 * math.pi * i / sides + math.radians(rotation)
            x = center.x + radius * math.cos(angle)
            y = center.y + radius * math.sin(angle)
            vertices.append(Point(x, y))
        
        super().__init__(vertices, name, closed=True, **kwargs)
        self.add_parent(center)
    
    def to_dict(self) -> Dict[str, Any]:
        d = super().to_dict()
        d['type'] = 'RegularPolygon'
        d['sides'] = self.sides
        d['radius'] = self.radius
        d['rotation'] = self.rotation
        return d


class Arc(GeometricObject):
    """Represents a circular arc"""
    
    def __init__(self, center: Point, radius: float, start_angle: float, 
                 end_angle: float, name: Optional[str] = None, **kwargs):
        super().__init__(name, **kwargs)
        self.center = center
        self.radius = float(radius)
        self.start_angle = float(start_angle)  # In degrees
        self.end_angle = float(end_angle)
        self.add_parent(center)
    
    def get_arc_length(self) -> float:
        """Calculate arc length"""
        angle_diff = abs(self.end_angle - self.start_angle)
        if angle_diff > 360:
            angle_diff = 360
        return self.radius * math.radians(angle_diff)
    
    def get_bounds(self) -> Tuple[float, float, float, float]:
        return (self.center.x - self.radius, self.center.y - self.radius,
                self.center.x + self.radius, self.center.y + self.radius)
    
    def get_vertices(self) -> np.ndarray:
        start_rad = math.radians(self.start_angle)
        end_rad = math.radians(self.end_angle)
        theta = np.linspace(start_rad, end_rad, 64)
        x = self.center.x + self.radius * np.cos(theta)
        y = self.center.y + self.radius * np.sin(theta)
        return np.column_stack([x, y])
    
    def contains_point(self, point: Point, tolerance: float = 1e-6) -> bool:
        """Check if point is on arc"""
        # Check radius
        dist = self.center.distance_to(point)
        if abs(dist - self.radius) > tolerance:
            return False
        
        # Check angle
        angle = math.degrees(math.atan2(point.y - self.center.y, point.x - self.center.x))
        angle = angle % 360
        start = self.start_angle % 360
        end = self.end_angle % 360
        
        if start <= end:
            return start <= angle <= end
        else:
            return angle >= start or angle <= end
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'type': 'Arc',
            'id': self.id,
            'name': self.name,
            'center_id': self.center.id,
            'radius': self.radius,
            'start_angle': self.start_angle,
            'end_angle': self.end_angle,
            'arc_length': self.get_arc_length(),
            'color': self.color,
            'visible': self.visible
        }
