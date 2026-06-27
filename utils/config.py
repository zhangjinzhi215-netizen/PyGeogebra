"""Application configuration"""

from dataclasses import dataclass
from typing import Dict, Tuple


@dataclass
class AppConfig:
    """Application configuration settings"""
    
    # Window settings
    WINDOW_WIDTH: int = 1200
    WINDOW_HEIGHT: int = 800
    WINDOW_TITLE: str = "PyGeogebra - Geometry Studio"
    
    # Canvas settings
    CANVAS_BG_COLOR: str = "#ffffff"
    GRID_ENABLED: bool = True
    GRID_SIZE: float = 20.0
    GRID_COLOR: str = "#e0e0e0"
    SNAP_ENABLED: bool = True
    SNAP_TOLERANCE: float = 10.0
    
    # Coordinate system
    SHOW_AXES: bool = True
    ORIGIN_X: float = 600.0
    ORIGIN_Y: float = 400.0
    SCALE: float = 20.0  # Pixels per unit
    
    # Drawing settings
    DEFAULT_COLOR: str = "#000000"
    DEFAULT_LINE_WIDTH: float = 2.0
    POINT_SIZE: float = 5.0
    SELECTED_COLOR: str = "#ff0000"
    SELECTION_LINE_WIDTH: float = 3.0
    
    # Tool settings
    TOOL_CURSOR_SIZE: int = 16
    INTERSECTION_TOLERANCE: float = 5.0
    DISTANCE_TOLERANCE: float = 1e-6
    
    # Animation settings
    DEFAULT_FPS: int = 60
    DEFAULT_ANIMATION_DURATION: int = 2000  # milliseconds
    
    # UI settings
    THEME: str = "light"  # "light" or "dark"
    FONT_FAMILY: str = "Arial"
    FONT_SIZE: int = 10
    
    # Export settings
    EXPORT_DPI: int = 300
    EXPORT_FORMAT: str = "png"  # "png", "svg", "pdf"
    
    # Debug settings
    DEBUG_MODE: bool = False
    SHOW_PERFORMANCE: bool = False
    LOG_LEVEL: str = "INFO"
