import os
import subprocess
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

class VideoToAudioConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("MKV to Audio Converter")
        self.root.geometry("400x200")

        self.files = []
        self.cancel_flag = False

        self.label = tk.Label(root, text="Select MKV files to convert to audio format")
        self.label.pack()

        self.browse_button = tk.Button(root, text="Browse", command=self.browse_files)
        self.browse_button.pack()

        self.format_label = tk.Label(root, text="Select audio format:")
        self.format_label.pack()

        self.selected_format = tk.StringVar(value="mp3")
        self.mp3_button = tk.Radiobutton(root, text="MP3 (320kbps)", variable=self.selected_format, value="mp3")
        self.mp3_button.pack(anchor=tk.W)

        self.mp4_button = tk.Radiobutton(root, text="MP4 (AAC)", variable=self.selected_format, value="mp4")
        self.mp4_button.pack(anchor=tk.W)

        self.m4a_button = tk.Radiobutton(root, text="M4A (ALAC)", variable=self.selected_format, value="m4a")
        self.m4a_button.pack(anchor=tk.W)

        self.convert_button = tk.Button(root, text="Convert", command=self.start_conversion)
        self.convert_button.pack()

        self.cancel_button = tk.Button(root, text="Cancel", command=self.cancel_conversion, state=tk.DISABLED)
        self.cancel_button.pack()

    def browse_files(self):
        self.files = filedialog.askopenfilenames(filetypes=[("MKV Files", "*.mkv"), ("All Files", "*.*")])
        if self.files:
            self.label.config(text=f"{len(self.files)} files selected")

    def start_conversion(self):
        self.cancel_flag = False
        self.convert_button.config(state=tk.DISABLED)
        self.cancel_button.config(state=tk.NORMAL)

        threading.Thread(target=self.convert_files).start()

    def convert_files(self):
        if not self.files:
            self.show_message("No files selected", "Please select MKV files to convert.")
            self.reset_buttons()
            return

        total_files = len(self.files)
        for file in self.files:
            if self.cancel_flag:
                self.show_message("Conversion Cancelled", "The conversion process has been cancelled.")
                self.reset_buttons()
                return

            self.convert_to_audio(file)

        self.show_message("Conversion Complete", "All files have been converted.")
        self.reset_buttons()

    def convert_to_audio(self, input_file):
        format_selected = self.selected_format.get()
        output_file = os.path.splitext(input_file)[0] + f'.{format_selected}'
        command = ['ffmpeg', '-i', input_file]

        if format_selected == 'mp3':
            command += ['-b:a', '320k', output_file]
        elif format_selected == 'mp4':
            command += ['-c:a', 'aac', output_file]
        elif format_selected == 'm4a':
            command += ['-c:a', 'alac', output_file]

        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        process.communicate()

    def cancel_conversion(self):
        self.cancel_flag = True

    def reset_buttons(self):
        self.convert_button.config(state=tk.NORMAL)
        self.cancel_button.config(state=tk.DISABLED)

    def show_message(self, title, message):
        messagebox.showinfo(title, message)

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoToAudioConverter(root)
    root.mainloop()
