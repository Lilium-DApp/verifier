import base64
from PIL import Image
from io import BytesIO

class ImageDecode:
    """A class to decode images from different formats and manipulate them."""

    @staticmethod
    def from_bytes(data: bytes) -> Image.Image:
        """Creates a PIL image from byte data.

        :param data: The image data in bytes.
        :return: An Image object.
        """
        try:
            buffer = BytesIO(data)
            pil_img = Image.open(buffer)
            return pil_img
        except Exception as e:
            raise ValueError("Could not create an image from the provided bytes.") from e

    @staticmethod
    def from_base64(base64_str: str) -> Image.Image:
        """Creates a PIL image from a base64 string.

        :param base64_str: The base64 string containing the image data.
        :return: An Image object.
        """
        try:
            data = base64.b64decode(base64_str)
            return ImageDecode.from_bytes(data)
        except Exception as e:
            raise ValueError("Could not create an image from the provided base64 string.") from e

    @staticmethod
    def resize_and_pad(img: Image.Image, target_size=(640, 640), padding_color=(114, 114, 114)) -> Image.Image:
        """Resizes and pads an image to a target size.

        :param img: The PIL image to be resized and padded.
        :param target_size: The target size for the image (width, height).
        :param padding_color: The padding color (R, G, B).
        :return: The new resized and padded image.
        """
        try:
            ratio = min(target_size[0] / img.size[0], target_size[1] / img.size[1])
            new_size = (
                int(round(img.size[0] * ratio)),
                int(round(img.size[1] * ratio))
            )
            padding = (
                target_size[0] - new_size[0],
                target_size[1] - new_size[1],
            )
            position = (
                padding[0] // 2,
                padding[1] // 2
            )

            new_img = Image.new(mode=img.mode, size=target_size, color=padding_color)
            new_img.paste(
                im=img.resize(new_size),
                box=position,
            )
            return new_img
        except Exception as e:
            raise ValueError("Could not resize and pad the image.") from e
