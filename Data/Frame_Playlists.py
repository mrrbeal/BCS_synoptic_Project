import tkinter as tk
from tkinter import Tk, ttk

class Playlists(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is page 1", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go to the stsqsqsqsart page",
                           command=lambda: controller.show_frame("PageOne"),  bg=controller.colourPalette["darkblue"], fg="White")
        button.pack()

        tk.Button(controller.playlist_frame.inner_frame, text="Add New Playlist",
                           command=lambda: controller.show_frame("PageOne"), bg=controller.colourPalette["darkblue"], fg="White").grid(row=0, column=0,columnspan=2,sticky='ew')