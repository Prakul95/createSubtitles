import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox 
import subprocess
from helperFunctions import callBashFunction

def generate_subtitles(arg="HelloFromPython"):
    if not selected_files:
        messagebox.showwarning("No Files Selected", "Please select files first.")
        return

    try:
        language = language_var.get()
        beam_size = int(beam_size_var.get())
        word_timestamps = word_timestamps_var.get()
    except ValueError:
        messagebox.showerror("Invalid Input", "Beam size must be an integer.")
        return

    progress["maximum"] = len(selected_files)
    progress["value"] = 0

    completed = []
    for i, file in enumerate(selected_files):
        try:
            input_path = file
            output = callBashFunction(backend_var.get(),model_size_var.get(), input_path=input_path, language=language, task="transcribe" )
            # output = transcribe_to_srt(file, lang, beam_size, word_timestamps)
            if output:
                completed.append(output)
        except Exception as e:
            print(f"Error processing {file}: {e}")
        progress["value"] = i + 1
        root.update_idletasks()

    messagebox.showinfo("Done", f"Generated {len(completed)} subtitle files.")
    
    
    

def choose_files():
    global selected_files
    selected_files = filedialog.askopenfilenames(
        title="Select Audio or Video Files",
        filetypes=[("Audio/Video Files", "*.mp3 *.wav *.m4a *.mp4 *.mov *.mkv *.avi")]
    )
    file_count.set(f"{len(selected_files)} files selected")

# Create the main window
root = tk.Tk()
root.title("Whisper Subtitle Generator")
root.geometry("500x400")

# Backend dropdown
tk.Label(root, text="Select Backend").pack(pady=(10, 0))
backend_var = tk.StringVar()
backend_dropdown = ttk.Combobox(root, textvariable=backend_var, state="readonly", width=20)
backend_dropdown["values"] = ["whisper", "faster-whisper"]
backend_dropdown.current(0)
backend_dropdown.pack(pady=5)

tk.Label(root, text="Select model size").pack(pady=(10, 0))
model_size_var = tk.StringVar()
model_size_dropdown = ttk.Combobox(root, textvariable=model_size_var, state="readonly", width=20)
model_size_dropdown["values"] = ["large", "small", "base", "turbo"]
model_size_dropdown.current(0)
model_size_dropdown.pack(pady=5)


tk.Label(root, text="Select Language").pack(pady=(10, 0))
language_var = tk.StringVar()
language_dropdown = ttk.Combobox(root, textvariable=language_var, state="readonly", width=20)
language_dropdown["values"] = ["en", "hi", "es", "fr", "de", "zh", "ja", "ru"]
language_dropdown.current(0)
language_dropdown.pack(pady=5)

# Beam size dropdown
tk.Label(root, text="Select Beam Size").pack(pady=(10, 0))
beam_size_var = tk.StringVar()
beam_dropdown = ttk.Combobox(root, textvariable=beam_size_var, state="readonly", width=5)
beam_dropdown["values"] = [str(i) for i in range(1, 11)]
beam_dropdown.current(4)
beam_dropdown.pack(pady=4)

# Word timestamps checkbox
word_timestamps_var = tk.BooleanVar(value=False)
tk.Checkbutton(root, text="Enable Word Timestamps", variable=word_timestamps_var).pack(pady=7)

# File selection label
file_count = tk.StringVar(value="No files selected")
tk.Label(root, textvariable=file_count).pack(pady=5)

# Buttons
tk.Button(root, text="Choose Files", command=choose_files).pack(pady=15)
tk.Button(root, text="Generate Subtitles", command=generate_subtitles).pack(pady=20)

# Progress bar
progress = ttk.Progressbar(root, orient="horizontal", length=350, mode="determinate")
progress.pack(pady=20)

root.mainloop()
