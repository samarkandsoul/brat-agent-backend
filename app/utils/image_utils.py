"""
Image Utils – şəkillərlə basic əməliyyatlar üçün skeleton.
Real funksiyalar Creative Factory-də implement olunacaq.
"""

from PIL import Image
from typing import Tuple


class ImageUtils:
    @staticmethod
    def load_image(path: str) -> Image.Image:
        return Image.open(path)

    @staticmethod
    def resize(image: Image.Image, size: Tuple[int, int]) -> Image.Image:
        return image.resize(size)

    @staticmethod
    def save(image: Image.Image, path: str) -> None:
        image.save(path)
