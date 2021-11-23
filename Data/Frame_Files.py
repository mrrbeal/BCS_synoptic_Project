import tkinter as tk
from tkinter import Label, Tk, Toplevel, ttk
from tkinter.messagebox import askyesno, askquestion
from tkinter import filedialog as fd
from Data.Utils import MyDialog as MyDialog

def DEBUG(text):
    if DEBUGON == True:
        print(text)

DEBUGON = True

class Files(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.mediaLibrary = MediaLibrary()


        self.controller = controller
        self.searchBar = tk.Entry(self,font=("helvetica",16))
        self.searchBar.grid(column=0,row=0,columnspan=3, pady=25,padx= 50)
        self.searchBar.insert(0, 'Search Files')
        self.searchBar.bind("<FocusIn>", lambda args: self.searchBar.delete('0', 'end'))
        self.searchBar.bind("<KeyRelease>", lambda args: self.dynamicTreeSearch(self.searchBar.get()))
        button_addFiles = tk.Button(self, text="Add Files", command=self.add_files).grid(column=0,row=1,sticky='W')
        button_view_editFiles = tk.Button(self, text="View Or Edit File", command=lambda: controller.show_frame("StartPage")).grid(column=1,row=1,sticky='E')
        button_deleteFiles = tk.Button(self, text="Delete File", command=lambda: self.delete_treeItem()).grid(column=2,row=1,sticky='W')
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

        
        #populate table with blank search
        self.populateTable(self.mediaLibrary)

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
        self.view_edit_entry_commentBox = tk.Text(view_edit_frame_commentBox)
        self.view_edit_entry_commentBox.grid(sticky="NSEW")

        view_edit_frame_listbox = tk.Frame(view_editFrame, width=250, height=10)
        view_edit_frame_listbox.grid(column=1,row=6,columnspan=3,pady=5)
        view_edit_frame_listbox.rowconfigure(0, weight=10) 
        view_edit_frame_listbox.columnconfigure(0, weight=10) 
        view_edit_frame_listbox.grid_propagate(False) 
        self.yscrollbar = tk.Scrollbar(view_edit_frame_listbox)
        self.yscrollbar.pack(side = "right", fill = "y")
        self.listBox = tk.Listbox(view_edit_frame_listbox, selectmode = "multiple",yscrollcommand = self.yscrollbar.set)
        self.listBox.pack(pady = 5)

        self.load_categories()

    def add_files(self):
        diag = MyDialog(self,"BOX")
        answer = askyesno("Add a file or a folder ", f"Click 'Yes' to add a file \n or \n click 'No' to add a folder ?")
        if answer:
            print(diag.selectedTypes)
            filename = fd.askopenfilename(filetypes=diag.selectedTypes)
            self.mediaLibrary.add_file(filename)
        else:
            directory = fd.askdirectory(parent=self,initialdir="/",title='Please select a directory')
            self.mediaLibrary.add_folder(directory)
        self.populateTable(self.mediaLibrary)

    def select_file(tupletypes= None):
    
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


    def load_categories(self):
        self.listBox.delete('0','end')
        categories = self.controller.database.database_category_query()
        catlist=[]
        for record in categories:
            if record[2] == self.controller.current_session_state:
                catlist.append(record[1])
    
        self.listBox.insert("end", *catlist)
        self.yscrollbar.config(command = self.listBox.yview)

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

        self.view_edit_entry_fileName.delete(0, 'end')
        self.view_edit_entry_filePath.delete(0, 'end')
        self.view_edit_entry_fileType.delete(0, 'end')
        self.view_edit_entry_fileName.insert(0,result[0][1])
        self.view_edit_entry_filePath.insert(0,result[0][2])
        self.view_edit_entry_fileType.insert(0,result[0][3])
        self.view_edit_entry_commentBox.delete(1.0, 'end')
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

    def delete_treeItem(self):
        curItem = self.tree.focus()
        DEBUG(f"Current ITEM: {curItem}")
        selectedFileID = self.tree.item(curItem)["values"][0]
        selectedFileName = self.tree.item(curItem)["values"][1]
        DEBUG(f"selectedFileID: {selectedFileID}")
        DEBUG(f"selectedFileName: {selectedFileName}")
        # TODO
        self.tree.delete(curItem)

    def populateTable(self,mediaLibrary):
        for item in self.tree.get_children():
            self.tree.delete(item)

        count = 0
        if self.mediaLibrary.getSize() > 0:
            for record in self.mediaLibrary.files:
                print(record)
                if count %2 ==0:
                    self.tree.insert(parent="",index="end", iid= count, text="", values=(1,record.file_name,record.file_type),tags=('evenrow',""))

                else:
                    self.tree.insert(parent="",index="end", iid= count, text="", values=(1,record.file_name,record.file_type),tags=('oddrow',""))
                count +=1 





import os
class Image:
    def __init__(self,filePath=None) -> None:
        #print(os.path.join(subdir, file))
        if filePath != None:
            self.image_path = filePath
            self.image_name = os.path.split(filePath)[1].split(".")[0]
        else:
            self.image_path = None
            self.image_name = None
    def setImage(self,filePath):
            self.image_path = filePath
            self.image_name = os.path.split(filePath)[1].split(".")[0]

class CategoryList:
    def __init__(self) -> None:
        self.categories = []
    def addCategory(self,name):
        if name.isdigit() or name.isalpha():
            if name not in self.categories:
                self.categories += name





class MediaFile(Image):
    def __init__(self,filePath) -> None:
        self.file_path = filePath
        self.file_name = os.path.split(filePath)[1].split(".")[0]
        self.file_type = os.path.splitext(filePath)[1][1:]
        self.comment = ""

class MediaLibrary:
    def __init__(self) -> None:
        self.files = []
    def getSize(self):
        return len(self.files)
    def add_file(self,filePath):
        self.files.append(MediaFile(filePath))
        pass
    def add_folder(self,folderDir,fileTypes) -> list:
        for subdir, dir, files in os.walk(folderDir):
            for file in files:
                file_path = subdir + os.sep + file
                file_type = os.path.splitext(file)[1][1:]
                if file_type in fileTypes:
                    self.files.append(MediaFile(file_path))
    def exportLibrary():
        pass
    def importLibrary(json):
        pass



    

