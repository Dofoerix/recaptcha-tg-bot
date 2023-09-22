import random
import io
import os
from pathlib import Path
from typing import Optional

from PIL import Image, ImageFont
from PIL.ImageDraw import ImageDraw


class ImageMaker:
    def __init__(self, images_directory: str, include_directories: Optional[list[str]] = None,
                 exclude_directories: Optional[list[str]] = None,
                 no_caption_directories: Optional[list[str]] = None) -> None:
        self.images_path = Path(images_directory)

        self.images_dict: dict[str, list[str]] = {}

        for item in self.images_path.iterdir():
            if item.is_dir():
                if include_directories:
                    if item.name not in include_directories:
                        continue
                if exclude_directories:
                    if item.name in exclude_directories:
                        continue
                self.images_dict[item.name] = []
                for inner_item in Path(os.path.join(self.images_path, item.name)).iterdir():
                    if inner_item.is_file():
                        self.images_dict[item.name].append(inner_item.name)

        for directory, files in self.images_dict.items():
            if len(files) < 4:
                raise ValueError(f'There must be at least four images in \'{directory}\' directory')

        self.images_list = [(directory, file) for directory, files in self.images_dict.items() for file in files]

        # These images can't be used as caption, but still appear in captcha
        for directory in list(self.images_dict.keys()):
            if directory in no_caption_directories:
                del self.images_dict[directory]

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