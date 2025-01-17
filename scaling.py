def compute_scale_and_offset(x_min, y_min, x_max, y_max, width, height):
    grid_height = x_max - x_min
    grid_width = y_max - y_min

    if grid_width == 0 or grid_height == 0:
        raise ValueError("Grid dimensions cannot be zero.")

    scale_x = height / grid_height
    scale_y = width / grid_width
    scale = min(scale_x, scale_y)

    return scale

def scale_coordinates(x, y, x_min, y_min, scale):
    scaled_x = (x - x_min) * scale
    scaled_y = (y - y_min) * scale
    return scaled_x, scaled_y
