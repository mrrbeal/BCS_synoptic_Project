import os,sys
import tkinter as tk
from tkinter import Tk, ttk
from tkinter import font as tkfont
from tkinter.constants import BOTH, CENTER, END, NO, RIGHT, W, Y
from tkinter.ttk import *
from tkscrolledframe import ScrolledFrame
from typing import Counter, Text
from PIL import Image, ImageTk
import Database
import win32api


class MediaOrganiser(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title("Whizzy Media Organiser")
        self.geometry("1400x750+10+10")
        self.minsize(400,600)
        self.colourPalette = {"nero": "#252726",
                            "orange": "#FF8700",
                            "lightgrey": "#e0e0e0", 
                            "lightblue" : '#36c3d9',
                            "darkblue" : "#42618a"}
        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        # determine if application is a script file or frozen exe
        if getattr(sys, 'frozen', False):
            self.dname = os.path.dirname(sys.executable)
        elif __file__:
            self.dname = os.path.dirname(__file__)
        #self.database = Database.MediaDataBase(self.dname + r"\Data\system_database.db")
        self.database = Database.MediaDataBase("cheese1.db")

        self.current_session_state = 40
   
        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others

        headerFrame = tk.Frame(self, bg=self.colourPalette["darkblue"], height=50, width=1400, highlightbackground="black",highlightthickness=1)
        headerFrame.place(x=0, y=0)
        #self.logoImage = ImageTk.PhotoImage(Image.open('logo.png').resize((110,110),Image.ANTIALIAS))
        logoLabel = tk.Label(headerFrame, text="MEDIA ORGANISER", bg=self.colourPalette["darkblue"])
        logoLabel.config(font=("stencil", 30),fg="white")
        logoLabel.place(x=0, y=-1)
        headerLabel = tk.Label(headerFrame, text="HEADERLABEL", bg=self.colourPalette["darkblue"],font=self.title_font)
        headerLabel.place(x=700, y=75)


        sideMenu = tk.Frame(self, bg=self.colourPalette["darkblue"], height=700, width=150, highlightbackground="black",highlightthickness=1)
        sideMenu.place(x=0, y=50)
        #sideMenu.grid_propagate(0)
        #options = ["Files", "playlists", "settings", "Help", "About"]
        # Navbar Option Buttons:
        #y = 40
        #for i in range(5):
         #   action = lambda x = options[i]: self.show_frame(x)
          #  tk.Button(sideMenu, text=options[i],command=action, font="BahnschriftLight 15", bg=self.colourPalette["darkblue"], fg="white", activebackground=self.colourPalette["darkblue"], activeforeground="black", bd=0).place(x=25, y=y)
          #  y += 60

        #action = lambda x = options[i]: self.show_frame(x)

### Set up side menu buttons start ################################
        tk.Button(sideMenu, text="Files",command=lambda x = "Files": self.show_frame(x), font="BahnschriftLight 15", 
                    bg=self.colourPalette["darkblue"], fg="white", activebackground=self.colourPalette["darkblue"], activeforeground="black", bd=0).grid(column=0,row=0, columnspan=2)
        self.playlist_frame = ToggledFrame(sideMenu, self, text='playlists')
        self.playlist_frame.mainLabel.config(font="BahnschriftLight 15", bg=self.colourPalette["darkblue"], fg="white", activebackground=self.colourPalette["darkblue"], activeforeground="black", bd=0)
        self.playlist_frame.grid(column=0,row=1, columnspan=2)
        tk.Button(sideMenu, text="settings",command=lambda x = "Files": self.show_frame(x), font="BahnschriftLight 15",
                     bg=self.colourPalette["darkblue"], fg="white", activebackground=self.colourPalette["darkblue"], activeforeground="black", bd=0).grid(column=0,row=2, columnspan=2)
        tk.Button(sideMenu, text="Help",command=lambda x = "Files": self.show_frame(x), font="BahnschriftLight 15", 
                    bg=self.colourPalette["darkblue"], fg="white", activebackground=self.colourPalette["darkblue"], activeforeground="black", bd=0).grid(column=0,row=3, columnspan=2)
### Set up side menu buttons end ##################################

        row = 4
        for i in range(27):
            tk.Label(sideMenu, text="this is nonsence text",bg=self.colourPalette["darkblue"],fg=self.colourPalette["darkblue"]).grid(column=1,row=row)
            row +=1

        container = tk.Frame(self)
        container.place(x=150, y=50)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, Playlists, Files):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="NSEW")

        self.show_frame("Files")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        button1 = tk.Button(self, text="Go to Page One",
                            command=lambda: controller.show_frame("PageOne"))
        button2 = tk.Button(self, text="Go to Page Two",
                            command=lambda: controller.show_frame("PageTwo"))
        button1.pack()
        button2.pack()


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


