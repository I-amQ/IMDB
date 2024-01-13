import base64
import io
import tkinter as tk
from tkinter import Toplevel, Label

from PIL import Image, ImageTk

import IMDB

#IMDB.scrape_data()
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
    movie_info_window.minsize(window_width, window_height)
    # Create a canvas and a vertical scrollbar attached to it
    vscrollbar = tk.Scrollbar(movie_info_window, orient='vertical')
    vscrollbar.pack(fill='y', side='right')

    canvas = tk.Canvas(movie_info_window, bg='gray', yscrollcommand=vscrollbar.set)
    canvas.pack(side='left', fill='both', expand=True)

    vscrollbar.config(command=canvas.yview)

    # Create a frame inside the canvas to hold the labels
    frame = tk.Frame(canvas, bg='gray')
    canvas.create_window((0,0), window=frame, anchor='nw')

    movies = IMDB.get_movies(id)

    heading_enum_label = Label(frame, text="No", font=("Helvetica Bold", 12), bg='black', fg='white')
    heading_enum_label.grid(row=0, column=0, sticky='w', padx=10, pady=10)

    heading_title_label = Label(frame, text="Movie Name", font=("Helvetica Bold", 12), bg='black', fg='white')
    heading_title_label.grid(row=0, column=1, sticky='w', padx=10, pady=10)

    heading_rating_label = Label(frame, text="Movie Rating", font=("Helvetica Bold", 12), bg='black', fg='white')
    heading_rating_label.grid(row=0, column=2, sticky='w', padx=10, pady=10)

    heading_year_label = Label(frame, text="Movie Year", font=("Helvetica Bold", 12), bg='black', fg='white')
    heading_year_label.grid(row=0, column=3, sticky='w', padx=10, pady=10)

    heading_genre_label = Label(frame, text="Movie Genre", font=("Helvetica Bold", 12), bg='black', fg='white')
    heading_genre_label.grid(row=0, column=4, sticky='w', padx=10, pady=10)


    # Create labels for each movie and place them in the grid
    for i, movie in enumerate(movies, start=1):

        enum_label = Label(frame, text=str(i)+".", font=("Helvetica Bold", 12), bg='black', fg='white')
        enum_label.grid(row=i, column=0, sticky='w', padx=10, pady=10)

        # Create a label for the movie title
        title_label = Label(frame, text=movie[1], font=("Helvetica", 12), bg='black', fg='white')
        title_label.grid(row=i, column=1, sticky='w', padx=10, pady=10)

        # Create a label for the movie rating
        rating_label = Label(frame, text=movie[2], font=("Helvetica", 12), bg='black', fg='white')
        rating_label.grid(row=i, column=2, sticky='w', padx=10, pady=10)

        # Create a label for the movie year
        year_label = Label(frame, text=movie[3], font=("Helvetica", 12), bg='black', fg='white')
        year_label.grid(row=i, column=3, sticky='w', padx=10, pady=10)

        # Create a label for the movie genre
        genre_label = Label(frame, text=movie[4], font=("Helvetica", 12), bg='black', fg='white')
        genre_label.grid(row=i, column=4, sticky='w', padx=10, pady=10)

    # Update scrollregion after starting 'mainloop'
    # when all widgets are in canvas
    frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox('all'))

def on_select_genres(id):
    genres = IMDB.get_genre(id)  

    genre_window = Toplevel(root)
    genre_window.title(IMDB.show_name(id) + "'s Genres")
    genre_window.minsize(200, 250)

    # Add a label for each genre
    for genre in genres:
        label = tk.Label(genre_window, text=genre)
        label.pack()

def on_select_awards(id):
    awards = IMDB.get_awards(id)

    awards_window = tk.Toplevel(root)
    awards_window.title(IMDB.show_name(id) + "'s Awards")
    awards_window.minsize(window_width, window_height)

    # Create a canvas and a vertical scrollbar attached to it
    vscrollbar = tk.Scrollbar(awards_window, orient='vertical')
    vscrollbar.pack(fill='y', side='right')

    canvas = tk.Canvas(awards_window, bg='gray', yscrollcommand=vscrollbar.set)
    canvas.pack(side='left', fill='both', expand=True)

    vscrollbar.config(command=canvas.yview)

    # Create a frame inside the canvas to hold the labels
    frame = tk.Frame(canvas, bg='gray')
    canvas.create_window((0,0), window=frame, anchor='nw')

    heading_enum = Label(frame, text="No.", font=("Helvetica Bold", 12), bg='black', fg='white')
    heading_enum.grid(row=0, column=0, sticky='w', padx=10, pady=10)

    heading_award = Label(frame, text="Awards", font=("Helvetica Bold", 12), bg='black', fg='white')
    heading_award.grid(row=0, column=1, sticky='w', padx=10, pady=10)
    

    # Add a label for each award
    for i,award in enumerate(awards, start = 1):
        
        enum_lable = tk.Label(frame, text=str(i), anchor='center')
        label = tk.Label(frame, text=award, anchor='center')
        #label.pack(pady=10, expand=True)  # Add vertical padding

        enum_lable.grid(row=i, column=0,sticky='w', padx=10, pady=10)
        label.grid(row=i, column=1,sticky='w', padx=10, pady=10)
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)

    # Update scrollregion after starting 'mainloop'
    # when all widgets are in canvas
    frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox('all'))


