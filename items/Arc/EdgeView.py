import PySide6.QtWidgets as widg
import PySide6.QtCore as core
import PySide6.QtGui as gui


from .Line import Line

class EdgeView(widg.QGraphicsItem):
    def __init__(self, start_point: core.QPointF, end_point = None):
        super().__init__()
        
        end_point = start_point if end_point == None else end_point
        
        self.line  = Line(start_point, end_point, parent = self)
        self.nodes = {"start" : None, "end" : None}

        self.setZValue(0)
    
    #--------------------------------Draw------------------------------------
    
    def boundingRect(self) -> core.QRectF:
        return self.line.boundingRect()

    def paint(self, painter, option, widget=None):
        pass

    def shape(self) -> gui.QPainterPath:
        return self.line.shape()

    #------------------------------Methods-------------------------------------

    def setStartPoint(self, start_point: core.QPointF):
        line = self.line.line()
        line.setP1(start_point)
        self.line.setLine(line)

    def setEndPoint(self, end_point: core.QPointF):
        line = self.line.line()
        line.setP2(end_point)
        self.line.setLine(line)
        
    def update_pos(self):
        self.setStartPoint(self.nodes["start"].scenePos())
        self.setEndPoint(self.nodes["end"].pos())