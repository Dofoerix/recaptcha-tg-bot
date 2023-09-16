import random
import io

from PIL import Image, ImageFont
from PIL.ImageDraw import ImageDraw
import os
from pathlib import Path


class ImageMaker:
    def __init__(self, images_directory: str) -> None:
        self.images_path = Path(images_directory)

        self.images_dict: dict[str, list[str]] = {}

        for item in self.images_path.iterdir():
            if item.is_dir():
                self.images_dict[item.name] = []
                for inner_item in Path(os.path.join(self.images_path, item.name)).iterdir():
                    if inner_item.is_file():
                        self.images_dict[item.name].append(inner_item.name)

        self.images_list = [(directory, file) for directory, files in self.images_dict.items() for file in files]

        self.coordinates = [(8, 128), (138, 128), (268, 128),
                            (8, 258), (138, 258), (268, 258),
                            (8, 388), (138, 388), (268, 388)]

    def create(self, text: str) -> tuple[bytes, list[int]]:
        """Create reCAPTCHA styled image with defined caption."""
        with Image.open(os.path.join(Path(__file__).parents[1], 'sample.jpg')) as sample:
            draw = ImageDraw(sample)
            draw.text((32, 50), text, font=ImageFont.truetype('Roboto-Black.ttf', size=27))

            correct = random.sample([(text, image) for image in self.images_dict[text]], 4)

            all_incorrect = [image for image in self.images_list if image[0] != text]
            incorrect = random.sample(all_incorrect, 5)

            all = correct + incorrect
            random.shuffle(all)

            correct_nums: list[int] = []

            for num, image, coord in zip(range(9), all, self.coordinates):
                if image in correct:
                    correct_nums.append(num + 1)
                with Image.open(os.path.join(self.images_path, image[0], image[1])) as image:
                    image = image.resize((126, 126), Image.Resampling.LANCZOS)
                    sample.paste(image, coord)

            buf = io.BytesIO()
            sample.save(buf, 'JPEG')

            return buf.getvalue(), correct_nums

    def create_random(self) -> tuple[bytes, list[int]]:
        """Create reCAPTCHA styled image with random caption."""
        return self.create(random.choice(list(self.images_dict.keys())))