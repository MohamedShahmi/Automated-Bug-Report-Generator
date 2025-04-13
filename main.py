import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
from bug_storage import add_bug, get_all_bugs
from utils import read_log_file
from report_generator import generate_pdf
from PIL import ImageGrab

# Appearance
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# GUI Setup
root = ctk.CTk()
root.title("Bug Report Generator")
root.geometry("800x720")
root.configure(bg="#dbeafe")

# Centered container
container = ctk.CTkFrame(root, fg_color="#dbeafe", corner_radius=0)
container.pack(expand=True, fill="both")

# Card-style frame
card_frame = ctk.CTkFrame(container, fg_color="#ffffff", corner_radius=20)
card_frame.place(relx=0.5, rely=0.5, anchor="center")

# Heading
heading = ctk.CTkLabel(card_frame, text="🐞 Bug Report Generator", font=("Helvetica", 18, "bold"), text_color="#1e40af")
heading.pack(pady=15)

# Bug Title
title_label = ctk.CTkLabel(card_frame, text="Bug Title", font=("Arial", 12, "bold"))
title_label.pack(pady=(10, 0))

title_entry = ctk.CTkEntry(card_frame, width=400, height=40, font=("Arial", 12), corner_radius=15, border_width=1, border_color="#cbd5e1", fg_color="#f8fafc")
title_entry.pack(pady=(0, 10))

# Bug Description
desc_label = ctk.CTkLabel(card_frame, text="Bug Description", font=("Arial", 12, "bold"))
desc_label.pack()

desc_text = ctk.CTkTextbox(
    card_frame,
    width=400,
    height=130,
    font=("Arial", 12),
    corner_radius=15,
    border_width=1,
    border_color="#cbd5e1",
    fg_color="#f8fafc",
    text_color="black"
)
desc_text.pack(pady=(0, 10))

# Global variables
log_text = ""
log_label = None
screenshot_path = None
screenshot_label = None


def select_log_file():
    global log_text
    filepath = filedialog.askopenfilename(title="Select Log File", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if filepath:
        log_text = read_log_file(filepath)
        log_label.configure(text=os.path.basename(filepath), text_color="green")
    else:
        log_label.configure(text="No log file selected", text_color="red")


def take_or_upload_screenshot():
    global screenshot_path
    screenshot_choice = messagebox.askyesno("Screenshot Option", "Would you like to take an instant screenshot? (Click No to upload from your computer)")

    if screenshot_choice:
        screenshot = ImageGrab.grab()
        save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if save_path:
            screenshot.save(save_path)
            screenshot_path = save_path
            screenshot_label.configure(text="Screenshot saved!", text_color="green")
        else:
            screenshot_label.configure(text="No screenshot saved", text_color="red")
    else:
        screenshot_path = filedialog.askopenfilename(title="Select Screenshot", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])
        if screenshot_path:
            screenshot_label.configure(text=os.path.basename(screenshot_path), text_color="green")
        else:
            screenshot_label.configure(text="No screenshot selected", text_color="red")


def add_bug_to_report():
    title = title_entry.get()
    desc = desc_text.get("1.0", "end").strip()

    if not title or not desc or not log_text:
        messagebox.showwarning("Missing Data", "Please enter all fields and select a log file.")
        return

    add_bug(title, desc, log_text, screenshot_path)
    messagebox.showinfo("Added", "Bug added to the report list.")
    title_entry.delete(0, "end")
    desc_text.delete("1.0", "end")


def generate_final_report():
    all_bugs = get_all_bugs()
    if not all_bugs:
        messagebox.showwarning("No Bugs", "No bugs to report.")
        return

    file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
    if not file_path:
        messagebox.showwarning("No File Selected", "No file location selected, report generation canceled.")
        return

    generate_pdf(all_bugs, file_path)
    messagebox.showinfo("PDF Generated", f"Report saved to:\n{file_path}")


# Buttons
btn1 = ctk.CTkButton(card_frame, text="📁 Choose Log File", command=select_log_file, width=250, fg_color="#f9a8d4", text_color="black", hover_color="#f472b6")
btn1.pack(pady=5)

log_label = ctk.CTkLabel(card_frame, text="No log file selected", text_color="red")
log_label.pack()

btn2 = ctk.CTkButton(card_frame, text="🖼 Take or Upload Screenshot", command=take_or_upload_screenshot, width=250, fg_color="#a7f3d0", text_color="black", hover_color="#6ee7b7")
btn2.pack(pady=5)

screenshot_label = ctk.CTkLabel(card_frame, text="No screenshot selected", text_color="red")
screenshot_label.pack()

btn3 = ctk.CTkButton(card_frame, text="➕ Add to Report", command=add_bug_to_report, width=250, fg_color="#fde68a", text_color="black", hover_color="#facc15")
btn3.pack(pady=15)

btn4 = ctk.CTkButton(card_frame, text="📄 Generate PDF Report (All Bugs)", command=generate_final_report, width=250, fg_color="#fecaca", text_color="black", hover_color="#f87171")
btn4.pack(pady=10)

root.mainloop()
