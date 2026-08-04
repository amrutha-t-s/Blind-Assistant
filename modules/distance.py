def estimate_distance(box, frame_height):
    """
    Estimate object distance based on bounding box height.
    This is an approximation using image size.
    """

    x1, y1, x2, y2 = box

    object_height = y2 - y1

    if object_height > frame_height * 0.60:
        return "very close"

    elif object_height > frame_height * 0.40:
        return "close"

    elif object_height > frame_height * 0.20:
        return "medium"

    else:
        return "far"