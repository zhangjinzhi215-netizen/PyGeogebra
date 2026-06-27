"""Mathematical utility functions"""

import math
from typing import Tuple


def clamp(value: float, min_val: float, max_val: float) -> float:
    """Clamp value between min and max"""
    return max(min_val, min(max_val, value))


def normalize(vector: Tuple[float, float]) -> Tuple[float, float]:
    """Normalize vector to unit length"""
    x, y = vector
    length = math.sqrt(x**2 + y**2)
    if length == 0:
        return (0, 0)
    return (x / length, y / length)


def dot_product(v1: Tuple[float, float], v2: Tuple[float, float]) -> float:
    """Calculate dot product of two vectors"""
    return v1[0] * v2[0] + v1[1] * v2[1]


def cross_product_2d(v1: Tuple[float, float], v2: Tuple[float, float]) -> float:
    """Calculate 2D cross product (returns scalar)"""
    return v1[0] * v2[1] - v1[1] * v2[0]


def vector_length(vector: Tuple[float, float]) -> float:
    """Calculate vector length"""
    return math.sqrt(vector[0]**2 + vector[1]**2)


def interpolate(start: float, end: float, t: float) -> float:
    """Linear interpolation between start and end (t in [0, 1])"""
    return start + (end - start) * t


def interpolate_point(p1: Tuple[float, float], p2: Tuple[float, float], 
                     t: float) -> Tuple[float, float]:
    """Linear interpolation between two points"""
    x = interpolate(p1[0], p2[0], t)
    y = interpolate(p1[1], p2[1], t)
    return (x, y)


def angle_between(v1: Tuple[float, float], v2: Tuple[float, float]) -> float:
    """Calculate angle between two vectors in radians"""
    dot = dot_product(v1, v2)
    len1 = vector_length(v1)
    len2 = vector_length(v2)
    
    if len1 == 0 or len2 == 0:
        return 0
    
    cos_angle = dot / (len1 * len2)
    cos_angle = clamp(cos_angle, -1, 1)
    return math.acos(cos_angle)


def rotate_vector(vector: Tuple[float, float], angle: float) -> Tuple[float, float]:
    """Rotate vector by angle in radians"""
    cos_a = math.cos(angle)
    sin_a = math.sin(angle)
    x = vector[0] * cos_a - vector[1] * sin_a
    y = vector[0] * sin_a + vector[1] * cos_a
    return (x, y)


def reflect_vector(vector: Tuple[float, float], normal: Tuple[float, float]) -> Tuple[float, float]:
    """Reflect vector across plane with given normal"""
    d = 2 * dot_product(vector, normal)
    return (vector[0] - d * normal[0], vector[1] - d * normal[1])


def distance_point_to_line(point: Tuple[float, float], 
                          line_start: Tuple[float, float],
                          line_end: Tuple[float, float]) -> float:
    """Calculate distance from point to line"""
    px, py = point
    x1, y1 = line_start
    x2, y2 = line_end
    
    numerator = abs((y2 - y1) * px - (x2 - x1) * py + x2 * y1 - y2 * x1)
    denominator = math.sqrt((y2 - y1)**2 + (x2 - x1)**2)
    
    if denominator == 0:
        return math.sqrt((px - x1)**2 + (py - y1)**2)
    
    return numerator / denominator
