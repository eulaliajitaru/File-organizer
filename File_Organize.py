import os
import shutil
import time
import tkinter as tk
from tkinter import filedialog, messagebox
from collections import deque
import logging

logging.basicConfig(filename='file_organizer.log', level=logging.INFO,
                    format='%(asctime)s - %(message)s')

history = deque()

EXTENSION_MAP = {
    '.jpg': 'Images',
    '.jpeg': 'Images',
    '.png': 'Images',
    '.gif': 'Images',
    '.pdf': 'Documents',
    '.docx': 'Documents',
    '.txt': 'Text',
    '.mp3': 'Music',
    '.mp4': 'Videos',
    '.avi': 'Videos',
}

def organize_folder(folder_path):
    moved_files = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            src = os.path.join(root, file)
            ext = os.path.splitext(file)[1].lower()
            category = EXTENSION_MAP.get(ext, 'Others')
            dest_folder = os.path.join(folder_path, category)
            os.makedirs(dest_folder, exist_ok=True)
            dest = os.path.join(dest_folder, file)

            base, extension = os.path.splitext(file)
            counter = 1
            while os.path.exists(dest):
                dest = os.path.join(dest_folder, f"{base}_{counter}{extension}")
                counter += 1

            try:
                shutil.move(src, dest)
                moved_files.append((src, dest))
                logging.info(f"Moved: {src} -> {dest}")
            except Exception as e:
                logging.error(f"Error moving {src}: {e}")
                messagebox.showerror("Error", f"Error moving {file}: {e}")

    if moved_files:
        history.append(moved_files)

def undo_last():
    if not history:
        messagebox.showinfo("Undo", "Nothing to undo.")
        return

    moved_files = history.pop()
    for dest, src in reversed(moved_files):
        try:
            shutil.move(dest, src)
            logging.info(f"Undone: {dest} -> {src}")
        except Exception as e:
            logging.error(f"Error undoing move {dest}: {e}")
            messagebox.showerror("Undo Error", f"Error undoing move {dest}: {e}")


class FileOrganizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Organizer")

        self.label = tk.Label(root, text="Choose folder to organize:")
        self.label.pack(pady=5)

        self.path_entry = tk.Entry(root, width=50)
        self.path_entry.pack(pady=5)

        self.browse_button = tk.Button(root, text="Browse", command=self.browse_folder)
        self.browse_button.pack(pady=5)

        self.start_button = tk.Button(root, text="Start Organizing", command=self.start_organizing)
        self.start_button.pack(pady=5)

        self.undo_button = tk.Button(root, text="Undo Last Move", command=undo_last)
        self.undo_button.pack(pady=5)

    def browse_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, folder_selected)

    def start_organizing(self):
        folder_path = self.path_entry.get()
        if not folder_path or not os.path.isdir(folder_path):
            messagebox.showerror("Invalid Folder", "Please select a valid folder.")
            return
        organize_folder(folder_path)
        messagebox.showinfo("Done", "Files organized successfully.")

if __name__ == '__main__':
    root = tk.Tk()
    app = FileOrganizerApp(root)
    root.mainloop()
