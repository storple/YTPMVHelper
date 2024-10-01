import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import os

def start():
    # Create the main application window
    root = tk.Tk()
    root.title("YTPMV Helper GUI")
    root.geometry("600x500")
    root.resizable(False, False)

    # Variables to hold the folder paths and parameters
    midi_folder_path = tk.StringVar()
    video_folder_path = tk.StringVar()
    output_filename = tk.StringVar()
    bpm = tk.StringVar(value="120")  # Default value
    tpb = tk.StringVar(value="96")   # Default value
    frame_rate = tk.StringVar(value="60")  # Default value

    # Function to select the MIDI folder
    def select_midi_folder():
        folder_path = filedialog.askdirectory(title="Select MIDI Folder")
        if folder_path:
            midi_folder_path.set(folder_path)

    # Function to select the video folder
    def select_video_folder():
        folder_path = filedialog.askdirectory(title="Select Video Folder")
        if folder_path:
            video_folder_path.set(folder_path)

    # Function to select the output filename
    def select_output_filename():
        folder_path = filedialog.askdirectory(title="Select Output Folder")
        if folder_path:
            output_filename.set(folder_path)

    # Function to run the YTPMV Helper script
    def run_ytpmv_helper():
        # Make sure both folders are selected
        if not midi_folder_path.get() or not video_folder_path.get():
            messagebox.showerror("Error", "Please select both MIDI and video folders.")
            return

        # Make sure the output folder is selected
        if not output_filename.get():
            messagebox.showerror("Error", "Please select the output folder.")
            return

        # Build the command to run the YTPMV Helper program
        command = [
            "python", "YTPMVHelper.py",  # Change this to the path of your script if needed
            "--midi-folder", midi_folder_path.get(),
            "--video-folder", video_folder_path.get(),
            "--bpm", bpm.get(),
            "--tpb", tpb.get(),
            "--frame-rate", frame_rate.get(),
            "--output-filename", output_filename.get()
        ]

        try:
            # Run the command and capture output
            result = subprocess.run(command, capture_output=True, text=True)
            output_box.insert(tk.END, f"{result.stdout}\n\n")
            if result.stderr:
                output_box.insert(tk.END, f"Errors:\n{result.stderr}\n\n")
        except Exception as e:
            messagebox.showerror("Execution Error", str(e))

    # GUI Layout
    # Folder Selection
    tk.Label(root, text="MIDI Folder:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
    tk.Entry(root, textvariable=midi_folder_path, width=50).grid(row=0, column=1, padx=10, pady=10)
    tk.Button(root, text="Browse...", command=select_midi_folder).grid(row=0, column=2, padx=10, pady=10)

    tk.Label(root, text="Video Folder:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
    tk.Entry(root, textvariable=video_folder_path, width=50).grid(row=1, column=1, padx=10, pady=10)
    tk.Button(root, text="Browse...", command=select_video_folder).grid(row=1, column=2, padx=10, pady=10)

    tk.Label(root, text="Output Filename:").grid(row=2, column=0, padx=10, pady=10, sticky="e")
    tk.Entry(root, textvariable=output_filename, width=50).grid(row=2, column=1, padx=10, pady=10)
    tk.Button(root, text="Browse...", command=select_output_filename).grid(row=2, column=2, padx=10, pady=10)

    # Parameter Inputs
    tk.Label(root, text="BPM:").grid(row=3, column=0, padx=10, pady=10, sticky="e")
    tk.Entry(root, textvariable=bpm, width=10).grid(row=3, column=1, padx=10, pady=10, sticky="w")

    tk.Label(root, text="Ticks Per Beat:").grid(row=4, column=0, padx=10, pady=10, sticky="e")
    tk.Entry(root, textvariable=tpb, width=10).grid(row=4, column=1, padx=10, pady=10, sticky="w")

    tk.Label(root, text="Frame Rate:").grid(row=5, column=0, padx=10, pady=10, sticky="e")
    tk.Entry(root, textvariable=frame_rate, width=10).grid(row=5, column=1, padx=10, pady=10, sticky="w")

    # Run Button
    tk.Button(root, text="Run YTPMV Helper", command=run_ytpmv_helper, bg="green", fg="white").grid(row=6, column=1, padx=10, pady=20)

    # Output Display Box
    output_box = tk.Text(root, height=10, width=70)
    output_box.grid(row=7, column=0, columnspan=3, padx=10, pady=10)

    # Start the main loop
    root.mainloop()
