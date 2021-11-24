import tkinter as tk
from tkinter import Tk, ttk

class Playlists(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.grid_propagate(False)
        self.config(width=1000,height=600,borderwidth=2,relief="solid")
        self.searchBar = tk.Entry(self,font=("helvetica",16))
        self.searchBar.grid(column=0,row=0,columnspan=3, pady=25,padx= 50)
        self.searchBar.insert(0, 'Search Files')
        self.searchBar.bind("<FocusIn>", lambda args: self.searchBar.delete('0', 'end'))
        self.searchBar.bind("<KeyRelease>", lambda args: self.filter_table(self.searchBar.get()))
        #load sidemenu items
        self.load_playlistMenu()


        self.label_playlistName = tk.Label(self, text="This is page 1", font=controller.title_font).place(x=0,y=135) # PLACE LABEL
        button_rename_playlist = tk.Button(self,text="change name").place(x=0,y=0) # PLACE LABEL
        button_delete_playlist = tk.Button(self,text="change name").place(x=0,y=0) # PLACE LABEL

        style = ttk.Style()
        style.theme_use('default')
        style.configure("Treeview",
        background="#D3D3D3",
        foreground="black",
        rowheight=30,
        fieldbackground="#D3D3D3",
        height=800)
        style.map("Treeview", background=[("selected","#347083")])
        tree_frame= tk.Frame(self)
        tree_frame.place(x=0,y=300)
        tree_scroll = tk.Scrollbar(tree_frame)
        tree_scroll.pack(side="right", fill="y")
        self.tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode="extended",height=15)
        self.tree.pack()
        tree_scroll.config(command=self.tree.yview)
        self.tree["columns"] = ("PlaylistNumber", "FileName")
        self.tree.column("#0", width=0, stretch="no")
        self.tree.column("PlaylistNumber", anchor="center", width=100)
        self.tree.column("FileName", anchor="center", width=400)
        self.tree.heading("#0", text="", anchor="w")
        self.tree.heading("PlaylistNumber", text="Playlist Number", anchor="center")
        self.tree.heading("FileName", text="File Name", anchor="center")
        self.tree.tag_configure('oddrow', background="white")
        self.tree.tag_configure('evenrow', background="lightblue")

        button_moveUp_playlist = tk.Button(self,text="change name").place(x=0,y=0) # PLACE LABEL
        button_removeFile_playlist = tk.Button(self,text="change name").place(x=0,y=0) # PLACE LABEL
        button_moveDown_playlist = tk.Button(self,text="change name").place(x=0,y=0) # PLACE LABEL
        button_save_playlist = tk.Button(self,text="change name").place(x=0,y=0) # PLACE LABEL



    def move_playlistFile(self,direction):
        pass
    def delete_playlistFile(self,selected):
        pass
    def save_playlist(self):
        pass

    def filter_table(self,search=""):
        for item in self.tree.get_children():
            self.tree.delete(item)
        count = 0
        if self.controller.mediaLibrary.getSize() > 0:
            for key,record in self.controller.mediaLibrary.files.items():
                if search in record.file_name:
                    if count %2 ==0:
                        self.tree.insert(parent="",index="end", iid= count, text="", values=(key,record.file_name,record.file_type),tags=('evenrow',""))

                    else:
                        self.tree.insert(parent="",index="end", iid= count, text="", values=(key,record.file_name,record.file_type),tags=('oddrow',""))
                    count +=1 



    def load_playlistMenu(self):
        tk.Button(self.controller.playlist_frame.inner_frame, text="Add New Playlist2",
                           command=lambda: self.controller.show_frame("PageOne"), bg=self.controller.colourPalette["darkblue"], fg="White").grid(row=0, column=0,columnspan=2,sticky='ew')
        tk.Button(self.controller.playlist_frame.inner_frame, text="Add New Playlist2",
                           command=lambda: self.controller.show_frame("PageOne"), bg=self.controller.colourPalette["darkblue"], fg="White").grid(row=1, column=0,columnspan=2,sticky='ew')
        tk.Button(self.controller.playlist_frame.inner_frame, text="Add New Playl334ist",
                           command=lambda: self.controller.show_frame("PageOne"), bg=self.controller.colourPalette["darkblue"], fg="White").grid(row=2, column=0,columnspan=2,sticky='ew')