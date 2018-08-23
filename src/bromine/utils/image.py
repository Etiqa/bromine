from PIL import Image
from six import BytesIO


def image_from_bytes(bytes_):
    return Image.open(BytesIO(bytes_))


def png_format(image):
    bytes_ = BytesIO()
    image.save(bytes_, 'PNG')
    return bytes_.getvalue()


class ScreenshotFromPngBytes(object):

    def __init__(self, png_bytes):
        self._png_bytes = png_bytes

    def as_image(self):
        return image_from_bytes(self._png_bytes)

    def as_png_bytes(self):
        return self._png_bytes


class ScreenshotFromImage(object):

    def __init__(self, image):
        self._image = image

    def as_image(self):
        return self._image.copy()

    def as_png_bytes(self):
        return png_format(self._image)
