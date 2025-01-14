from .GraphModel import GraphModel
from .GraphView import GraphView

class GraphController:
    def __init__(self, model: GraphModel, view: GraphView):
        self.view = view
        self.model = model