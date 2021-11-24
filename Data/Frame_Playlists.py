import tkinter as tk
from tkinter import Tk, ttk

def DEBUG(text):
    if DEBUGON == True:
        print(text)

DEBUGON = True

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
        self.playlistCount = 1
        self.top_exists = False
        #load sidemenu items
        self.load_playlistMenu()

        self.labelText = tk.StringVar()
        self.label_playlistName = tk.Label(self, textvariable=self.labelText, font=controller.title_font).place(x=0,y=135) # PLACE LABEL
        button_rename_playlist = tk.Button(self,text="change name").place(x=0,y=0) # PLACE LABEL
        button_delete_playlist = tk.Button(self,text="change name",command=lambda: self.delete_playlistFile()).place(x=60,y=0) # PLACE LABEL

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
        #button_save_playlist = tk.Button(self,text="change name").place(x=0,y=0) # PLACE LABEL



    def move_playlistFile(self,direction):
        pass
    def delete_playlistFile(self):
        curItem = self.tree.focus()
        DEBUG(f"Current ITEM: {curItem}")
        selectedPlaylistID = self.tree.item(curItem)["values"][0]
        selectedPlaylistFileName = self.tree.item(curItem)["values"][1]
        DEBUG(f"selectedPlaylistID: {selectedPlaylistID}")
        DEBUG(f"selectedPlaylistFileName: {selectedPlaylistFileName}")
        self.controller.playlistLibrary.delete_file_from_playist(self.labelText.get(),selectedPlaylistID)
        self.tree.delete(curItem)


    def create_playlist(self,name):
        if name.isalnum(): #TODO string validation
            self.controller.playlistLibrary.add_playlist(name)
            tk.Button(self.controller.playlist_frame.inner_frame, text=name,
                            command=lambda: self.load_playlist(name), bg=self.controller.colourPalette["darkblue"], fg="White").grid(row=self.playlistCount, column=0,columnspan=2,sticky='ew')
            self.close_win(self.top)
            self.playlistCount +=1

    def load_playlist(self,name):
        self.labelText.set(name)
        for item in self.tree.get_children():
            self.tree.delete(item)
        count = 0
        if self.controller.playlistLibrary.getSize() > 0:
            for key,record in self.controller.playlistLibrary.playlists.items():
                if name == key:
                    for mediaFile in self.controller.playlistLibrary.playlists[name]:
                        print(mediaFile)
                        print(self.controller.playlistLibrary.playlists[name])
                        if count %2 ==0:
                            self.tree.insert(parent="",index="end", iid= count, text="", values=(mediaFile[0],mediaFile[1]),tags=('evenrow',""))

                        else:
                            self.tree.insert(parent="",index="end", iid= count, text="", values=(mediaFile[0],mediaFile[1]),tags=('oddrow',""))
                        count +=1 
        pass
    
    #TODO
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
        tk.Button(self.controller.playlist_frame.inner_frame, text="Add New Playlist",
                           command=self.popupwin, bg=self.controller.colourPalette["darkblue"], fg="White").grid(row=0, column=0,columnspan=2,sticky='ew')
        for key,record in self.controller.playlistLibrary.playlists.items():
            tk.Button(self.controller.playlist_frame.inner_frame, text=key,
                            command=lambda: self.load_playlist(key), bg=self.controller.colourPalette["darkblue"], fg="White").grid(row=self.playlistCount, column=0,columnspan=2,sticky='ew')
            self.playlistCount +=1
    def popupwin(self):
        if self.top_exists == False:
        #Create a Toplevel window
            self.top= tk.Toplevel(self)
            self.top.geometry("400x150")
            label = tk.Label(self.top,text="Enter A New Playlist Name:")
            label.pack(pady=10)
            entry= tk.Entry(self.top, width= 25)
            entry.pack()
            tk.Button(self.top,text= "Create Playlist", command= lambda:self.create_playlist(entry.get())).pack(pady= 5,in_=self.top, side="top")
            #Create a Button Widget in the Toplevel Window
            tk.Button(self.top, text="Cancel", command=lambda:self.close_win(self.top)).pack(pady=5, in_=self.top, side="top")
            self.top_exists = True

    def close_win(self,top):
        top.destroy()
        self.top_exists = False