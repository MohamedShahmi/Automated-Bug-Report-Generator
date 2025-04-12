import tkinter as tk
from tkinter import filedialog, messagebox
import os
from bug_storage import add_bug, get_all_bugs
from utils import read_log_file, take_or_upload_screenshot
from report_generator import generate_pdf
import pyautogui
from PIL import ImageGrab

# GUI Setup
root = tk.Tk()
root.title("Bug Report Generator")
root.geometry("800x720")
root.configure(bg="#dbeafe")  # Light blue background

# Centered container
container = tk.Frame(root, bg="#dbeafe")
container.pack(expand=True, fill="both")

# Stylish card-like frame
card_frame = tk.Frame(container, bg="#ffffff", bd=2, relief="groove")
card_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

# heading
heading = tk.Label(card_frame, text="🐞 Bug Report Generator", font=("Helvetica", 18, "bold"), bg="#ffffff", fg="#1e40af")
heading.pack(pady=15)

# Bug Title
title_label = tk.Label(card_frame, text="Bug Title", font=("Arial", 12, "bold"), bg="#ffffff")
title_label.pack(pady=(10, 0))

title_entry = tk.Entry(card_frame, width=55, font=("Arial", 12), bg="#f7fafc", bd=3, relief="solid")
title_entry.pack(pady=(0, 10))

# Bug Description
desc_label = tk.Label(card_frame, text="Bug Description", font=("Arial", 12, "bold"), bg="#ffffff")
desc_label.pack()

desc_text = tk.Text(card_frame, height=6, width=55, font=("Arial", 12), bg="#f7fafc", bd=3, relief="solid")
desc_text.pack(pady=(0, 10))

log_text = ""
log_label = None
screenshot_path = None
screenshot_label = None


def select_log_file():
    global log_text
    filepath = filedialog.askopenfilename(title="Select Log File", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if filepath:
        log_text = read_log_file(filepath)
        log_label.config(text=os.path.basename(filepath), fg="green")
    else:
        log_label.config(text="No log file selected", fg="red")


def take_or_upload_screenshot():
    global screenshot_path
    screenshot_choice = messagebox.askyesno("Screenshot Option", "Would you like to take an instant screenshot? (Click No to upload from your computer)")

    if screenshot_choice:  # Take instant screenshot
        screenshot = ImageGrab.grab()
        save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if save_path:
            screenshot.save(save_path)
            screenshot_path = save_path
            screenshot_label.config(text="Screenshot saved!", fg="green")
        else:
            screenshot_label.config(text="No screenshot saved", fg="red")
    else:  # Upload from computer
        screenshot_path = filedialog.askopenfilename(title="Select Screenshot", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])
        if screenshot_path:
            screenshot_label.config(text=os.path.basename(screenshot_path), fg="green")
        else:
            screenshot_label.config(text="No screenshot selected", fg="red")


def add_bug_to_report():
    title = title_entry.get()
    desc = desc_text.get("1.0", tk.END).strip()

    if not title or not desc or not log_text:
        messagebox.showwarning("Missing Data", "Please enter all fields and select a log file.")
        return

    add_bug(title, desc, log_text, screenshot_path)
    messagebox.showinfo("Added", "Bug added to the report list.")
    title_entry.delete(0, tk.END)
    desc_text.delete("1.0", tk.END)


def generate_final_report():
    all_bugs = get_all_bugs()
    if not all_bugs:
        messagebox.showwarning("No Bugs", "No bugs to report.")
        return

    # save location
    file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
    if not file_path:
        messagebox.showwarning("No File Selected", "No file location selected, report generation canceled.")
        return

    generate_pdf(all_bugs, file_path)
    messagebox.showinfo("PDF Generated", f"Report saved to:\n{file_path}")


# Buttons with different background colors
btn1 = tk.Button(card_frame, text="📁 Choose Log File", command=select_log_file, bg="#f9a8d4", fg="black", width=35)
btn1.pack(pady=5)

log_label = tk.Label(card_frame, text="No log file selected", bg="#ffffff", fg="red")
log_label.pack()

btn2 = tk.Button(card_frame, text="🖼 Take or Upload Screenshot", command=take_or_upload_screenshot, bg="#a7f3d0", fg="black", width=35)
btn2.pack(pady=5)

screenshot_label = tk.Label(card_frame, text="No screenshot selected", bg="#ffffff", fg="red")
screenshot_label.pack()

btn3 = tk.Button(card_frame, text="➕ Add to Report", command=add_bug_to_report, bg="#fcd34d", fg="black", width=35)
btn3.pack(pady=15)

btn4 = tk.Button(card_frame, text="📄 Generate PDF Report (All Bugs)", command=generate_final_report, bg="#fecaca", fg="black", width=35)
btn4.pack(pady=10)

root.mainloop()
