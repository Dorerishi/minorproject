from PIL import Image
import os

def compress_image(input_path, output_path=None, quality=85, max_size=(512, 512), delete_original=False):
    img = Image.open(input_path).convert("RGB")
    img.thumbnail(max_size)
    img.thumbnail((512, 512))

    if output_path is None:
        name, _ = os.path.splitext(input_path)
        output_path = name + "_compressed.webp"

    img.save(output_path, format="WEBP", quality=quality)

    if delete_original and os.path.exists(input_path):
        os.remove(input_path)

    return output_path
