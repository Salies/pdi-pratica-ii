import dearpygui.dearpygui as dpg
from PIL import Image
import numpy as np

def save_callback():
    print("Save Clicked")

dpg.create_context()
dpg.create_viewport()
dpg.setup_dearpygui()
im = Image.open("imagens/ramona.png").convert('L').convert('RGBA')
data = np.frombuffer(im.tobytes(), dtype=np.uint8) / 255.0
width, height = im.size

with dpg.texture_registry():
    texture_id = dpg.add_static_texture(width, height, data)

with dpg.window(label="Example Window"):
    dpg.add_image(texture_id)

dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()