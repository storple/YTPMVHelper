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


    # Variables to hold the file paths and parameters
    midi_file_path = tk.StringVar()
    video_file_path = tk.StringVar()
    output_file_name = tk.StringVar(value="Timeline")
    bpm = tk.StringVar(value="120")  # Default value
    tpb = tk.StringVar(value="96")   # Default value
    frame_rate = tk.StringVar(value="60")  # Default value

    # Function to select the MIDI file
    def select_midi_file():
        file_path = filedialog.askopenfilename(title="Select MIDI File", filetypes=[("MIDI Files", "*.mid")])
        if file_path:
            midi_file_path.set(file_path)

    # Function to select the video file
    def select_video_file():
        file_path = filedialog.askopenfilename(title="Select Video File", filetypes=[("Video Files", "*.mov *.mp4")])
        if file_path:
            video_file_path.set(file_path)

    # Function to run the YTPMV Helper script
    def run_ytpmv_helper():
        # Make sure both files are selected
        if not midi_file_path.get() or not video_file_path.get():
            messagebox.showerror("Error", "Please select both MIDI and video files.")
            return

        # Build the command to run the YTPMV Helper program
        command = [
            "python", "YTPMVHelper.py",  # Change this to the path of your script if needed
            "--midi", midi_file_path.get(),
            "--video", video_file_path.get(),
            "--bpm", bpm.get(),
            "--tpb", tpb.get(),
            "--frame-rate", frame_rate.get(),
            "--output", output_file_name.get()
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
    # File Selection
    tk.Label(root, text="MIDI File:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
    tk.Entry(root, textvariable=midi_file_path, width=50).grid(row=0, column=1, padx=10, pady=10)
    tk.Button(root, text="Browse...", command=select_midi_file).grid(row=0, column=2, padx=10, pady=10)

    tk.Label(root, text="Video File:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
    tk.Entry(root, textvariable=video_file_path, width=50).grid(row=1, column=1, padx=10, pady=10)
    tk.Button(root, text="Browse...", command=select_video_file).grid(row=1, column=2, padx=10, pady=10)

    # Parameter Inputs
    tk.Label(root, text="BPM:").grid(row=2, column=0, padx=10, pady=10, sticky="e")
    tk.Entry(root, textvariable=bpm, width=10).grid(row=2, column=1, padx=10, pady=10, sticky="w")

    tk.Label(root, text="Ticks Per Beat:").grid(row=3, column=0, padx=10, pady=10, sticky="e")
    tk.Entry(root, textvariable=tpb, width=10).grid(row=3, column=1, padx=10, pady=10, sticky="w")

    tk.Label(root, text="Frame Rate:").grid(row=4, column=0, padx=10, pady=10, sticky="e")
    tk.Entry(root, textvariable=frame_rate, width=10).grid(row=4, column=1, padx=10, pady=10, sticky="w")

    tk.Label(root, text="Output Filename:").grid(row=5, column=0, padx=10, pady=10, sticky="e")
    tk.Entry(root, textvariable=output_file_name, width=50).grid(row=5, column=1, padx=10, pady=10)

    # Run Button
    tk.Button(root, text="Run YTPMV Helper", command=run_ytpmv_helper, bg="green", fg="white").grid(row=6, column=1, padx=10, pady=20)

    # Output Display Box
    output_box = tk.Text(root, height=10, width=70)
    output_box.grid(row=7, column=0, columnspan=3, padx=10, pady=10)

    # Start the main loop
    root.mainloop()