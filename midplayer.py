#!/usr/bin/env python3

import vlc
import tkinter as tk
from tkinter import filedialog, messagebox
import os
import sys
import time

class AdoboMidPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Adobo Mid Player")
        self.root.geometry("800x600")
        
        # Initialize VLC instance
        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()
        
        # Variables
        self.current_file = None
        self.is_playing = False
        self.is_video = False
        
        # Create GUI elements
        self.create_widgets()
        
        # Bind window close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_widgets(self):
        # Video frame
        self.video_frame = tk.Frame(self.root, bg="black")
        self.video_frame.pack(fill=tk.BOTH, expand=True)

        # Control frame
        control_frame = tk.Frame(self.root)
        control_frame.pack(fill=tk.X, pady=5)

        # Buttons
        self.play_button = tk.Button(control_frame, text="Play", command=self.play_pause)
        self.play_button.pack(side=tk.LEFT, padx=5)

        self.stop_button = tk.Button(control_frame, text="Stop", command=self.stop)
        self.stop_button.pack(side=tk.LEFT, padx=5)

        self.open_button = tk.Button(control_frame, text="Open File", command=self.open_file)
        self.open_button.pack(side=tk.LEFT, padx=5)

        # Volume control
        self.volume_label = tk.Label(control_frame, text="Volume:")
        self.volume_label.pack(side=tk.LEFT, padx=5)
        
        self.volume_scale = tk.Scale(control_frame, from_=0, to=100, 
                                   orient=tk.HORIZONTAL, command=self.set_volume)
        self.volume_scale.set(70)
        self.volume_scale.pack(side=tk.LEFT, padx=5)

        # Position slider
        self.position_scale = tk.Scale(control_frame, from_=0, to=100, 
                                     orient=tk.HORIZONTAL, command=self.set_position)
        self.position_scale.pack(fill=tk.X, padx=5, pady=5)

        # Status label
        self.status_label = tk.Label(self.root, text="No media loaded")
        self.status_label.pack(pady=5)

        # Update position slider
        self.root.after(1000, self.update_position)

    def open_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[
                ("Media files", "*.mp3 *.ogg *.m4a *.mov *.mp4 *.avi *.mkv *.flv *.wmv"),
                ("All files", "*.*")
            ]
        )
        if file_path:
            self.current_file = file_path
            media = self.instance.media_new(file_path)
            self.player.set_media(media)
            
            # Check if it's a video by looking at file extension
            video_extensions = ['.mov', '.mp4', '.avi', '.mkv', '.flv', '.wmv']
            self.is_video = any(file_path.lower().endswith(ext) for ext in video_extensions)
            
            if self.is_video:
                self.player.set_hwnd(self.video_frame.winfo_id())
            
            self.status_label.config(text=f"Loaded: {os.path.basename(file_path)}")
            self.play()

    def play(self):
        if self.current_file and not self.is_playing:
            self.player.play()
            self.is_playing = True
            self.play_button.config(text="Pause")
            self.status_label.config(text=f"Playing: {os.path.basename(self.current_file)}")

    def pause(self):
        if self.is_playing:
            self.player.pause()
            self.is_playing = False
            self.play_button.config(text="Play")
            self.status_label.config(text=f"Paused: {os.path.basename(self.current_file)}")

    def play_pause(self):
        if self.is_playing:
            self.pause()
        else:
            self.play()

    def stop(self):
        self.player.stop()
        self.is_playing = False
        self.play_button.config(text="Play")
        self.status_label.config(text="Stopped")
        self.position_scale.set(0)

    def set_volume(self, val):
        self.player.audio_set_volume(int(float(val)))

    def set_position(self, val):
        pos = float(val) / 100
        self.player.set_position(pos)

    def update_position(self):
        if self.is_playing:
            pos = self.player.get_position() * 100
            self.position_scale.set(pos)
        self.root.after(1000, self.update_position)

    def on_closing(self):
        self.stop()
        self.instance.release()
        self.root.destroy()

def main():
    # Check if VLC is installed
    try:
        vlc.Instance()
    except NameError:
        messagebox.showerror("Error", "VLC Python bindings not found.\nPlease install python-vlc")
        sys.exit(1)

    root = tk.Tk()
    app = AdoboMidPlayer(root)
    root.mainloop()

if __name__ == "__main__":
    main()