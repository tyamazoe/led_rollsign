#!/usr/bin/env python
from samplebase import SampleBase
from rgbmatrix import graphics
from PIL import Image
import time
import os

class ImageAndText(SampleBase):

    # font_file = "./font/" + "jiskan16s.bdf" 
    # font_pos = 22   # 0-32: jiskan16
    font_file = "./font/" + "jiskan24h.bdf" 
    font_pos = 24   # 0-32: jiskan24

    def __init__(self, *args, **kwargs):
        super(ImageAndText, self).__init__(*args, **kwargs)
        self.parser.add_argument("-f", "--folder", help="The folder containing images to display", required=True)
        self.parser.add_argument("-d", "--duration", help="Display duration for each image in seconds", default=1, type=float)

    def read_message_from_file(self, file_path):
        try:
            with open(file_path, 'r') as file:
                return file.read().strip()
        except Exception as e:
            print(f"Error reading message file: {str(e)}")
            return "Hello LED matrix, Welcome!"

    def run(self):
        # image_folder = self.args.folder + "/image" 
        image_folder = self.args.folder
        image_duration = self.args.duration
        message_file = self.args.folder + "/message.txt"

        # Read text from file
        if os.path.isfile(message_file):
            text = self.read_message_from_file(message_file)
            enable_text = True
        else:
            text = "NA"
            enable_text = False

        # Get all image files from the specified folder
        image_extensions = ('.png', '.jpg', '.jpeg', '.bmp', '.gif')
        image_files = [f for f in os.listdir(image_folder) if f.lower().endswith(image_extensions)]

        if not image_files:
            print(f"No image files found in {image_folder}")
            return

        # sort image files by name
        image_files.sort()
        
        offscreen_canvas = self.matrix.CreateFrameCanvas()
        font = graphics.Font()
        font.LoadFont(self.font_file)
        textColor = graphics.Color(255, 255, 255)

        # Main loop
        while True:
            # Display scrolling text
            if enable_text:
                pos = offscreen_canvas.width
                while pos + graphics.DrawText(offscreen_canvas, font, 0, 0, textColor, text) > 0:
                    offscreen_canvas.Clear()
                    len = graphics.DrawText(offscreen_canvas, font, pos, self.font_pos, textColor, text)
                    pos -= 1
                    time.sleep(0.02)
                    offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)

            # Clear the matrix after showing text
            # offscreen_canvas.Clear()
            # self.matrix.SwapOnVSync(offscreen_canvas)

            # Display images
            for image_file in image_files:
                file_path = os.path.join(image_folder, image_file)
                try:
                    image = Image.open(file_path)
                    # image.thumbnail((self.matrix.width, self.matrix.height), Image.ANTIALIAS)
                    image.thumbnail((self.matrix.width, self.matrix.height), Image.LANCZOS)
                    self.matrix.SetImage(image.convert('RGB'))
                    time.sleep(image_duration)
                except Exception as e:
                    print(f"Error displaying {image_file}: {str(e)}")
            
            # Clear the matrix after showing image
            # offscreen_canvas.Clear()
            # self.matrix.SwapOnVSync(offscreen_canvas)

# Main function
if __name__ == "__main__":
    image_and_text = ImageAndText()
    if (not image_and_text.process()):
        image_and_text.print_help()