"""Premium SVG icons for TASKY rendered using QPainterPath."""
from PyQt6.QtGui import QPainterPath, QPainter, QPen, QColor, QBrush
from PyQt6.QtCore import Qt, QRectF

class PremiumIcons:
    # Lucide-like SVG paths (simplified for QPainterPath)
    
    @staticmethod
    def get_tasks_path() -> QPainterPath:
        path = QPainterPath()
        # Rounded square outline
        path.addRoundedRect(3, 3, 18, 18, 4.5, 4.5)
        # Checkmark
        path.moveTo(8.5, 12.5)
        path.lineTo(10.5, 14.5)
        path.lineTo(15.5, 9.5)
        return path

    @staticmethod
    def get_focus_path() -> QPainterPath:
        path = QPainterPath()
        # Circle (Clock)
        path.addEllipse(4, 5, 16, 16)
        # Top button
        path.moveTo(10, 2)
        path.lineTo(14, 2)
        # Hands
        path.moveTo(12, 13)
        path.lineTo(12, 9)
        path.moveTo(12, 13)
        path.lineTo(15, 13)
        return path

    @staticmethod
    def get_play_path() -> QPainterPath:
        path = QPainterPath()
        path.moveTo(8, 5)
        path.lineTo(19, 12)
        path.lineTo(8, 19)
        path.closeSubpath()
        return path

    @staticmethod
    def get_pause_path() -> QPainterPath:
        path = QPainterPath()
        path.addRect(6, 4, 4, 16)
        path.addRect(14, 4, 4, 16)
        return path

    @staticmethod
    def get_reset_path() -> QPainterPath:
        path = QPainterPath()
        path.arcTo(4, 4, 16, 16, 45, 270)
        path.moveTo(12, 4)
        path.lineTo(16, 8)
        path.lineTo(12, 12)
        return path

    @staticmethod
    def get_analytics_path() -> QPainterPath:
        path = QPainterPath()
        # Bar 1
        path.addRect(18, 3, 3, 18)
        # Bar 2
        path.addRect(10, 8, 3, 13)
        # Bar 3
        path.addRect(3, 13, 3, 8)
        return path

    @staticmethod
    def get_search_path() -> QPainterPath:
        path = QPainterPath()
        # Circle
        path.addEllipse(3, 3, 11, 11)
        # Handle
        path.moveTo(13, 13)
        path.lineTo(21, 21)
        return path

    @staticmethod
    def get_plus_path() -> QPainterPath:
        path = QPainterPath()
        path.moveTo(12, 5)
        path.lineTo(12, 19)
        path.moveTo(5, 12)
        path.lineTo(19, 12)
        return path

    @staticmethod
    def get_streak_path() -> QPainterPath:
        path = QPainterPath()
        path.moveTo(12, 2)
        path.lineTo(12, 2)
        # Fire icon simplified
        path.moveTo(12, 2)
        path.cubicTo(12, 2, 6, 8, 6, 14)
        path.cubicTo(6, 18, 9, 21, 12, 21)
        path.cubicTo(15, 21, 18, 18, 18, 14)
        path.cubicTo(18, 8, 12, 2, 12, 2)
        return path

    @staticmethod
    def render_icon(painter: QPainter, path: QPainterPath, x: int, y: int, size: int, color: QColor, stroke_width: float = 2.0):
        painter.save()
        painter.translate(x, y)
        scale = size / 24.0
        painter.scale(scale, scale)
        
        pen = QPen(color, stroke_width, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin)
        painter.setPen(pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        
        # If it's the analytics icon, we might want fills for bars
        # But for consistency, let's keep them as outlines or simple shapes
        painter.drawPath(path)
        painter.restore()