class Files(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.searchBar = Entry(self,font=("helvetica",16))
        self.searchBar.grid(column=0,row=0,columnspan=3, pady=25,padx= 50)
        self.searchBar.insert(0, 'Search Files')
        self.searchBar.bind("<FocusIn>", lambda args: self.searchBar.delete('0', 'end'))
        self.searchBar.bind("<KeyRelease>", lambda args: self.dynamicTreeSearch(self.searchBar.get()))
        button_addFiles = tk.Button(self, text="Add Files", command=lambda: controller.show_frame("StartPage")).grid(column=0,row=1,sticky='W')
        button_view_editFiles = tk.Button(self, text="View Or Edit File", command=lambda: controller.show_frame("StartPage")).grid(column=1,row=1,sticky='E')
        button_deleteFiles = tk.Button(self, text="Delete File", command=lambda: self.treeSelectedItem()).grid(column=2,row=1,sticky='W')
        button_deleteFiles12 = tk.Button(self, text="Delete File", command=lambda: self.treeSelectedItem()).grid(column=3,row=1,sticky='W')
        button_deleteFiles2 = tk.Button(self, text="Delete File", command=lambda: self.treeSelectedItem()).grid(column=4,row=1,sticky='W')
        button_deleteFiles4 = tk.Button(self, text="Delete File", command=lambda: self.treeSelectedItem()).grid(column=5,row=1,sticky='W')
        button_deleteFiles22 = tk.Button(self, text="Delete File", command=lambda: self.treeSelectedItem()).grid(column=6,row=1,sticky='W')
        button_deleteFiles434 = tk.Button(self,text='Print Selected', command=lambda: self.selected_item()).grid(column=7,row=1,sticky='W')




        self.playlistsList=[1,2,3,4,5]
        self.selectedFileID=None
        selectedPlaylistID=None

        self.popup = tk.Menu(self, tearoff=0)
        self.popup.add_command(label="Add to Playlist",command=self.playlistPopup)
        self.popup.add_command(label="Edit Name")
        self.popup.add_separator()
        self.popup.add_command(label="Exit", command=lambda: self.closeWindow())

        self.playpopup = tk.Menu(self, tearoff=0)


        style = ttk.Style()
        style.theme_use('default')
        style.configure("Treeview",
        background="#D3D3D3",
        foreground="black",
        rowheight=30,
        fieldbackground="#D3D3D3",
        height=800)
        style.map("Treeview", background=[("selected","#347083")])

        tree_frame= Frame(self)
        tree_frame.grid(column=0, row=3, columnspan=3, pady=10)

        tree_scroll = Scrollbar(tree_frame)
        tree_scroll.pack(side=RIGHT, fill=Y)

        self.tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode="extended",height=15)
        self.tree.pack()

        tree_scroll.config(command=self.tree.yview)

        self.tree["columns"] = ("FileID", "FileName", "FileType")

        self.tree.column("#0", width=0, stretch=NO)
        self.tree.column("FileID", anchor=CENTER, width=40)
        self.tree.column("FileName", anchor=CENTER, width=400)
        self.tree.column("FileType", anchor=CENTER, width=60)

        self.tree.heading("#0", text="", anchor=W)
        self.tree.heading("FileID", text="File ID", anchor=CENTER)
        self.tree.heading("FileName", text="File Name", anchor=CENTER)
        self.tree.heading("FileType", text="File Type", anchor=CENTER)

        self.tree.tag_configure('oddrow', background="white")
        self.tree.tag_configure('evenrow', background="lightblue")

    
        #populate table with blank search
        self.dynamicTreeSearch("type")

        #bind right click to pop up menu
        self.tree.bind("<Button-3>", self.do_popup)
        self.tree.bind("<Button-1>", self.fill_view_edit)

        view_editFrame = tk.Frame(self)
        view_editFrame.place(x=550,y=115)
        view_edit_label = tk.Label(view_editFrame,text="View or edit file details below:").grid(column=0,row=0,sticky='N',columnspan=3,pady=10)
        view_edit_label_fileName = tk.Label(view_editFrame,text="File Name:").grid(column=0,row=1,sticky='N',pady=5)
        view_edit_label_fileType = tk.Label(view_editFrame,text="File Path:").grid(column=0,row=2,pady=5)
        view_edit_label_filePath = tk.Label(view_editFrame,text="File Type:").grid(column=0,row=3,pady=5)
        view_edit_label_commentBox = tk.Label(view_editFrame,text="Comment:").grid(column=0,row=4,pady=5)
        view_edit_label_category = tk.Label(view_editFrame,text="Category").grid(column=0,row=6,pady=5) ## include space for comment box
        #need to include image stuffs

        self.view_edit_entry_fileName = tk.Entry(view_editFrame,text="")
        self.view_edit_entry_fileName.grid(column=1,row=1,sticky='N',columnspan=3,pady=5)

        self.view_edit_entry_fileType = tk.Entry(view_editFrame,text="")
        self.view_edit_entry_fileType.grid(column=1,row=2,columnspan=3,pady=5)

        self.view_edit_entry_filePath = tk.Entry(view_editFrame,text="")
        self.view_edit_entry_filePath.grid(column=1,row=3,columnspan=3,pady=5)

        view_edit_frame_commentBox = tk.Frame(view_editFrame, width=200, height=100)
        view_edit_frame_commentBox.grid(column=0,row=5,columnspan=3,pady=5)
        view_edit_frame_commentBox.columnconfigure(0, weight=100)  
        view_edit_frame_commentBox.rowconfigure(0, weight=100)  
        view_edit_frame_commentBox.grid_propagate(False)
        self.view_edit_entry_commentBox = tk.Entry(view_edit_frame_commentBox)
        self.view_edit_entry_commentBox.grid(sticky="NSEW")

        view_edit_frame_listbox = tk.Frame(view_editFrame, width=250, height=10)
        view_edit_frame_listbox.grid(column=1,row=6,columnspan=3,pady=5)
        view_edit_frame_listbox.rowconfigure(0, weight=10) 
        view_edit_frame_listbox.columnconfigure(0, weight=10) 
        view_edit_frame_listbox.grid_propagate(False) 
        yscrollbar = Scrollbar(view_edit_frame_listbox)
        yscrollbar.pack(side = RIGHT, fill = Y)
        self.listBox = tk.Listbox(view_edit_frame_listbox, selectmode = "multiple",yscrollcommand = yscrollbar.set)
        self.listBox.pack(pady = 5)
  
        categories = self.controller.database.database_category_query()
        catlist=[]
        for record in categories:
            if record[2] == self.controller.current_session_state:
                catlist.append(record[1])
    
        self.listBox.insert(END, *catlist)
        yscrollbar.config(command = self.listBox.yview)

    def listBox_get_selected_items(self):
        for i in self.listBox.curselection():
            print(self.listBox.get(i))
    
    def listBox_set_selected_items(self,n):
        self.listBox.select_set(n)

    def fill_view_edit(self, event):
        item = self.tree.identify("item", event.x, event.y)
        print("you clicked on", self.tree.item(item)["values"])
        print(self.tree.item(item)["values"][1])
        
        result = self.controller.database.database_search_files_by_ID(self.tree.item(item)["values"][0],self.controller.current_session_state)

        self.view_edit_entry_fileName.insert(0,result[0][1])
        self.view_edit_entry_filePath.insert(0,result[0][2])
        self.view_edit_entry_fileType.insert(0,result[0][3])
        if result[0][4] != None:
            self.view_edit_entry_commentBox.insert(0,result[0][4])
        #call categories / files then loop through each
        #listBox_set_selected_items(n)

        # add image default or pull file path from DB





    def do_popup(self, event):
        try:
            item = self.tree.identify("item", event.x, event.y)
            curItem = self.tree.focus()
            print(self.tree.item(curItem))
            print(item)
            print("you clicked on", self.tree.item(item)["values"])
            self.selectedFileID = self.tree.item(item)["values"][0]
            self.popup.tk_popup(event.x_root, event.y_root, 0)
        finally:
            self.popup.grab_release()

    def playlistPopup(self):
        for x in self.playlistsList:
            self.playpopup.add_command(label=x)
        x, y = win32api.GetCursorPos()
        try:
            self.playpopup.tk_popup(x+20, y, 0)
        finally:
            self.playpopup.grab_release()
        pass

    def treeSelectedItem(self):
        curItem = self.tree.focus()
        selectedFileID = self.tree.item(curItem)["values"][0]
        selectedFileName = self.tree.item(curItem)["values"][0]
        inputTuple = [selectedFileID,selectedFileName]
        self.controller.database.database_delete_files(selectedFileID)
        self.tree.delete(curItem)

    def dynamicTreeSearch(self,input):
        for item in self.tree.get_children():
            self.tree.delete(item)

        count = 0
        files = self.controller.database.database_search_files(input,self.controller.current_session_state)
        if files != None:
            for record in files:
                print(record)
                if count %2 ==0:
                    self.tree.insert(parent="",index="end", iid= count, text="", values=(record[0],record[1],record[2]),tags=('evenrow',""))

                else:
                    self.tree.insert(parent="",index="end", iid= count, text="", values=(record[0],record[1],record[2]),tags=('oddrow',""))
                count +=1 

        def fill_view_edit_database_search(self,file_id):
            file = self.controller.database.database_search_files_by_ID(file_id,self.controller.current_session_state)
            print(file)


        
    


