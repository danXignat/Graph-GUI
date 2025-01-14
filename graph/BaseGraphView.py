import PySide6.QtWidgets as widg
import PySide6.QtCore as core
import PySide6.QtGui as gui

class BaseGraphView(widg.QGraphicsView):
    def __init__(self):
        super().__init__()
        scene = widg.QGraphicsScene(self)
        self.setScene(scene)
        self.setRenderHint(gui.QPainter.RenderHint.Antialiasing)
        
        self.setViewportUpdateMode(widg.QGraphicsView.ViewportUpdateMode.FullViewportUpdate)
        
        self.setHorizontalScrollBarPolicy(core.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(core.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        self.setMouseTracking(True)
        
        size = 1_000_000
        self.setSceneRect(-size / 2, -size / 2, size, size)
        
        self.centerOn(0, 0)
        
        self.zoom_factor_base = 1.15
        self.current_zoom = 1.0
        self.min_zoom = 0.1
        self.max_zoom = 5000.0

    def wheelEvent(self, event):
        old_pos = self.mapToScene(event.position().toPoint())

        if event.angleDelta().y() > 0:
            factor = self.zoom_factor_base
        else:
            factor = self.zoom_factor_base ** (event.angleDelta().y() / 120)

        new_zoom = self.current_zoom * factor
        
        if self.min_zoom <= new_zoom <= self.max_zoom:
            self.current_zoom = new_zoom
            self.scale(factor, factor)
            
            new_pos = self.mapToScene(event.position().toPoint())
            
            delta = new_pos - old_pos
            self.translate(delta.x(), delta.y())

    def resizeEvent(self, event):
        super().resizeEvent(event)
        
    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        self.setDragMode(widg.QGraphicsView.DragMode.RubberBandDrag)
        
    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        self.setDragMode(widg.QGraphicsView.DragMode.NoDrag)
        