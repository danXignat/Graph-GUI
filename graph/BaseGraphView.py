import PySide6.QtWidgets as widg
import PySide6.QtCore as core
import PySide6.QtGui as gui

class BaseGraphView(widg.QGraphicsView):
    def __init__(self):
        super().__init__()
        self.scene = widg.QGraphicsScene(self)
        self.setScene(self.scene)
        
        self._is_zooming = False
        self._is_updating = False
        
        self._setup_view_properties()
        self._setup_zoom_parameters()
        
    def _setup_view_properties(self):
        self.setViewportUpdateMode(widg.QGraphicsView.ViewportUpdateMode.SmartViewportUpdate)
        self.setCacheMode(widg.QGraphicsView.CacheModeFlag.CacheBackground)
        self.setOptimizationFlag(widg.QGraphicsView.OptimizationFlag.DontAdjustForAntialiasing, True)
        self.setRenderHint(gui.QPainter.RenderHint.Antialiasing)
        
        self.setHorizontalScrollBarPolicy(core.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(core.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setTransformationAnchor(widg.QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setResizeAnchor(widg.QGraphicsView.ViewportAnchor.AnchorViewCenter)
        
        self.setMouseTracking(True)
        
        size = 10000
        self.setSceneRect(-size/2, -size/2, size, size)
        self.centerOn(0, 0)
        
    def _setup_zoom_parameters(self):
        self.zoom_factor_base = 1.15
        self.current_zoom = 1.0
        self.min_zoom = 0.1
        self.max_zoom = 50.0
        
    def wheelEvent(self, event):
        if self._is_zooming:
            event.ignore()
            return
            
        try:
            self._is_zooming = True
            
            delta = event.angleDelta().y()
            if delta == 0:
                return
                
            factor = pow(self.zoom_factor_base, delta / 240.0)
            resulting_zoom = self.current_zoom * factor
            
            # Check zoom bounds
            if not (self.min_zoom <= resulting_zoom <= self.max_zoom):
                return
                
            old_pos = self.mapToScene(event.position().toPoint())
            
            self.scale(factor, factor)
            self.current_zoom = resulting_zoom
            
            new_pos = self.mapToScene(event.position().toPoint())
            delta = new_pos - old_pos
            self.translate(delta.x(), delta.y())
            
        finally:
            self._is_zooming = False
            
    def resizeEvent(self, event):
        if self._is_updating:
            return
            
        try:
            self._is_updating = True
            super().resizeEvent(event)
            
            # Ensure view stays centered
            if not event.oldSize().isEmpty():
                ratio_x = event.size().width() / event.oldSize().width()
                ratio_y = event.size().height() / event.oldSize().height()
                self.scale(ratio_x, ratio_y)
                
        finally:
            self._is_updating = False

        