import tkinter as tk
from tkinter import Tk, ttk

from Data.Frame_Files import Files

def DEBUG(text):
    if DEBUGON == True:
        print(text)



DEBUGON = True

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
        tree_frame.grid(column=0, row=3, columnspan=1, pady=10)

        tree_scroll = tk.Scrollbar(tree_frame)
        tree_scroll.pack(side="right", fill="y")

        self.tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode="extended",height=15)
        self.tree.pack()

        tree_scroll.config(command=self.tree.yview)

        self.tree["columns"] = ("CategoryName")

        self.tree.column("#0", width=0, stretch="no")
        self.tree.column("CategoryName", anchor="center", width=400)

        self.tree.heading("#0", text="", anchor="w")
        self.tree.heading("CategoryName", text="Category Name", anchor="center")

        self.tree.tag_configure('oddrow', background="white")
        self.tree.tag_configure('evenrow', background="lightblue")

    
        #populate table with blank search
        self.populateTable()

        #bind right click to pop up menu
        #self.tree.bind("<Button-3>", self.do_popup)
        #self.tree.bind("<Button-1>", self.fill_view_edit)
    

    def populateTable(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        count = 0
        if self.controller.categoryList.getSize() > 0:
            for record in self.controller.categoryList.categories:
                if count %2 ==0:
                    self.tree.insert(parent="",index="end", iid= count, text="", values=(record),tags=('evenrow',""))

                else:
                    self.tree.insert(parent="",index="end", iid= count, text="", values=(record),tags=('oddrow',""))
                count +=1 

    def delete_treeItem(self):
        curItem = self.tree.focus()
        DEBUG(f"Current ITEM: {curItem}")
        categoryName = self.tree.item(curItem)["values"][0]
        DEBUG(f"selectedFileID: {categoryName}")
        self.controller.categoryList.removeCategory(categoryName)
        self.tree.delete(curItem)

    def close_win(self,top):
        top.destroy()
        self.top_exists = False

    def create_category(self,e):
        print("ENTRY IS ", e)
        if e.isdigit() or e.isalpha():
            if e not in self.controller.categoryList.categories:
                self.controller.categoryList.createCategory(e.strip())
                self.populateTable()
                self.close_win(self.top)
        page = self.controller.get_page("Files")
        page.unselectTable()

    def popupwin(self):
        if self.top_exists == False:
        #Create a Toplevel window
            self.top= tk.Toplevel(self)
            self.top.geometry("400x150")
            label = tk.Label(self.top,text="Enter A New Category Name:")
            label.pack(pady=10)
            entry= tk.Entry(self.top, width= 25)
            entry.pack()
            tk.Button(self.top,text= "Create Category", command= lambda:self.create_category(entry.get())).pack(pady= 5,in_=self.top, side="top")
            #Create a Button Widget in the Toplevel Window
            tk.Button(self.top, text="Cancel", command=lambda:self.close_win(self.top)).pack(pady=5, in_=self.top, side="top")
            self.top_exists = True

    def update_Category(self):#TODO
        pass
    def delete_Category(self):#TODO
        pass