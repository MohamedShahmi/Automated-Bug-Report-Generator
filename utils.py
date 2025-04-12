
import os
from tkinter import filedialog
from PIL import ImageGrab
import datetime
import shutil

def read_log_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def take_or_upload_screenshot():
    """Allows the user to either take a screenshot or upload an image file."""
    # Ask the user if they want to take a screenshot or upload
    choice = filedialog.askquestion("Screenshot Option", "Do you want to take a screenshot?\n(Click 'No' to upload an image instead)")

    save_dir = "assets/screenshots"
    if os.path.isfile(save_dir):
        os.remove(save_dir)
    os.makedirs(save_dir, exist_ok=True)

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    if choice == 'yes':
        image = ImageGrab.grab()
        path = os.path.join(save_dir, f"screenshot_{timestamp}.png")
        image.save(path)
        return path
    else:
        filepath = filedialog.askopenfilename(title="Select Image", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if filepath:
            new_path = os.path.join(save_dir, f"uploaded_{timestamp}.png")
            shutil.copy(filepath, new_path)
            return new_path
    return None
