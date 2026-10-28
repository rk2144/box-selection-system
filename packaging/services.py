from itertools import permutations, product


def overlaps(a, b):
    """Check whether two placed cuboids overlap."""
    return (
        a["x"] < b["x"] + b["length"]
        and a["x"] + a["length"] > b["x"]
        and a["y"] < b["y"] + b["width"]
        and a["y"] + a["width"] > b["y"]
        and a["z"] < b["z"] + b["height"]
        and a["z"] + a["height"] > b["z"]
    )


def can_pack(items, box):
    """Return product placements if every item fits; otherwise None."""
    box_dims = (
        box.inner_length,
        box.inner_width,
        box.inner_height,
    )

    items = sorted(
        items,
        key=lambda dims: dims[0] * dims[1] * dims[2],
        reverse=True,
    )

    placed = []

    for index, (length, width, height) in enumerate(items):
        found = False

        for l, w, h in sorted(set(permutations((length, width, height)))):
            if l > box_dims[0] or w > box_dims[1] or h > box_dims[2]:
                continue

            xs = {0}
            ys = {0}
            zs = {0}

            for item in placed:
                xs.add(item["x"] + item["length"])
                ys.add(item["y"] + item["width"])
                zs.add(item["z"] + item["height"])

            for x, y, z in sorted(product(xs, ys, zs)):
                if (
                    x + l > box_dims[0]
                    or y + w > box_dims[1]
                    or z + h > box_dims[2]
                ):
                    continue

                candidate = {
                    "item_index": index,
                    "x": x,
                    "y": y,
                    "z": z,
                    "length": l,
                    "width": w,
                    "height": h,
                }

                if not any(overlaps(candidate, other) for other in placed):
                    placed.append(candidate)
                    found = True
                    break

            if found:
                break

        if not found:
            return None

    return placed
def recommend_box(order_items):
    """
    order_items format:
    [{"product": product_object, "quantity": 2}, ...]
    """
    if not order_items:
        raise ValueError("Order must contain at least one product.")

    items = []
    total_weight = 0

    for entry in order_items:
        product_obj = entry["product"]
        quantity = entry["quantity"]

        if not isinstance(quantity, int) or isinstance(quantity, bool) or quantity < 1:
            raise ValueError("Quantity must be a positive integer.")

        total_weight += product_obj.weight * quantity

        dimensions = (
            product_obj.length,
            product_obj.width,
            product_obj.height,
        )
        items.extend([dimensions] * quantity)

    boxes = []

    from .models import Box

    for box in Box.objects.all():
        if total_weight > box.max_weight:
            continue

        if can_pack(items, box):
            boxes.append(box)

    if not boxes:
        return None

    return min(boxes, key=lambda box: (box.cost, box.pk))