#!/usr/bin/env python
# Display a runtext with double-buffering.
from samplebase import SampleBase
from rgbmatrix import graphics
import time
import os

class RunText(SampleBase):
    
    # font_file = "./font/" + "jiskan16s.bdf" 
    # font_pos = 22   # 0-32: jiskan16
    font_file = "./font/" + "jiskan24h.bdf" 
    font_pos = 24   # 0-32: jiskan24

    def __init__(self, *args, **kwargs):
        super(RunText, self).__init__(*args, **kwargs)
        self.parser.add_argument("-f", "--folder", help="The folder containing images to display", required=True)
        self.parser.add_argument("-l", "--loop", help="loop count, 0 for infinite", default=0, type=int)
        self.parser.add_argument("-t", "--text", help="The text to scroll on the RGB LED panel", default="Hello world!")
    
    def read_message_from_file(self, file_path):
        try:
            with open(file_path, 'r') as file:
                return file.read().strip()
        except Exception as e:
            print(f"Error reading message file: {str(e)}")
            return "Hello LED matrix, Welcome!"

    def run(self):
        offscreen_canvas = self.matrix.CreateFrameCanvas()
        font = graphics.Font()
        font.LoadFont(self.font_file)
        textColor = graphics.Color(255, 255, 255)
        pos = offscreen_canvas.width
        my_text = self.args.text
        message_file = self.args.folder + "/message.txt"
        # Read text from file
        if os.path.isfile(message_file):
            my_text = self.read_message_from_file(message_file)

        loop_count = 0
        while True:
            offscreen_canvas.Clear()
            len = graphics.DrawText(offscreen_canvas, font, pos, self.font_pos, textColor, my_text)
            pos -= 1
            if (pos + len < 0):
                pos = offscreen_canvas.width
                # exit with loop count option
                if self.args.loop > 0: 
                    loop_count += 1
                    if loop_count >= self.args.loop:
                        # break loop
                        break
            # time.sleep(0.05)
            time.sleep(0.02)
            offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)

# Main function
if __name__ == "__main__":
    run_text = RunText()
    if (not run_text.process()):
        run_text.print_help()
