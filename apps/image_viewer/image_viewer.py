import os
import shutil
import tkinter as tk
from PIL import ImageTk, Image


SOURCE_PATH = '/media/kgh/Seagate_bare/StarTrek/Episodes/'
DESTINATION_PATH = '/home/kgh/StarTrekGAN/train_blue/'
KEY_DELETE = 119
KEY_RIGHT = 114
KEY_LEFT = 113
KEY_UP = 111
KEY_N = 57


image_window = tk.Tk()
window_closed = False
image_list = []
last_keycode = 0


def on_close():
    global window_closed
    window_closed = True
    image_window.destroy()


def key_handler(event):
    global last_keycode
    last_keycode = event.keycode
    image_window.quit()


for subdir, dirs, files in os.walk(SOURCE_PATH):
    for image_file in files:
        if image_file.endswith('.png'):
            file_path = subdir + '/' + image_file
            image_list.append(file_path)

image_list = sorted(image_list)
panel = tk.Label(image_window, image='')
panel.pack(side="bottom", fill="both", expand="yes")
image_window.bind('<Key>', key_handler)
image_window.protocol("WM_DELETE_WINDOW", on_close)


if not os.path.isdir(DESTINATION_PATH):
    os.mkdir(DESTINATION_PATH)	

i = 0
while i < len(image_list):
    source_file = image_list[i]
    print(source_file)
    img = ImageTk.PhotoImage(Image.open(source_file))
    panel.configure(image=img)
    panel.image = img
    image_window.mainloop()
    if window_closed:
        break
    print(last_keycode)
    if last_keycode == KEY_N:
        # go to next directory
        current_directory = os.path.dirname(source_file)
        while current_directory in image_list[i]:
            i += 1
    elif last_keycode == KEY_RIGHT:
        i += 1
    elif last_keycode == KEY_LEFT:
        i -= 1
    elif last_keycode == KEY_DELETE:
        os.remove(source_file)
        image_list.pop(i)
    elif last_keycode == KEY_UP:
        k = 0
        destination_file = DESTINATION_PATH + str(k) + os.path.basename(source_file)
        while os.path.isfile(destination_file):
            k += 1
            destination_file = DESTINATION_PATH + str(k) + os.path.basename(source_file)
        shutil.move(source_file, destination_file)
        image_list.pop(i)

