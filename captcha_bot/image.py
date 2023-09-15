import random

from PIL import Image, ImageFont
from PIL.ImageDraw import ImageDraw
import os
from pathlib import Path


class ImageCreator:
    def __init__(self, images_directory: str) -> None:
        images_path = Path(images_directory)

        self.images_dict: dict[str, list[str]] = {}

        for item in images_path.iterdir():
            if item.is_dir():
                self.images_dict[item.name] = []
                for inner_item in Path(os.path.join(images_path, item.name)).iterdir():
                    if inner_item.is_file():
                        self.images_dict[item.name].append(inner_item.name)

        self.images_list = [(directory, file) for directory, files in self.images_dict.items() for file in files]

        self.coordinates = [(8, 128), (138, 128), (268, 128),
                       (8, 258), (138, 258), (268, 258),
                       (8, 388), (138, 388), (268, 388)]

    def create_image(self, text: str) -> Image.Image:
        """Create reCAPTCHA styled image with defined caption"""
        with Image.open('main.jpg') as sample:
            draw = ImageDraw(sample)
            draw.text((32, 50), text, font=ImageFont.truetype('Roboto-Black.ttf', size=27))

            correct = random.sample([(text, image) for image in self.images_dict[text]], 4)

            all_incorrect = [image for image in self.images_list if image[0] != text]
            incorrect = random.sample(all_incorrect, 5)

            all = correct + incorrect
            random.shuffle(all)

            for num, image, coord in zip(range(9), all, self.coordinates):
                if image in correct:
                    print(num+1)
                with Image.open(os.path.join('images', image[0], image[1])) as image:
                    image = image.resize((126, 126), Image.Resampling.LANCZOS)
                    sample.paste(image, coord)

            return sample