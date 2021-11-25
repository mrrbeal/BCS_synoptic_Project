import tkinter as tk
import PIL
from tkinter import ttk
from tkinter.messagebox import askyesno
from tkinter import filedialog as fd
from Data.Utils import MyDialog as MyDialog
import win32api

def DEBUG(text):
    if DEBUGON == True:
        print(text)



DEBUGON = True

class Files(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.searchBar = tk.Entry(self,font=("helvetica",16))
        self.searchBar.grid(column=0,row=0,columnspan=3, pady=25,padx= 50)
        self.searchBar.insert(0, 'Search Files')
        self.searchBar.bind("<FocusIn>", lambda args: self.searchBar.delete('0', 'end'))
        self.searchBar.bind("<KeyRelease>", lambda args: self.filter_table(self.searchBar.get()))
        button_addFiles = tk.Button(self, text="Add Files", command=self.add_files).grid(column=0,row=1,sticky='W')
        button_view_editFiles = tk.Button(self, text="View Or Edit File", command=lambda: controller.show_frame("StartPage")).grid(column=1,row=1,sticky='E')
        button_deleteFiles = tk.Button(self, text="Delete File", command=lambda: self.delete_treeItem()).grid(column=2,row=1,sticky='W')
        button_deleteFiles12 = tk.Button(self, text="Deleteawdwadwd File", command=lambda: self.controller.mediaLibrary.exportLibrary()).grid(column=3,row=1,sticky='W')
        button_deleteFiles2 = tk.Button(self, text="impdd File", command=lambda: self.controller.mediaLibrary.importLibrary()).grid(column=4,row=1,sticky='W')
        button_deleteFiles4 = tk.Button(self, text="Delete File", command=lambda: self.treeSelectedItem()).grid(column=5,row=1,sticky='W')
        tk.Button(self, text="Delete File", command=lambda: self.treeSelectedItem()).grid(column=6,row=1,sticky='W')
        tk.Button(self, text="Delete File", command=lambda: self.treeSelectedItem()).grid(column=7,row=1,sticky='W')
        tk.Button(self, text="Delete File", command=lambda: self.treeSelectedItem()).grid(column=8,row=1,sticky='W')
        tk.Button(self, text="Delete File", command=lambda: self.treeSelectedItem()).grid(column=9,row=1,sticky='W')
        tk.Button(self, text="Delete File", command=lambda: self.treeSelectedItem()).grid(column=10,row=1,sticky='W')

        button_deleteFiles434 = tk.Button(self,text='Print Selected', command=lambda: self.selected_item()).grid(column=11,row=1,sticky='W')




        self.playlistsList=  self.controller.playlistLibrary.playlists
        self.selectedFileID=None
        selectedPlaylistID=None
        self.selectedFile=None

        self.popup = tk.Menu(self, tearoff=0)
        self.popup.add_command(label="Add to Playlist",command=lambda: self.playlistPopup(self.curitem))
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

        tree_frame= tk.Frame(self)
        tree_frame.grid(column=0, row=3, columnspan=3, pady=10)

        tree_scroll = tk.Scrollbar(tree_frame)
        tree_scroll.pack(side="right", fill="y")

        self.tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode="extended",height=15)
        self.tree.pack()

        tree_scroll.config(command=self.tree.yview)

        self.tree["columns"] = ("FileID", "FileName", "FileType")

        self.tree.column("#0", width=0, stretch="no")
        self.tree.column("FileID", anchor="center", width=40)
        self.tree.column("FileName", anchor="center", width=400)
        self.tree.column("FileType", anchor="center", width=60)

        self.tree.heading("#0", text="", anchor="w")
        self.tree.heading("FileID", text="File ID", anchor="center")
        self.tree.heading("FileName", text="File Name", anchor="center")
        self.tree.heading("FileType", text="File Type", anchor="center")

        self.tree.tag_configure('oddrow', background="white")
        self.tree.tag_configure('evenrow', background="lightblue")

        


        #bind right click to pop up menu
        self.tree.bind("<Button-3>", self.do_popup)
        self.tree.bind("<Button-1>", self.fill_view_edit)

        view_editFrame = tk.Frame(self,width=550,height=1000)
        view_editFrame.place(x=550,y=115)
        view_editFrame.grid_propagate(0)
        view_edit_label = tk.Label(view_editFrame,text="View or edit file details below:").place(x=0,y=0)
  
        view_edit_label_fileName = tk.Label(view_editFrame,text="File Name:")
        view_edit_label_fileName.place(x=0,y=45)
        view_edit_label_fileType = tk.Label(view_editFrame,text="File Type:")
        view_edit_label_fileType.place(x=0,y=75)
        view_edit_label_filePath = tk.Label(view_editFrame,text="File Path:")
        view_edit_label_filePath.place(x=0,y=105)
        view_edit_label_commentBox = tk.Label(view_editFrame,text="Comment:")
        view_edit_label_commentBox.place(x=0,y=135)
        view_edit_label_category = tk.Label(view_editFrame,text="Category:")
        view_edit_label_category.place(x=0,y=260)
    

        self.view_edit_entry_fileName = tk.Entry(view_editFrame,text="")
        self.view_edit_entry_fileName.place(x=80,y=45,width=200)
        self.view_edit_entry_fileType = tk.Entry(view_editFrame,text="")
        self.view_edit_entry_fileType.place(x=80,y=75,width=200)
        self.view_edit_entry_filePath = tk.Entry(view_editFrame,text="")
        self.view_edit_entry_filePath.place(x=80,y=105,width=200)
        view_edit_frame_commentBox = tk.Frame(view_editFrame, width=200, height=100)
        view_edit_frame_commentBox.place(x=80,y=135)
        view_edit_frame_commentBox.columnconfigure(0, weight=100)  
        view_edit_frame_commentBox.rowconfigure(0, weight=100)  
        view_edit_frame_commentBox.grid_propagate(0)
        self.view_edit_entry_commentBox = tk.Text(view_edit_frame_commentBox)
        self.view_edit_entry_commentBox.grid(sticky="NSEW")

        view_edit_frame_listbox = tk.Frame(view_editFrame)
        view_edit_frame_listbox.place(x=80,y=260)
        view_edit_frame_listbox.rowconfigure(0, weight=10) 
        view_edit_frame_listbox.columnconfigure(0, weight=10) 
        view_edit_frame_listbox.grid_propagate(0) 
        self.yscrollbar = tk.Scrollbar(view_edit_frame_listbox)
        self.yscrollbar.pack(side = "right", fill = "y")
        self.listBox = tk.Listbox(view_edit_frame_listbox, selectmode = "multiple",yscrollcommand = self.yscrollbar.set)
        self.listBox.pack(pady = 5,fill = "y",expand=1)
        view_edit_label_fileImage = tk.Label(view_editFrame,text="File image:")
        view_edit_label_fileImage.place(x=300,y=0)
        self.view_edit_label_image = tk.Label(view_editFrame,text="",borderwidth=2, relief="ridge")
        self.view_edit_label_image.place(x=300,y=90,height=195, width=195)
        view_edit_button_selectImage = tk.Button(view_editFrame,text="Change image", command=self.update_image_file)
        view_edit_button_selectImage.place(x=350,y=45)
        self.photoImg = None
        self.img = None
        self.tempImagePath = None
        self.view_edit_button_saveChanges = tk.Button(view_editFrame,text="Save changes", command= self.update_file)
        self.view_edit_button_saveChanges.place(x=100,y=450)



    def unselectTable(self):
        self.tree.selection_clear()
        self.view_edit_entry_fileName.delete(0, 'end')
        self.view_edit_entry_filePath.delete(0, 'end')
        self.view_edit_entry_fileType.delete(0, 'end')
        self.view_edit_entry_commentBox.delete(1.0, 'end')
        self.listBox.delete(0,'end')
        self.view_edit_label_image.configure(image=None)

        #populate files table
        self.populateTable()
  
    def add_files(self):
        diag = MyDialog(self,"BOX")
        answer = askyesno("Add a file or a folder ", f"Click 'Yes' to add a file \n or \n click 'No' to add a folder ?")
        if answer:
            filename = fd.askopenfilename(filetypes=diag.selectedTypes)
            self.controller.mediaLibrary.add_file(filename)
        else:
            directory = fd.askdirectory(parent=self,initialdir="/",title='Please select a directory')
            fileTypes = []
            for x in diag.selectedTypes:
                fileTypes.append(x[1][2:].strip())
            self.controller.mediaLibrary.add_folder(directory,fileTypes)
        self.populateTable()

    def select_file(tupletypes= None):#TODO AM I USED
    
        if tupletypes == None:
            filetypes = (
                ('text files', '*.txt'),
                ('All files', '*.*')
            )
        else:
            filetypes = tupletypes

        filename = fd.askopenfilename(
            title='Open a file',
            initialdir='/',
            filetypes=filetypes)

        return filename

    def update_image_file(self):

        filetypes = [('Select Image', '*.png '), ('Select Image', '*.bmp '), ('Select Image', '*.gif '), ('Select Image', '*.jpg ')]

        filename = fd.askopenfilename(
            title='Select an Image',
            initialdir='/',
            filetypes=filetypes)
        width = 195
        height = 195
        self.tempImagePath = filename
        self.img = PIL.Image.open(filename)
        self.img = self.img.resize((width,height), PIL.Image.ANTIALIAS)
        self.photoImg =  PIL.ImageTk.PhotoImage(self.img)
        self.view_edit_label_image.configure(image=self.photoImg)

    def listBox_get_selected_items(self):
        for i in self.listBox.curselection():
            print(self.listBox.get(i))
    
    def listBox_set_selected_items(self,n):
        self.listBox.select_set(n)

    def update_file(self):
        print("CALLED")
        if self.selectedFile != None:
            self.selectedFile.file_path = self.view_edit_entry_filePath.get()
            self.selectedFile.file_name = self.view_edit_entry_fileName.get()
            self.selectedFile.file_type = self.view_edit_entry_fileType.get()
            self.selectedFile.file_comment = self.view_edit_entry_commentBox.get("1.0","end")
            self.selectedFile.categories = []
            for i in self.listBox.curselection():
                self.selectedFile.categories.append(self.listBox.get(i))
            if self.tempImagePath != None:
                self.selectedFile.image_path = self.tempImagePath
        self.tempImagePath = None
        self.populateTable()
        
    def fill_view_edit(self, event):
        item = self.tree.identify("item", event.x, event.y)
        print("you clicked on", self.tree.item(item)["values"])
        selectedFile =self.tree.item(item)["values"][0]
        gotfile = self.controller.mediaLibrary.get_file(selectedFile)      
        self.selectedFile = gotfile  
        self.view_edit_entry_fileName.delete(0, 'end')
        self.view_edit_entry_filePath.delete(0, 'end')
        self.view_edit_entry_fileType.delete(0, 'end')
        self.view_edit_entry_fileName.insert(0,gotfile.file_name)
        self.view_edit_entry_filePath.insert(0,gotfile.file_path)
        self.view_edit_entry_fileType.insert(0,gotfile.file_type)
        self.view_edit_entry_commentBox.delete(1.0, 'end')
        self.view_edit_entry_commentBox.insert(1.0,gotfile.file_comment)
        self.listBox.delete(0,'end')
        if self.controller.categoryList.getSize() > 0:
            sortedList = sorted(self.controller.categoryList.categories)
            print(self.controller.categoryList.categories)
            print(sortedList)
            for i in sortedList:
                self.listBox.insert('end',i)
            for x in gotfile.categories:
                if x in sortedList:
                    self.listBox_set_selected_items(sortedList.index(x))
        width = 195
        height = 195
        print("IMAGE PATH", gotfile.image_path)
        self.img = PIL.Image.open(gotfile.image_path)
        self.img = self.img.resize((width,height), PIL.Image.ANTIALIAS)
        self.photoImg =  PIL.ImageTk.PhotoImage(self.img)
        self.view_edit_label_image.configure(image=self.photoImg)

    def do_popup(self, event): #TODO
        try:
            item = self.tree.identify("item", event.x, event.y)
            curItem = self.tree.focus()
            self.tree.selection_set(item)
            print(self.tree.item(curItem))
            self.curitem = self.tree.item(item)["values"]
            print(item)
            print("you clicked on", self.tree.item(item)["values"])
            self.selectedFileID = self.tree.item(item)["values"][0]
            self.popup.tk_popup(event.x_root, event.y_root, 0,)
        finally:
            self.popup.grab_release()

    def playlistPopup(self,item): #TODO
        last = self.playpopup.index(tk.END)
        if last != None:
            for i in range(last+1):
                self.playpopup.delete(0, "end")
        for l in self.playlistsList:
            self.playpopup.add_command(label=l,command=lambda: self.add_toPlaylist(l,self.curitem))
        x, y = win32api.GetCursorPos()
        try:
            self.playpopup.tk_popup(x+20, y, 0)
        finally:
            self.playpopup.grab_release()

    def delete_treeItem(self):
        curItem = self.tree.focus()
        DEBUG(f"Current ITEM: {curItem}")
        selectedFileID = self.tree.item(curItem)["values"][0]
        selectedFileName = self.tree.item(curItem)["values"][1]
        selectedFileType = self.tree.item(curItem)["values"][2]
        DEBUG(f"selectedFileID: {selectedFileID}")
        DEBUG(f"selectedFileName: {selectedFileName}")
        DEBUG(f"selectedFileName: {selectedFileType}")
        self.controller.mediaLibrary.removeFile(selectedFileID,selectedFileName,selectedFileType)
        self.tree.delete(curItem)

    def populateTable(self,search=""):
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

    def filter_table(self,search):
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

    def add_toPlaylist(self,playlistName,tableItem):
        print("PLAYLISTNAME ",playlistName)
        fileid,filename,filetype = tableItem
        for key, value in self.controller.mediaLibrary.files.items():
            if value.file_name == filename and value.file_type == filetype and key == fileid:
                self.controller.playlistLibrary.add_file_to_playlist(playlistName,value)
     



    

