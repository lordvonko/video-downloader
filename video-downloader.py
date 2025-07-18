import os
import threading
import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog, messagebox
import yt_dlp

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")


class VideoDownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Downloader")
        self.root.geometry("600x500")

        # Default save directory
        self.save_dir = os.path.expanduser("~/Downloads")

        # Cookies file (optional)
        self.cookies_file = None

        # Main frame
        self.main_frame = ctk.CTkFrame(root)
        self.main_frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Title
        title_label = ctk.CTkLabel(
            self.main_frame, text="▷ Video Downloader", font=("Helvetica", 24, "bold")
        )
        title_label.pack(pady=20)

        # URL input
        url_frame = ctk.CTkFrame(self.main_frame)
        url_frame.pack(fill="x", pady=10)
        url_icon = ctk.CTkLabel(url_frame, text="🔗 ", font=("Helvetica", 16))
        url_icon.pack(side="left")
        self.url_entry = ctk.CTkEntry(
            url_frame, placeholder_text="Enter Video URL", font=("Helvetica", 12)
        )
        self.url_entry.pack(side="left", fill="x", expand=True, padx=5)

        # Save directory
        self.dir_button = ctk.CTkButton(
            self.main_frame,
            text="📁 Select Download Folder",
            command=self.select_directory,
            font=("Helvetica", 12),
        )
        self.dir_button.pack(pady=10)
        self.dir_label = ctk.CTkLabel(
            self.main_frame, text=f"Save to: {self.save_dir}", font=("Helvetica", 10)
        )
        self.dir_label.pack(pady=5)

        # Cookies (collapsible)
        self.cookies_var = tk.BooleanVar(value=False)
        self.cookies_switch = ctk.CTkSwitch(
            self.main_frame,
            text="🍪 Load Cookies File",
            variable=self.cookies_var,
            command=self.toggle_cookies,
            font=("Helvetica", 12),
        )
        self.cookies_switch.pack(pady=10)
        self.cookies_frame = ctk.CTkFrame(
            self.main_frame, border_width=2, border_color="#00C9FF"
        )
        self.cookies_button = ctk.CTkButton(
            self.cookies_frame,
            text="Select Cookies File",
            command=self.select_cookies_file,
            font=("Helvetica", 12),
        )
        self.cookies_button.pack(pady=5, fill="x")
        self.cookies_label = ctk.CTkLabel(
            self.cookies_frame, text="", font=("Helvetica", 10)
        )

        # Download button
        self.download_button = ctk.CTkButton(
            self.main_frame,
            text="▷ Download Video",
            command=self.start_download,
            fg_color="#00C9FF",
            text_color="#000000",
            font=("Helvetica", 16, "bold"),
            hover_color="#00A0CC",
        )
        self.download_button.pack(pady=20)

        # Status text area
        self.status_text = ctk.CTkTextbox(
            self.main_frame, height=120, font=("Consolas", 10)
        )
        self.status_text.pack(fill="both", expand=True)
        self.status_text.insert("0.0", "[INFO] Ready.\n[INFO] Waiting for URL...\n")
        self.status_text.configure(state="disabled")

    def toggle_cookies(self):
        """Toggle visibility of cookies file selection."""
        if self.cookies_var.get():
            self.cookies_frame.pack(after=self.cookies_switch, pady=10, fill="x")
        else:
            self.cookies_frame.pack_forget()
            self.cookies_file = None
            self.cookies_label.configure(text="")
            self.cookies_label.pack_forget()

    def select_directory(self):
        """Open file dialog to select save directory."""
        selected_dir = filedialog.askdirectory()
        if selected_dir:
            self.save_dir = selected_dir
            self.dir_label.configure(text=f"Save to: {self.save_dir}")

    def select_cookies_file(self):
        """Open file dialog to select cookies file."""
        selected_file = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if selected_file:
            self.cookies_file = selected_file
            self.cookies_label.configure(
                text=f"Cookies File: {os.path.basename(self.cookies_file)}"
            )
            self.cookies_label.pack(pady=5)
        else:
            self.cookies_file = None
            self.cookies_label.configure(text="")
            self.cookies_label.pack_forget()

    def start_download(self):
        """Validate input and start download in a separate thread."""
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showerror("Error", "Please enter a valid URL.")
            return

        # Clear status text
        self.status_text.configure(state="normal")
        self.status_text.delete("0.0", "end")
        self.status_text.configure(state="disabled")

        # Disable download button during download
        self.download_button.configure(state="disabled")

        # Start download in thread
        threading.Thread(target=self.download_video, args=(url,), daemon=True).start()

    def download_video(self, url):
        """Download the video using yt-dlp."""
        try:
            ydl_opts = {
                "format": "bestvideo+bestaudio/best",
                "outtmpl": os.path.join(self.save_dir, "%(title)s.%(ext)s"),
                "progress_hooks": [self.progress_hook],
                "concurrent_fragment_downloads": 8,  # Increase concurrent fragments for faster download without losing quality
            }
            if self.cookies_file:
                ydl_opts["cookiefile"] = self.cookies_file

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            self.root.after(
                0, lambda: messagebox.showinfo("Success", "Download completed!")
            )
        except Exception as e:
            error_msg = str(e)
            self.update_status(f"Error: {error_msg}\n")
            self.root.after(
                0,
                lambda: messagebox.showerror("Error", f"Download failed: {error_msg}"),
            )
        finally:
            # Re-enable download button
            self.root.after(0, lambda: self.download_button.configure(state="normal"))

    def progress_hook(self, d):
        """Hook to update progress in GUI."""
        if d["status"] == "downloading":
            progress = f"Downloading: {d['_percent_str']} | ETA: {d['_eta_str']} | Speed: {d['_speed_str']}\n"
            self.update_status(progress)
        elif d["status"] == "finished":
            self.update_status("Download finished, processing...\n")

    def update_status(self, message):
        """Update status text in GUI thread-safely."""
        self.root.after(0, lambda: self._update_status(message))

    def _update_status(self, message):
        """Internal method to update status text."""
        self.status_text.configure(state="normal")
        self.status_text.insert("end", message)
        self.status_text.see("end")
        self.status_text.configure(state="disabled")


if __name__ == "__main__":
    root = ctk.CTk()
    app = VideoDownloaderApp(root)
    root.mainloop()

