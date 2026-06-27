"""Measurement and calculation utilities"""

import math
from typing import Tuple, Optional, List
from .geometry import Point, Line, LineSegment, Ray
from .shapes import Circle, Polygon


def distance(p1: Point, p2: Point) -> float:
    """Calculate Euclidean distance between two points"""
    return p1.distance_to(p2)


def angle_between_vectors(v1: Tuple[float, float], 
                          v2: Tuple[float, float]) -> float:
    """Calculate angle between two vectors in degrees"""
    dot = v1[0] * v2[0] + v1[1] * v2[1]
    mag1 = math.sqrt(v1[0]**2 + v1[1]**2)
    mag2 = math.sqrt(v2[0]**2 + v2[1]**2)
    
    if mag1 == 0 or mag2 == 0:
        return 0
    
    cos_angle = dot / (mag1 * mag2)
    cos_angle = max(-1, min(1, cos_angle))  # Clamp to [-1, 1]
    return math.degrees(math.acos(cos_angle))


def angle_at_point(p1: Point, vertex: Point, p2: Point) -> float:
    """Calculate angle at vertex formed by p1-vertex-p2 in degrees"""
    v1 = (p1.x - vertex.x, p1.y - vertex.y)
    v2 = (p2.x - vertex.x, p2.y - vertex.y)
    return angle_between_vectors(v1, v2)


def angle_of_line(line: Line) -> float:
    """Get angle of line with respect to x-axis in degrees"""
    dx = line.point2.x - line.point1.x
    dy = line.point2.y - line.point1.y
    return math.degrees(math.atan2(dy, dx))


def angle_between_lines(line1: Line, line2: Line) -> float:
    """Calculate angle between two lines in degrees"""
    angle1 = angle_of_line(line1)
    angle2 = angle_of_line(line2)
    angle_diff = abs(angle2 - angle1)
    
    # Return acute angle
    if angle_diff > 90:
        angle_diff = 180 - angle_diff
    
    return angle_diff


def are_parallel(line1: Line, line2: Line, tolerance: float = 1e-6) -> bool:
    """Check if two lines are parallel"""
    return abs(angle_between_lines(line1, line2)) < tolerance


def are_perpendicular(line1: Line, line2: Line, tolerance: float = 1e-6) -> bool:
    """Check if two lines are perpendicular"""
    angle = angle_between_lines(line1, line2)
    return abs(angle - 90) < tolerance


def midpoint(p1: Point, p2: Point) -> Point:
    """Get midpoint between two points"""
    return p1.midpoint(p2)


def line_segment_length(segment: LineSegment) -> float:
    """Get length of line segment"""
    return segment.get_length()


def polygon_area(poly: Polygon) -> float:
    """Calculate polygon area"""
    return poly.get_area()


def polygon_perimeter(poly: Polygon) -> float:
    """Calculate polygon perimeter"""
    return poly.get_perimeter()


def circle_area(circle: Circle) -> float:
    """Calculate circle area"""
    return circle.get_area()


def circle_circumference(circle: Circle) -> float:
    """Calculate circle circumference"""
    return circle.get_circumference()


def point_to_line_distance(point: Point, line: Line) -> float:
    """Calculate perpendicular distance from point to line"""
    return line.distance_to_point(point)


def point_to_segment_distance(point: Point, segment: LineSegment) -> float:
    """Calculate distance from point to line segment"""
    dx = segment.point2.x - segment.point1.x
    dy = segment.point2.y - segment.point1.y
    
    if dx == 0 and dy == 0:
        return point.distance_to(segment.point1)
    
    t = ((point.x - segment.point1.x) * dx + (point.y - segment.point1.y) * dy) / (dx**2 + dy**2)
    t = max(0, min(1, t))
    
    closest_x = segment.point1.x + t * dx
    closest_y = segment.point1.y + t * dy
    
    return math.sqrt((point.x - closest_x)**2 + (point.y - closest_y)**2)


def calculate_coordinates(reference_point: Point, distance_val: float, 
                         angle_deg: float) -> Point:
    """Calculate new point at given distance and angle from reference point"""
    angle_rad = math.radians(angle_deg)
    x = reference_point.x + distance_val * math.cos(angle_rad)
    y = reference_point.y + distance_val * math.sin(angle_rad)
    return Point(x, y)


def find_line_intersections(line1: Line, line2: Line) -> Optional[Point]:
    """Find intersection point of two lines"""
    return line1.intersection_with_line(line2)


def find_circle_intersections(circle1: Circle, circle2: Circle) -> List[Point]:
    """Find intersection points of two circles"""
    return circle1.intersection_with_circle(circle2)


def line_segment_intersection(seg1: LineSegment, seg2: LineSegment) -> Optional[Point]:
    """Find intersection of two line segments"""
    x1, y1 = seg1.point1.x, seg1.point1.y
    x2, y2 = seg1.point2.x, seg1.point2.y
    x3, y3 = seg2.point1.x, seg2.point1.y
    x4, y4 = seg2.point2.x, seg2.point2.y
    
    denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    
    if abs(denom) < 1e-10:
        return None  # Parallel or collinear
    
    t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denom
    u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / denom
    
    if 0 <= t <= 1 and 0 <= u <= 1:
        x = x1 + t * (x2 - x1)
        y = y1 + t * (y2 - y1)
        return Point(x, y)
    
    return None