class ToggledFrame(tk.Frame):

    def __init__(self, parent, controller, text="", *args, **options):
        tk.Frame.__init__(self, parent, *args, **options)

        self.show = tk.IntVar()
        self.show.set(0)

        self.controller = controller
        self.title_frame = tk.Frame(self,background=controller.colourPalette["darkblue"])
        self.title_frame.pack(fill="x", expand=1)

        self.mainLabel = tk.Button(self.title_frame, text=text,command=self.changeFrame)
        self.mainLabel.pack(side="left", fill="x", expand=1)
        self.frame_State = 0
        #self.toggle_button = ttk.Checkbutton(self.title_frame, width=2, text='+', command=self.toggle,
        #                                     variable=self.show, style='Toolbutton')
        self.toggle_button = tk.Button(self.title_frame, text="+",height=1,width=1,bd=0, command=self.toggle)
        self.toggle_button.pack(side="left")

        self.sub_frame = ScrolledFrame(self, relief="sunken", borderwidth=1,background=controller.colourPalette["darkblue"],width=97, height=150)
        self.inner_frame = self.sub_frame.display_widget(Frame)


    def changeFrame(self):
        self.controller.show_frame("Playlists")
        if self.frame_State == 0:
            self.toggle()


    def toggle(self):
        self.frame_State = not self.frame_State
        if bool(self.frame_State):
            self.sub_frame.pack(side="top",fill="both", expand=1)
            self.toggle_button.configure(text='-')
        else:
            self.sub_frame.forget()
            self.toggle_button.configure(text='+')      



if __name__ == "__main__":
    app = MediaOrganiser()
    app.mainloop()