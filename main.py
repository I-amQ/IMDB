import base64
import io
import tkinter as tk
from tkinter import Toplevel

from PIL import Image, ImageTk

import IMDB

IMDB.scrape_data()
actors = IMDB.list_actors()

root = tk.Tk()
root.title("IMDb Actors and Actresses")
root.configure(background='yellow')

# Get screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Set window size to 50% of screen size
window_width = int(screen_width * 0.5)
window_height = int(screen_height * 0.5)

# Center the window
position_top = int(screen_height / 2 - window_height / 2)
position_right = int(screen_width / 2 - window_width / 2)

root.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")


def on_select_movies(id):

    # Create new window to show actor movies
    movie_info_window = Toplevel(root)
    movie_info_window.title(IMDB.show_name(id) + "'s movies")
    movie_info_window.configure(background='Gray')  # Set the background color of the info window

    movies = IMDB.get_movies(id)

    text = tk.Text(movie_info_window, wrap='word', font=("Helvetica", 12), bg='black',
                   fg='white')  # Set the background and foreground color of the text widget
    for i, movie in enumerate(movies):
        text.insert('end', str(i) + ". " + movie + "\n\n\n")
    text.configure(state='disabled')
    text.pack(expand=True, fill='both')
    text.tag_configure("center", justify='center')


def on_select(id):

    description = IMDB.show_info(id)
    img_str = IMDB.show_image(id)

    # Create new window to show actor info
    info_window = Toplevel(root)
    info_window.title(IMDB.show_name(id))
    info_window.configure(background='Gray')  # Set the background color of the info window

    # Convert the base64 string back to an image
    img_data = base64.b64decode(img_str)
    img = Image.open(io.BytesIO(img_data))

    # Resize the image while maintaining aspect ratio
    max_size = (250, 250)
    img.thumbnail(max_size, Image.Resampling.LANCZOS)
    img = ImageTk.PhotoImage(img)

    # Create a label and add the image to it
    label = tk.Label(info_window, image=img)
    label.image = img  # Keep a reference to the image
    label.pack()

    button_frame = tk.Frame(info_window)
    button_frame.pack()

    movies_button = tk.Button(button_frame, text="Movies", command=lambda: on_select_movies(id))
    movies_button.pack(side=tk.LEFT)

    movies_button = tk.Button(button_frame, text="Genres")
    movies_button.pack(side=tk.LEFT)

    movies_button = tk.Button(button_frame, text="Awards")
    movies_button.pack(side=tk.LEFT)

    text = tk.Text(info_window, wrap='word', font=("Helvetica", 12), bg='black',
                   fg='white')  # Set the background and foreground color of the text widget
    text.insert('end', description)
    text.configure(state='disabled')
    text.pack(expand=True, fill='both')
    text.tag_configure("center", justify='center')




frame = tk.Frame(root, bg='yellow')  # Set the background color of the frame
frame.place(relx=0.5, rely=0.5, anchor='center')  # Use place instead of pack

for i, actor in enumerate(actors):
    name = actor
    text = str(i+1) + '. ' + name
    button = tk.Button(frame, text=text, command=lambda id=i+1: on_select(id))  # Add the button to the frame
    button.grid(row=i // 5, column=i % 5, padx=10, pady=10)  # Add margins to the buttons

root.mainloop()