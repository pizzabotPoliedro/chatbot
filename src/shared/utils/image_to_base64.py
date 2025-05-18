import base64

def image_to_base64(image_bytes):
    if image_bytes:
        return base64.b64encode(image_bytes).decode("utf-8")
    return None