def on_select_top_10(id):

    top10 = IMDB.get_top10(id)
    movie_titles,movie_ratings = top10


    top10_window = tk.Toplevel(root)
    top10_window.title(IMDB.show_name(id) + "'s Top 10 Movies")
    top10_window.minsize(window_width, window_height)

    # Create a canvas and a vertical scrollbar attached to it
    vscrollbar = tk.Scrollbar(top10_window, orient='vertical')
    vscrollbar.pack(fill='y', side='right')

    canvas = tk.Canvas(top10_window, bg='gray', yscrollcommand=vscrollbar.set)
    canvas.pack(side='left', fill='both', expand=True)

    vscrollbar.config(command=canvas.yview)

    # Create a frame inside the canvas to hold the labels
    frame = tk.Frame(canvas, bg='gray')
    canvas.create_window((0,0), window=frame, anchor='nw')

    heading_enum = Label(frame, text="No.", font=("Helvetica Bold", 12), bg='black', fg='white')
    heading_enum.grid(row=0, column=0, sticky='w', padx=10, pady=10)

    heading_title = Label(frame, text="Movie Title", font=("Helvetica Bold", 12), bg='black', fg='white')
    heading_title.grid(row=0, column=1, sticky='w', padx=10, pady=10)

    heading_rating = Label(frame, text="Movie Rating", font=("Helvetica Bold", 12), bg='black', fg='white')
    heading_rating.grid(row=0, column=2, sticky='w', padx=10, pady=10)
    

    # Add a label for each award
    for i, movie_title in enumerate(movie_titles, start = 0):

        movie_rating = movie_ratings[i]
        
        enum_label = tk.Label(frame, text=str(i+1), anchor='center')
        title_label = tk.Label(frame, text=movie_title, anchor='center')
        rating_label = tk.Label(frame, text=movie_rating, anchor='center')
        #label.pack(pady=10, expand=True)  # Add vertical padding

        enum_label.grid(row=i+1, column=0,sticky='w', padx=10, pady=10)
        title_label.grid(row=i+1, column=1,sticky='w', padx=10, pady=10)
        rating_label.grid(row=i+1, column=2,sticky='w', padx=10, pady=10)
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)

    # Update scrollregion after starting 'mainloop'
    # when all widgets are in canvas
    frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox('all'))




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

    average_rating_label = tk.Label(info_window,text="Average Rating: " + str(IMDB.get_average_rating(id))[0:5],fg="YELLOW", bg="Black", font=("Helvetica Bold", 12))
    average_rating_label.pack()


    button_frame = tk.Frame(info_window)
    button_frame.pack()

    movies_button = tk.Button(button_frame, text="Movies", command=lambda: on_select_movies(id))
    movies_button.pack(side=tk.LEFT)

    genres_button = tk.Button(button_frame, text="Genres", command=lambda: on_select_genres(id))
    genres_button.pack(side=tk.LEFT)

    awards_button = tk.Button(button_frame, text="Awards", command=lambda: on_select_awards(id))
    awards_button.pack(side=tk.LEFT)

    top10_button = tk.Button(button_frame, text="TOP_10", command=lambda: on_select_top_10(id))
    top10_button.pack(side=tk.LEFT)

    text = tk.Text(info_window, wrap='word', font=("Helvetica", 12), bg='black',
                   fg='white')  # Set the background and foreground color of the text widget
    text.insert('end', description,'both')
    text.configure(state='disabled')
    text.pack(expand=True, fill='both')
    text.tag_configure("center", justify='center')




frame = tk.Frame(root, bg='yellow')  # Set the background color of the frame
frame.place(relx=0.5, rely=0.5, anchor='center')  # Use place instead of pack

for i, actor in enumerate(actors,start=1):
    name = actor
    text = str(i) + '. ' + name
    button = tk.Button(frame, text=text, command=lambda id=i: on_select(id))  # Add the button to the frame
    button.grid(row=(i-1) // 5, column=(i-1) % 5, padx=10, pady=10)  # Add margins to the buttons

root.mainloop()