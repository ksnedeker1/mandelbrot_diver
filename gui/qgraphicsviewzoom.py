from PyQt5.QtWidgets import QGraphicsView
from PyQt5.QtCore import Qt, QPointF, pyqtSignal


class QGraphicsViewZoom(QGraphicsView):
    """Interpret mouse events and communicate."""
    SIG_UPDATE_BOUNDS = pyqtSignal(float, QPointF)

    def __init__(self, parent):
        super(QGraphicsViewZoom, self).__init__(parent)

    def wheelEvent(self, event):
        """Handle scroll wheel events for zooming."""
        factor = 5/4 if event.angleDelta().y() > 0 else 4/5
        self.SIG_UPDATE_BOUNDS.emit(factor, event.pos())
