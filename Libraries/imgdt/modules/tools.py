### imgdt
### v0.0.2
### MikiTwenty

import os
import shutil
from PIL import Image
from .utils import stdoformat, log

class History:
    def __init__(self, path):
        self.path = path

    def read(self, old_labels, new_labels):
        log(f"Reading history from \"{self.path}\"...", stdoformat.TEXT)
        stored_new_names = set()
        with open(self.path, 'r') as history_file:
            for line in history_file:
                old_label, new_label = line.strip().split(',')
                if old_label in old_labels and new_label not in new_labels:
                    line.strip(' ')
                else:
                    stored_new_names.add(new_label)
        log(f"History loaded!", stdoformat.SUCCESS)
        return stored_new_names

    def update(self, old_labels, new_labels):
        log(f"Updating history to \"{self.path}\"...", stdoformat.TEXT)
        for old_label, new_label in zip(old_labels, new_labels):
            with open(self.path, 'a') as history_file:
                history_file.write(f"{old_label},{new_label}\n")
            lines_seen = set()
            with open(self.path, 'r') as file:
                lines = file.readlines()
            with open(self.path, 'w') as file:
                for line in lines:
                    if line.strip() not in lines_seen:
                        file.write(line)
                        lines_seen.add(line.strip())
        log(f"History updated!", stdoformat.SUCCESS)

class Transformer:
    def __init__(self, dataset_folder, target_folder, scaling_size):
        self.dataset_folder = dataset_folder
        self.target_folder = target_folder
        self.scaling_size = scaling_size
        self.old_labels = []
        self.new_labels = []

    def get_labels(self, sort=True):
        log(f"\Scanning \"{self.dataset_folder}\" for images...", stdoformat.TEXT)
        old_labels = [f for f in os.listdir(self.dataset_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]
        log(f"{len(old_labels)} images found!", stdoformat.SUCCESS)
        if sort: old_labels = self.sort(self.dataset_folder, old_labels)
        log(f"Scanning \"{self.target_folder}\" for images...")
        new_labels = [f for f in os.listdir(self.target_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]
        log(f"{len(new_labels)} images found!", stdoformat.SUCCESS)
        self.old_labels = old_labels
        self.new_labels = new_labels
        return old_labels, new_labels

    def sort(self, folder, labels):
        log(f"Sorting images from \"{folder}\"...", stdoformat.TEXT)
        labels.sort()
        log(f"Images sorted!", stdoformat.SUCCESS)
        return labels

    def convert(self, labels, dataset_name, remove_originals=False, stored_new_labels=None):
        log(f"Converting and renaming images to \"{self.target_folder}\"...", stdoformat.TEXT)
        old_labels = []
        new_labels = []
        counter = 0
        index = 1
        for old_label in labels:
            log(f"[{index}/{len(labels)}]", stdoformat.LOADING)
            old_path = os.path.join(self.dataset_folder, old_label)
            if not(old_label.lower().startswith(dataset_name) and old_label[len(dataset_name):].split('.')[0].isdigit()):
                new_label = f'{dataset_name}{index:08d}.jpg'
                if not(new_label in stored_new_labels or new_label in new_labels):
                    while new_label.lower() in labels:
                        index += 1
                        new_label = f'{dataset_name}{index:08d}.jpg'
                    if not old_label.lower().endswith('.jpg'):
                        img = Image.open(old_path)
                        new_path = os.path.join(self.target_folder, new_label)
                        img.convert('RGB').save(new_path, format='JPEG')
                        img.close()
                    else:
                        new_path = os.path.join(self.target_folder, new_label)
                        shutil.copy(old_path, new_path)
                    if remove_originals:
                        os.remove(old_path)
                    old_labels.append(old_label)
                    new_labels.append(new_label)
                    counter += 1
            index += 1
        print(20*' ', end='\r')
        log(f"{counter} images converted and renamed!", stdoformat.SUCCESS)
        return old_labels, new_labels

    def crop(self, labels):
        log(f"Resizing images from \"{self.target_folder}\"...", stdoformat.TEXT)
        counter = 0
        index = 0
        for label in labels:
            log(f"[{index}/{len(labels)}]", stdoformat.LOADING)
            image_path = os.path.join(self.target_folder, label)
            img = Image.open(image_path)
            width, height = img.size
            if height != width and (height == self.scaling_size or width == self.scaling_size):
                if height < width:
                    offset = int((width - self.scaling_size)/2)
                    if width % 2 == 0:
                        cropped_image = img.crop((offset, 0, width-offset, height))
                    else:
                        cropped_image = img.crop((offset, 0, width-offset-1, height))
                    cropped_image.save(image_path, format='JPEG')
                    counter += 1
                elif height > width:
                    offset = int((height - self.scaling_size)/2)
                    if height % 2 == 0:
                        cropped_image = img.crop((0, offset, width, height-offset))
                    else:
                        cropped_image = img.crop((0, offset, width, height-offset-1))
                    cropped_image.save(image_path, format='JPEG')
                    counter += 1
                else:
                    cropped_image = img
            else:
                cropped_image = img
            cropped_image.close()
            index += 1
        print(20*' ', end='\r')
        log(f"{counter} images resized!", stdoformat.SUCCESS)

    def scale(self, labels):
        log(f"Scaling images from \"{self.target_folder}\"...", stdoformat.TEXT)
        counter = 0
        index = 0
        for label in labels:
            log(f"[{index}/{len(labels)}]", stdoformat.LOADING)
            image_path = os.path.join(self.target_folder, label)
            img = Image.open(image_path)
            width, height = img.size
            if self.scaling_size < height and self.scaling_size < width:
                if width <= height:
                    new_width = self.scaling_size
                    new_height = int(height * (self.scaling_size / width))
                elif width > height:
                    new_width = int(width * (self.scaling_size / height))
                    new_height = self.scaling_size
                scaled_image = img.resize((new_width, new_height), Image.LANCZOS)
                scaled_image.save(image_path, format='JPEG')
                counter += 1
            elif self.scaling_size > height and self.scaling_size > width:
                scaled_image = img
                log(f"Image \"{os.path.basename(img.filename)}\" has low resolution: can't be rescaled!", stdoformat.ERROR)
            else:
                scaled_image = img
            scaled_image.close()
            index += 1
        print(20*' ', end='\r')
        log(f"{counter} images scaled!", stdoformat.SUCCESS)