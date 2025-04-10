from yt_dlp import YoutubeDL
from tqdm import tqdm
import os
import tkinter as tk
from tkinter import filedialog, messagebox

def download_video(video_url, download_path, resolution="highest"):
    try:
        ydl_opts = {
            'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s'),
            'format': 'bestaudio' if resolution == "audio" else 'best' if resolution == "highest" else f'best[height={resolution[:-1]}]',
        }
        
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)
            title = info.get('title', 'Unknown Title')
            print(f"Downloaded: {title}\n")
    except Exception as e:
        print(f"Error downloading {video_url}: {e}")

def download_playlist(playlist_url, download_path, resolution="highest"):
    try:
        ydl_opts = {
            'outtmpl': os.path.join(download_path, '%(playlist)s/%(title)s.%(ext)s'),
            'format': 'bestaudio' if resolution == "audio" else 'best' if resolution == "highest" else f'best[height={resolution[:-1]}]',
        }
        
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([playlist_url])
        
        print("Playlist download complete!")
    except Exception as e:
        print(f"Error downloading playlist: {e}")

def start_download():
    url = url_entry.get().strip()
    download_path = path_entry.get().strip() or os.getcwd()
    resolution = resolution_var.get()
    
    if not url:
        messagebox.showerror("Error", "Please enter a valid URL.")
        return
    
    if choice_var.get() == "1":
        download_video(url, download_path, resolution)
    elif choice_var.get() == "2":
        download_playlist(url, download_path, resolution)
    else:
        messagebox.showerror("Error", "Invalid choice!")

def browse_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        path_entry.delete(0, tk.END)
        path_entry.insert(0, folder_selected)

# GUI Setup
root = tk.Tk()
root.title("YouTube Downloader")

choice_frame = tk.Frame(root)
choice_frame.pack(pady=10)
choice_var = tk.StringVar(value="1")

single_video_rb = tk.Radiobutton(choice_frame, text="Single Video", variable=choice_var, value="1")
single_video_rb.grid(row=0, column=0, padx=5)

playlist_rb = tk.Radiobutton(choice_frame, text="Playlist", variable=choice_var, value="2")
playlist_rb.grid(row=0, column=1, padx=5)

url_label = tk.Label(root, text="YouTube URL:")
url_label.pack(anchor="w", padx=10)
url_entry = tk.Entry(root, width=50)
url_entry.pack(padx=10, pady=5)

resolution_label = tk.Label(root, text="Resolution (e.g., 720p, 480p, audio, or highest):")
resolution_label.pack(anchor="w", padx=10)
resolution_var = tk.StringVar(value="highest")
resolution_entry = tk.Entry(root, textvariable=resolution_var, width=50)
resolution_entry.pack(padx=10, pady=5)

path_label = tk.Label(root, text="Download Path:")
path_label.pack(anchor="w", padx=10)
path_entry = tk.Entry(root, width=50)
path_entry.pack(padx=10, pady=5)

browse_button = tk.Button(root, text="Browse", command=browse_folder)
browse_button.pack(pady=5)

download_button = tk.Button(root, text="Download", command=start_download)
download_button.pack(pady=20)

root.mainloop()
