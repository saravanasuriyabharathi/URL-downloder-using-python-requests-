import os
import requests
from tkinter import Tk, Label, Entry, Button, filedialog, messagebox, StringVar, PhotoImage
from tkinter.ttk import Progressbar, Style
from PIL import Image, ImageTk

def download_file():
    url = url_entry.get()
    if not url:
        messagebox.showerror("Error", "Please enter a URL.")
        return

    save_path = filedialog.askdirectory()
    if not save_path:
        messagebox.showinfo("Cancelled", "Download cancelled.")
        return

    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()

        file_name = os.path.join(save_path, url.split("/")[-1])
        total_size = int(response.headers.get('content-length', 0))
        downloaded_size = 0

        with open(file_name, 'wb') as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
                downloaded_size += len(chunk)
                progress_var.set(int((downloaded_size / total_size) * 100))
                progress_bar.update()

        messagebox.showinfo("Success", f"File downloaded successfully: {file_name}")
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Download Error", f"An error occurred: {e}")
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")
    finally:
        progress_var.set(0)


root = Tk()
root.title("URL Downloader")
root.geometry("600x400")
root.resizable(False, False)


bg_image = Image.open("backround.jpg")  # Load the image
bg_image = bg_image.resize((600, 400), Image.Resampling.LANCZOS)
 # Resize to fit window
bg_photo = ImageTk.PhotoImage(bg_image)  # Convert to PhotoImage

bg_label = Label(root, image=bg_photo)
bg_label.place(relwidth=1, relheight=1)  #
# Styling
style = Style()
style.configure("TButton", font=("Arial", 12), padding=6, background="#4CAF50", foreground="white")
style.configure("TLabel", background="#f0f0f0", font=("Arial", 12))
style.configure("TProgressbar", troughcolor="#d9d9d9", background="#4CAF50")

# Transparent Background Labels
transparent_bg = "#f0f0f0"

# Widgets
title_label = Label(
    root,
    text="URL Downloader",
    font=("Arial", 20, "bold"),
    bg=transparent_bg,
    fg="black"
)
title_label.pack(pady=10)

Label(root, text="Enter URL:", font=("Arial", 14, "bold"), bg=transparent_bg).pack(pady=10)
url_entry = Entry(root, width=50, font=("Arial", 12))
url_entry.pack(pady=5)

progress_var = StringVar()
progress_var.set(0)
progress_bar = Progressbar(root, orient="horizontal", length=400, mode="determinate", variable=progress_var)
progress_bar.pack(pady=20)

download_button = Button(root, text="Download", font=("Arial", 12), bg="#4CAF50", fg="white", command=download_file)
download_button.pack(pady=10)

footer_label = Label(
    root,
    text="URL Downloader App © 2024",
    font=("Arial", 10, "italic"),
    bg=transparent_bg,
    fg="gray"
)
footer_label.pack(side="bottom", pady=10)

# Run the application
root.mainloop()
