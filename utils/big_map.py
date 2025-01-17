from decimal import MIN_ETINY
import xml.etree.ElementTree as ET

from PySide6.QtCore import QPointF

def scale_point(point):
    x_min, x_max, y_min, y_max = (573929.0, 652685.0, 4945029.0, 5018275.0)
    x_min_t, x_max_t, y_min_t, y_max_t = (0, 10000, 0, 10000)

    scale_x = (x_max_t - x_min_t) / (x_max - x_min)
    scale_y = (y_max_t - y_min_t) / (y_max - y_min)

    scaled_x = x_min_t + (point.x() - x_min) * scale_x 
    scaled_y = y_min_t + (point.y() - y_min) * scale_y 

    return QPointF(scaled_x - x_max_t/2, -scaled_y + y_max_t/2)

def get_node_data():
    tree = ET.parse("Harta_Luxemburg.xml")
    root = tree.getroot()

    description = root.get("description")
    print(f"Map Description: {description}")

    for node in root.find("nodes").findall("node"):
        node_id = node.get("id")
        latitude = float(node.get("latitude"))
        longitude = float(node.get("longitude"))

        scaled_point = scale_point(QPointF(latitude, longitude))        
        
        yield (node_id, scaled_point)

# for arc in root.find("arcs").findall("arc"):
    #     arc_from = arc.get("from")
    #     arc_to = arc.get("to")
    #     length = arc.get("length")
    #     print(f"Arc from {arc_from} to {arc_to}, Length: {length}")

def get_arc_data():
    tree = ET.parse("Harta_Luxemburg.xml")
    root = tree.getroot()

    description = root.get("description")
    print(f"Map Description: {description}")

    for arc in root.find("arcs").findall("arc"):
        arc_from = arc.get("from")
        arc_to   = arc.get("to")
        length   = int(arc.get("length"))

        yield ((arc_from, arc_to), length)
