from modules.distance import estimate_distance


def get_direction(box, frame_width):

    x1, y1, x2, y2 = box

    center_x = (x1 + x2) // 2

    if center_x < frame_width * 0.35:
        return "left"

    elif center_x > frame_width * 0.65:
        return "right"

    else:
        return "center"


def navigation_message(obj, frame_width, frame_height):

    direction = get_direction(obj["box"], frame_width)

    distance = estimate_distance(obj["box"], frame_height)

    name = obj["name"]

    obj_type = obj["type"]

    message = None

    # -------------------------
    # Person
    # -------------------------

    if name == "person":

        if direction == "left":
            message = "Person on your left. Move right."

        elif direction == "right":
            message = "Person on your right. Move left."

        else:
            message = "Person ahead."

    # -------------------------
    # Pothole
    # -------------------------

    elif obj_type == "pothole":

        if direction == "left":
            message = "Pothole on your left."

        elif direction == "right":
            message = "Pothole on your right."

        else:
            message = "Pothole ahead. Stop."

    # -------------------------
    # Currency
    # -------------------------

    elif obj_type == "currency":

        message = f"{name} detected."

    # -------------------------
    # Other Objects
    # -------------------------

    else:

        if direction == "left":
            message = f"{name} on your left."

        elif direction == "right":
            message = f"{name} on your right."

        else:
            message = f"{name} ahead."

    return message, direction