import tkinter as tk
from tkinter import Tk, ttk

class Categories(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.searchBar = tk.Entry(self,font=("helvetica",16))
        self.searchBar.grid(column=0,row=0,columnspan=3, pady=25,padx= 50)
        self.searchBar.insert(0, 'Search Files')
        self.searchBar.bind("<FocusIn>", lambda args: self.searchBar.delete('0', 'end'))
        self.searchBar.bind("<KeyRelease>", lambda args: self.dynamicTreeSearch(self.searchBar.get()))
        #control for pop up window pop
        self.top_exists = False
        button_addFiles = tk.Button(self, text="Add A Category", command= self.popupwin).grid(column=0,row=1,sticky='W')
        button_view_editFiles = tk.Button(self, text="View Or Edit File", command=lambda: controller.show_frame("StartPage")).grid(column=1,row=1,sticky='E')
        button_deleteFiles = tk.Button(self, text="Delete File", command=lambda: self.delete_treeItem()).grid(column=2,row=1,sticky='W')
        button_deleteFiles12 = tk.Button(self, text="Delete File", command=lambda: self.treeSelectedItem()).grid(column=3,row=1,sticky='W')
        button_deleteFiles2 = tk.Button(self, text="Delete File", command=lambda: self.treeSelectedItem()).grid(column=4,row=1,sticky='W')
        button_deleteFiles4 = tk.Button(self, text="Delete File", command=lambda: self.treeSelectedItem()).grid(column=5,row=1,sticky='W')
        button_deleteFiles22 = tk.Button(self, text="Delete File", command=lambda: self.treeSelectedItem()).grid(column=6,row=1,sticky='W')
        button_deleteFiles434 = tk.Button(self,text='Print Selected', command=lambda: self.selected_item()).grid(column=7,row=1,sticky='W')

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
        self.dynamicTreeSearch(None)

        #bind right click to pop up menu
        #self.tree.bind("<Button-3>", self.do_popup)
        #self.tree.bind("<Button-1>", self.fill_view_edit)
    

    def dynamicTreeSearch(self,input):
        for item in self.tree.get_children():
            self.tree.delete(item)
        if input == "":
            input = None
        count = 0
        files = self.controller.database.database_category_query(input)
        if files != None:
            for record in files:
                print(record)
                if count %2 ==0:
                    self.tree.insert(parent="",index="end", iid= count, text="", values=(record[0],record[1],record[2]),tags=('evenrow',""))

                else:
                    self.tree.insert(parent="",index="end", iid= count, text="", values=(record[0],record[1],record[2]),tags=('oddrow',""))
                count +=1 

    def delete_treeItem(self):
        curItem = self.tree.focus()
        selectedCatID = self.tree.item(curItem)["values"][0]
        selectedCatName = self.tree.item(curItem)["values"][1]
        self.controller.database.database_category_delete(selectedCatID,selectedCatName)
        page = self.controller.get_page("Files")
        self.tree.delete(curItem)
        page.load_categories()
        self.dynamicTreeSearch(None)


    
    def close_win(self,top):
        top.destroy()
        self.top_exists = False

    def create_category(self,e):
        if e.isdigit() or e.isalpha():
            self.controller.database.database_category_insert(e)
            page = self.controller.get_page("Files")
            self.dynamicTreeSearch(None)
            page.load_categories()
            self.close_win(self.top)
        else:
            #TODO label for error text "name must not be blank"
            pass

    #Define a function to open the Popup Dialogue
    def popupwin(self):
        if self.top_exists == False:
        #Create a Toplevel window
            self.top= tk.Toplevel(self)
            self.top.geometry("400x150")
            #top.eval('tk::PlaceWindow . center')

    #Create an Entry Widget in the Toplevel window
            label = tk.Label(self.top,text="Enter A New Category Name:")
            label.pack(pady=10)
            entry= tk.Entry(self.top, width= 25)
            entry.pack()

        #Create a Button to print something in the Entry widget
            tk.Button(self.top,text= "Create Category", command= lambda:self.create_category(entry.get())).pack(pady= 5,in_=self.top, side="top")
            #Create a Button Widget in the Toplevel Window
            tk.Button(self.top, text="Cancel", command=lambda:self.close_win(self.top)).pack(pady=5, in_=self.top, side="top")
            self.top_exists = True
