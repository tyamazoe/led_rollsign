#!/usr/bin/env python
from samplebase import SampleBase
from PIL import Image
import time
import os

class ImageViewFolder(SampleBase):
    def __init__(self, *args, **kwargs):
        super(ImageViewFolder, self).__init__(*args, **kwargs)
        self.parser.add_argument("-f", "--folder", help="The folder containing images to display", required=True)
        self.parser.add_argument("-d", "--duration", help="Display duration for each image in seconds", default=1, type=float)
        self.parser.add_argument("-l", "--loop", help="loop count, 0 for infinite", default=0, type=int)

    def run(self):
        folder_path = self.args.folder
        duration = self.args.duration

        # Get all image files from the specified folder
        image_extensions = ('.png', '.jpg', '.jpeg', '.bmp', '.gif')
        image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(image_extensions)]

        if not image_files:
            print(f"No image files found in {folder_path}")
            return
        # sort image files by name
        image_files.sort()

        loop_count = 0
        while True:
            for image_file in image_files:
                file_path = os.path.join(folder_path, image_file)
                try:
                    image = Image.open(file_path)

                    # Make image fit our screen.
                    # image.thumbnail((self.matrix.width, self.matrix.height), Image.ANTIALIAS)
                    image.thumbnail((self.matrix.width, self.matrix.height), Image.LANCZOS)

                    # Clear the matrix before displaying the new image
                    self.matrix.Clear()

                    self.matrix.SetImage(image.convert('RGB'))
                    time.sleep(duration)

                except Exception as e:
                    print(f"Error displaying {image_file}: {str(e)}")
            
            # Clear the matrix after showing all images
            self.matrix.Clear()
            # loop count
            if self.args.loop > 0: 
                loop_count += 1
                if loop_count >= self.args.loop:
                    # break loop
                    break

# Main function
if __name__ == "__main__":
    image_view_folder = ImageViewFolder()
    if (not image_view_folder.process()):
        image_view_folder.print_help()